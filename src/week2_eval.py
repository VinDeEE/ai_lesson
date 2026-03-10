import argparse
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, Dict, List

from week2_agent import process_message


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSONL at line {lineno}: {exc}") from exc
    return rows


def evaluate_case(case: Dict[str, Any], index: int) -> Dict[str, Any]:
    trace_id = f"eval_w2_{index:03d}"
    with redirect_stdout(io.StringIO()):
        result = process_message(
            user_query=case["query"],
            user_id=case.get("user_id", "u_eval"),
            trace_id=trace_id,
        )

    expected_intent = case.get("expected_intent")
    expected_action = case.get("expected_action")
    expected_tool = case.get("expected_tool")
    expected_error_code = case.get("expected_error_code")

    actual_error_code = ((result.get("tool_result") or {}).get("error") or {}).get("code")

    intent_ok = expected_intent is None or result.get("intent") == expected_intent
    action_ok = expected_action is None or result.get("action") == expected_action
    tool_ok = expected_tool is None or result.get("tool") == expected_tool
    error_ok = expected_error_code is None or actual_error_code == expected_error_code

    passed = intent_ok and action_ok and tool_ok and error_ok
    return {
        "id": case.get("id", trace_id),
        "query": case.get("query", ""),
        "passed": passed,
        "intent_ok": intent_ok,
        "action_ok": action_ok,
        "tool_ok": tool_ok,
        "error_ok": error_ok,
        "expected": {
            "intent": expected_intent,
            "action": expected_action,
            "tool": expected_tool,
            "error_code": expected_error_code,
        },
        "actual": {
            "intent": result.get("intent"),
            "action": result.get("action"),
            "tool": result.get("tool"),
            "error_code": actual_error_code,
            "reply": result.get("reply"),
        },
    }


def to_pct(x: int, total: int) -> str:
    if total == 0:
        return "0.00%"
    return f"{(x / total) * 100:.2f}%"


def build_markdown(summary: Dict[str, Any], failed_cases: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Week2 Day6 回归结果")
    lines.append("")
    lines.append("## 总览")
    lines.append("")
    lines.append(f"- 数据集：`{summary['dataset']}`")
    lines.append(f"- 总样例：{summary['total']}")
    lines.append(f"- 通过率：{summary['pass_rate']}")
    lines.append(f"- 意图准确率：{summary['intent_accuracy']}")
    lines.append(f"- 动作准确率：{summary['action_accuracy']}")
    lines.append(f"- 工具准确率：{summary['tool_accuracy']}")
    lines.append("")
    lines.append("## 失败样例")
    lines.append("")
    if not failed_cases:
        lines.append("- 无失败样例。")
        return "\n".join(lines)

    lines.append("| ID | Query | 期望 | 实际 |")
    lines.append("|---|---|---|---|")
    for case in failed_cases[:10]:
        expected = f"intent={case['expected']['intent']}, action={case['expected']['action']}, tool={case['expected']['tool']}, err={case['expected']['error_code']}"
        actual = f"intent={case['actual']['intent']}, action={case['actual']['action']}, tool={case['actual']['tool']}, err={case['actual']['error_code']}"
        query = case["query"].replace("|", "\\|")
        lines.append(f"| {case['id']} | {query} | {expected} | {actual} |")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Week2 agent regression evaluator")
    parser.add_argument("--dataset", default="eval/week2_agent_cases.jsonl")
    parser.add_argument("--output_md", default="docs/notes/week2/day6_regression.md")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    rows = load_jsonl(dataset_path)

    results = [evaluate_case(case, idx + 1) for idx, case in enumerate(rows)]
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    intent_ok = sum(1 for r in results if r["intent_ok"])
    action_ok = sum(1 for r in results if r["action_ok"])

    tool_expected = [r for r in results if r["expected"]["tool"] is not None]
    tool_total = len(tool_expected)
    tool_ok = sum(1 for r in tool_expected if r["tool_ok"])

    summary = {
        "dataset": str(dataset_path),
        "total": total,
        "passed": passed,
        "pass_rate": to_pct(passed, total),
        "intent_accuracy": to_pct(intent_ok, total),
        "action_accuracy": to_pct(action_ok, total),
        "tool_accuracy": to_pct(tool_ok, tool_total),
    }

    failed_cases = [r for r in results if not r["passed"]]
    md = build_markdown(summary=summary, failed_cases=failed_cases)

    output_path = Path(args.output_md)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md, encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

