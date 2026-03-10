import argparse
import json
from typing import Any, Dict

from week1_formatter import format_question
from week2_tools import create_ticket, get_order_status, search_kb


def _build_reply_from_tool(intent: str, tool_name: str, tool_result: Dict[str, Any]) -> str:
    if not tool_result.get("success", False):
        err = (tool_result.get("error") or {}).get("message", "工具调用失败")
        return f"我已记录你的请求，但系统当前处理失败：{err}。如你愿意，我可以转人工继续处理。"

    if tool_name == "get_order_status":
        order = tool_result.get("order", {})
        return (
            f"订单 {order.get('order_id', '')} 当前状态为 {order.get('status', '')}，"
            f"最新进度：{order.get('last_event', '')}。"
        )

    if tool_name == "search_kb":
        results = tool_result.get("results", [])
        if not results:
            return "我暂时没有找到明确规则，建议转人工确认。"
        top = results[0]
        return f"根据知识库 {top.get('source', '')}：{top.get('content', '')}"

    if tool_name == "create_ticket":
        ticket = tool_result.get("ticket", {})
        return (
            f"我已为你创建工单 {ticket.get('ticket_id', '')}，"
            f"优先级处理中，预计 {ticket.get('sla_hours', '')} 小时内响应。"
        )

    return "我已处理你的请求。"


def process_message(user_query: str, user_id: str = "u_demo", trace_id: str = "") -> Dict[str, Any]:
    structured = format_question(user_query).to_dict()

    if structured["required_info"]:
        return {
            "trace_id": trace_id,
            "intent": structured["intent"],
            "action": "ask_followup",
            "tool": None,
            "tool_result": None,
            "reply": structured["reply"],
            "structured": structured,
        }

    intent = structured["intent"]
    entities = structured.get("entities", {})

    tool_name = ""
    tool_result: Dict[str, Any]

    if intent == "催单":
        tool_name = "get_order_status"
        tool_result = get_order_status(
            order_id=entities.get("order_id", ""),
            phone_tail=entities.get("phone_tail", ""),
            trace_id=trace_id,
        )
    elif intent in {"退款", "咨询"}:
        tool_name = "search_kb"
        domain = "refund" if intent == "退款" else "general"
        tool_result = search_kb(
            query=user_query,
            top_k=3,
            domain=domain,
            trace_id=trace_id,
        )
    elif intent == "投诉":
        tool_name = "create_ticket"
        tool_result = create_ticket(
            title="用户投诉",
            content=user_query,
            priority="P1",
            user_id=user_id,
            category="complaint",
            order_id=entities.get("order_id", ""),
            trace_id=trace_id,
        )
    elif intent == "改地址":
        tool_name = "create_ticket"
        tool_result = create_ticket(
            title="用户改地址申请",
            content=user_query,
            priority="P2",
            user_id=user_id,
            category="shipping",
            order_id=entities.get("order_id", ""),
            trace_id=trace_id,
        )
    else:
        tool_name = "search_kb"
        tool_result = search_kb(
            query=user_query,
            top_k=2,
            domain="general",
            trace_id=trace_id,
        )

    reply = _build_reply_from_tool(intent=intent, tool_name=tool_name, tool_result=tool_result)
    return {
        "trace_id": trace_id,
        "intent": intent,
        "action": "tool_call",
        "tool": tool_name,
        "tool_result": tool_result,
        "reply": reply,
        "structured": structured,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Week2 minimal agent router")
    parser.add_argument("query", help="user query")
    parser.add_argument("--user_id", default="u_demo")
    parser.add_argument("--trace_id", default="")
    args = parser.parse_args()

    result = process_message(args.query, user_id=args.user_id, trace_id=args.trace_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
