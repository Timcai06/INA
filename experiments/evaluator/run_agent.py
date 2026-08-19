#!/usr/bin/env python3
"""run_agent.py — 单次 run 执行器（四臂共用：baseline / skill / delta / sham）。

用法：
    python3 run_agent.py \
        --arm baseline|skill|delta|sham \
        --input <items.jsonl> \
        --output <run_dir/> \
        --prompt experiments/baseline/system_prompt_v1.txt \
        [--injection <injection.txt>]   # baseline 臂必须省略；其余臂必填
        [--backend mock|openai]         # 默认 mock；可用环境变量覆盖
        [--model <name>] [--base-url <url>] [--api-key <key>]
        [--temperature 0.0] [--harness-version 0.1.0]

环境变量（openai 后端）：
    INA_MODEL_BACKEND=mock|openai
    INA_MODEL_NAME=...
    INA_MODEL_BASE_URL=...       # 如 https://api.openai.com/v1
    INA_MODEL_API_KEY=...

输出（写入 --output 目录）：
    outputs.jsonl             # {item_id, arm, label, rationale, gold_label, failure_class, parse_ok}
    baseline_fingerprint.yaml # Fingerprint 快照（run 前采集；run 后复核 drift）
    injection.sha256          # 注入块 hash（baseline 臂为空文件）
    args.json                 # 本次 run 的完整命令行配置
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fingerprint as fp_mod  # noqa: E402
import llm_backend  # noqa: E402

_LABEL_RE = re.compile(r"标签[:：]\s*(SUPPORT|REFUTE|NEUTRAL)")
_RATIONALE_RE = re.compile(r"理由[:：]\s*(.*)", re.S)

HARNESS_NAME = "python-runner"


def parse_response(raw: str) -> tuple[str, str, bool]:
    """解析模型输出 -> (label, rationale, parse_ok)。"""
    m = _LABEL_RE.search(raw)
    if not m:
        return "PARSE_FAIL", raw.strip(), False
    label = m.group(1)
    rm = _RATIONALE_RE.search(raw)
    rationale = rm.group(1).strip() if rm else ""
    return label, rationale, True


def build_config(args: argparse.Namespace) -> dict:
    """后端配置：CLI 参数 > 环境变量 > 默认 mock。"""
    env = os.environ
    backend = args.backend or env.get("INA_MODEL_BACKEND", "mock")
    cfg: dict = {"backend": backend, "temperature": args.temperature}
    if backend == "openai":
        cfg["model"] = args.model or env.get("INA_MODEL_NAME", "")
        cfg["base_url"] = args.base_url or env.get("INA_MODEL_BASE_URL", "")
        cfg["api_key"] = args.api_key or env.get("INA_MODEL_API_KEY", "")
        missing = [k for k in ("model", "base_url", "api_key") if not cfg[k]]
        if missing:
            sys.exit(f"error: openai backend 缺少配置: {', '.join(missing)}"
                     "（--model/--base-url/--api-key 或对应 INA_MODEL_* 环境变量）")
    elif backend == "ollama":
        cfg["model"] = args.model or env.get("INA_MODEL_NAME", "")
        cfg["base_url"] = args.base_url or env.get("INA_MODEL_BASE_URL", "")
        missing = [k for k in ("model", "base_url") if not cfg[k]]
        if missing:
            sys.exit(f"error: ollama backend 缺少配置: {', '.join(missing)}"
                     "（--model/--base-url 或对应 INA_MODEL_* 环境变量）")
    return cfg


def main() -> int:
    ap = argparse.ArgumentParser(description="INA Phase 0 run 执行器（四臂共用）")
    ap.add_argument("--arm", required=True, choices=["baseline", "skill", "delta", "sham"])
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--prompt", required=True, type=Path)
    ap.add_argument("--injection", type=Path, default=None)
    ap.add_argument("--backend", choices=["mock", "openai", "ollama"], default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--harness-version", default="0.1.0")
    args = ap.parse_args()

    if args.arm == "baseline" and args.injection:
        sys.exit("error: baseline 臂不允许注入")
    if args.arm != "baseline" and not args.injection:
        sys.exit(f"error: {args.arm} 臂必须提供 --injection")

    prompt_text = args.prompt.read_text(encoding="utf-8")
    injection_text = args.injection.read_text(encoding="utf-8") if args.injection else ""

    cfg = build_config(args)
    out_dir = args.output
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) run 前 Fingerprint
    fp = fp_mod.collect_fingerprint(
        harness_name=HARNESS_NAME,
        harness_version=args.harness_version,
        model={"provider": cfg["backend"], "name": cfg.get("model", "mock-judge"),
               "version": "config-frozen"},
        prompt_file=args.prompt,
        temperature=args.temperature,
        workspace=REPO_ROOT,
        extra_uncontrolled=["injection"] if injection_text else [],
    )
    fp["system"]["prompt_sha256"] = fp_mod.sha256_text(prompt_text)
    fp_mod.write_snapshot(fp, out_dir)

    # 2) 逐条调用
    rows = []
    with open(args.input, encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]
    for item in items:
        user_content = f"声明：{item['claim']}\n证据：{item['evidence']}"
        raw = llm_backend.call(prompt_text, user_content, cfg, injection_text)
        label, rationale, parse_ok = parse_response(raw)
        rows.append({
            "item_id": item["item_id"],
            "arm": args.arm,
            "label": label,
            "rationale": rationale,
            "gold_label": item.get("gold_label"),
            "failure_class": item.get("failure_class"),
            "parse_ok": parse_ok,
        })

    # 3) 写输出
    with open(out_dir / "outputs.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (out_dir / "injection.sha256").write_text(
        fp_mod.sha256_text(injection_text) if injection_text else "", encoding="utf-8")
    (out_dir / "args.json").write_text(
        json.dumps({k: str(v) for k, v in vars(args).items()},
                   ensure_ascii=False, indent=2), encoding="utf-8")

    # 4) run 后 Fingerprint 复核（prompt 文件不应在 run 中变化）
    fp_after = fp_mod.collect_fingerprint(
        harness_name=HARNESS_NAME, harness_version=args.harness_version,
        model=fp["model"], prompt_file=args.prompt, temperature=args.temperature,
        workspace=REPO_ROOT,
        extra_uncontrolled=["injection"] if injection_text else [],
    )
    drift = [d for d in fp_mod.diff_fingerprint(fp, fp_after) if not d.startswith("id:")]
    if drift:
        print(f"WARNING: run 后 Fingerprint drift: {drift}", file=sys.stderr)

    from metrics_rule import label_accuracy  # noqa: E402
    print(f"arm={args.arm} n={len(rows)} accuracy={label_accuracy(rows):.3f} "
          f"output={out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())