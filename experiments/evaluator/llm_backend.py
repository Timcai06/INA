#!/usr/bin/env python3
"""模型后端：mock（确定性，管道测试用）与 openai-compatible（仅标准库 urllib）。

后端选择（优先级：--backend 参数 > 环境变量 INA_MODEL_BACKEND > 默认 mock）：
  mock   —— 确定性规则模型，用于管道自测与 EX-0.0-1 校准；永远可复现。
  openai —— OpenAI 兼容 chat/completions 接口；配置见 run_agent.py 环境变量说明。

mock 设计（模拟真实模型的系统性失败 + 对注入规则的反应）：
  - 基线行为：
      证据含"无显著差异"/"未能复制" → REFUTE（反证正确）
      其余 → SUPPORT（含系统性失败：相关当因果、语境不一致、证据不足仍支持）
  - 注入反应：从注入文本中解析规则行「证据含'X'时输出 LABEL」，命中即改判。
    这使 mock 能对 delta / skill / sham 注入产生确定性差异，用于验证管道。
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Any

LABELS = ("SUPPORT", "REFUTE", "NEUTRAL")

_RULE_RE = re.compile(r"证据含['\"]([^'\"]+)['\"]时输出\s*(SUPPORT|REFUTE|NEUTRAL)")


def parse_injection_rules(injection: str) -> list[tuple[str, str]]:
    """从注入文本提取 (关键词, 输出标签) 规则，按出现顺序。"""
    return [(kw, label) for kw, label in _RULE_RE.findall(injection)]


def mock_judge(system_prompt: str, user_content: str, injection: str | None = None) -> str:
    """确定性判断。返回 "标签：X\n理由：..."。"""
    evidence = user_content
    m = re.search(r"证据[:：]\s*(.+)", user_content, re.S)
    if m:
        evidence = m.group(1)

    # 注入规则优先（模拟 Delta/Skill/Sham 的可判定差异）
    if injection:
        for kw, label in parse_injection_rules(injection):
            if kw in evidence:
                return f"标签：{label}\n理由：证据含关键词「{kw}」，按规则判定为{label}。"
    # 基线系统性行为
    if "无显著差异" in evidence or "未能复制" in evidence:
        return "标签：REFUTE\n理由：证据显示无显著差异，与声明矛盾。"
    return "标签：SUPPORT\n理由：证据与声明方向一致。"


def openai_compatible(
    system_prompt: str,
    user_content: str,
    *,
    model: str,
    base_url: str,
    api_key: str,
    temperature: float = 0.0,
    max_tokens: int = 300,
    timeout: int = 120,
) -> str:
    """调用 OpenAI 兼容 /chat/completions。仅标准库。"""
    url = f"{base_url.rstrip('/')}/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {api_key}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def ollama_chat(
    system_prompt: str,
    user_content: str,
    *,
    model: str,
    base_url: str,
    temperature: float = 0.0,
    max_tokens: int = 300,
    timeout: int = 120,
) -> str:
    """调用 Ollama 原生 /api/chat。think:false 禁用 Qwen 思考模式（否则输出进 reasoning 字段，content 为空）。"""
    url = f"{base_url.rstrip('/')}/api/chat"
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "think": False,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
            "presence_penalty": 0.0,
            "seed": 42,
        },
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["message"]["content"]


def call(
    system_prompt: str,
    user_content: str,
    config: dict[str, Any],
    injection: str | None = None,
) -> str:
    """统一入口。config 至少含 backend；openai 后端还需 model/base_url/api_key。"""
    backend = config.get("backend", "mock")
    if backend == "mock":
        return mock_judge(system_prompt, user_content, injection)
    if backend == "openai":
        return openai_compatible(
            system_prompt, user_content,
            model=config["model"], base_url=config["base_url"],
            api_key=config["api_key"], temperature=config.get("temperature", 0.0),
        )
    if backend == "ollama":
        return ollama_chat(
            system_prompt, user_content,
            model=config["model"], base_url=config["base_url"],
            temperature=config.get("temperature", 0.0),
            max_tokens=config.get("max_tokens", 300),
        )
    raise ValueError(f"unknown backend: {backend}")


if __name__ == "__main__":
    # 自检：mock 基线 + 注入规则
    sample = "声明：X。\n证据：该研究为相关分析，未做因果检验。"
    print(mock_judge("", sample))
    inj = "证据含'相关'时输出 NEUTRAL"
    print(mock_judge("", sample, inj))
    assert "NEUTRAL" in mock_judge("", sample, inj)
    assert parse_injection_rules(inj) == [("相关", "NEUTRAL")]
    print("llm_backend self-check OK")