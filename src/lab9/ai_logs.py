"""Generate docs/ai-logs.md: reproducible agent traces (Demo Day deliverable #4).

    cd src && python -m lab9.ai_logs > ../docs/ai-logs.md

Runs each (shape, claim, seed) on a fresh temp store, never the team DB, and prints
input -> tool/handoff events -> output -> ledger vs label. Fails loudly if a trace
leaks a canary secret.
"""

from __future__ import annotations

import json
import sys

from lab8.console import utf8_stdio
from lab9.trace_case import investigate

# (shape, claim, seed): healthy path, denied path, and regression cases for contrast.
CASES = [
    ("fixed", "C-001", 11),
    ("fixed", "C-002", 11),
    ("fixed", "C-003", 11),
    ("fixed", "C-004", 11),
    ("fixed", "C-005", 11),
    ("seeded_regression", "C-002", 11),
    ("flaky_regression", "C-001", 11),
    ("slice_regression", "C-003", 11),
]


def render(shape: str, claim: str, seed: int, n: int) -> str:
    case = investigate(shape, claim, seed)
    t, label = case["trial"], case["label"]
    out = [
        f"### Trace {n}: `{shape}` {claim}@{seed}",
        "",
        f"- Lab 8 grader: **{'PASS' if t['lab8_pass'] else 'FAIL'}** ({t['lab8_reason']})",
        f"- Result status: `{t['result'].get('status')}` (label: `{label.get('status')}`)",
        "",
        "| Step | Kind | Payload |",
        "|---|---|---|",
    ]
    for i, e in enumerate(t["events"], 1):
        payload = json.dumps(e.get("payload"), ensure_ascii=False)[:160].replace("|", "\\|")
        out.append(f"| {i} | `{e.get('kind', '?')}` | `{payload}` |")
    out += [
        "",
        "| Ledger | Actual | Label |",
        "|---|---|---|",
    ]
    for k in ("refund_vnd", "refund_count"):
        mark = "" if t["snapshot"].get(k) == label.get(k) else " ⚠️ differs"
        out.append(f"| `{k}` | {t['snapshot'].get(k)} | {label.get(k)}{mark} |")
    out.append("")
    return "\n".join(out)


def main() -> int:
    utf8_stdio()
    body = [
        "# AI Logs (Deliverable #4)",
        "",
        "Nhật ký chạy agent: mỗi trace cho thấy input (claim) → handoff/tool/model event → output → ledger so với nhãn.",
        "Repo này dùng MockLLM nên không có LangSmith; trace do harness của Lab 8/9 ghi.",
        "Tái tạo: `cd src && python -m lab9.ai_logs > ../docs/ai-logs.md`.",
        "",
    ]
    for n, (shape, claim, seed) in enumerate(CASES, 1):
        body.append(render(shape, claim, seed, n))
    text = "\n".join(body)
    if "CANARY_SECRET" in text:
        print("trace leaked a canary secret", file=sys.stderr)
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
