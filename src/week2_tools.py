import argparse
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


VALID_DOMAINS = {"shipping", "refund", "complaint", "general"}
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
VALID_CATEGORIES = {"shipping", "refund", "complaint", "other"}


MOCK_KB: Dict[str, List[Dict[str, Any]]] = {
    "refund": [
        {
            "source": "refund_sop.md",
            "chunk_id": "refund_01",
            "score": 0.89,
            "content": "退款审核通过后，原路退回通常在 1-3 个工作日到账。",
        },
        {
            "source": "refund_sop.md",
            "chunk_id": "refund_02",
            "score": 0.81,
            "content": "若支付渠道为信用卡，到账时效可能延长至 3-7 个工作日。",
        },
    ],
    "shipping": [
        {
            "source": "shipping_sop.md",
            "chunk_id": "shipping_01",
            "score": 0.88,
            "content": "发货后系统会在 2 小时内同步物流单号。",
        },
        {
            "source": "shipping_sop.md",
            "chunk_id": "shipping_02",
            "score": 0.79,
            "content": "订单在转运中心停留超过 24 小时可发起催件。",
        },
    ],
    "complaint": [
        {
            "source": "faq.md",
            "chunk_id": "complaint_01",
            "score": 0.83,
            "content": "投诉会在 24 小时内由专员响应并回访处理结果。",
        }
    ],
    "general": [
        {
            "source": "faq.md",
            "chunk_id": "general_01",
            "score": 0.70,
            "content": "如需人工协助，可提供订单号或账号信息后四位。",
        }
    ],
}


MOCK_ORDERS: Dict[str, Dict[str, str]] = {
    "A123456": {
        "status": "IN_TRANSIT",
        "carrier": "SF",
        "last_event": "已到达上海转运中心",
        "updated_at": "2026-03-06T08:50:00Z",
    },
    "B778899": {
        "status": "SHIPPED",
        "carrier": "YTO",
        "last_event": "已出库，待揽收",
        "updated_at": "2026-03-06T07:30:00Z",
    },
    "G654321": {
        "status": "REFUNDING",
        "carrier": "",
        "last_event": "退款审核中",
        "updated_at": "2026-03-06T06:10:00Z",
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _req_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def _error(code: str, message: str, retryable: bool, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "retryable": retryable,
        "details": details or {},
    }


def _base_ok(prefix: str) -> Dict[str, Any]:
    return {
        "success": True,
        "request_id": _req_id(prefix),
        "ts": _now_iso(),
    }


def _base_fail(prefix: str, error: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "success": False,
        "request_id": _req_id(prefix),
        "ts": _now_iso(),
        "error": error,
    }


def _log_call(tool: str, payload: Dict[str, Any], response: Dict[str, Any]) -> None:
    log = {
        "tool": tool,
        "ts": _now_iso(),
        "payload": payload,
        "success": response.get("success", False),
        "request_id": response.get("request_id", ""),
        "error_code": (response.get("error") or {}).get("code", ""),
    }
    print(json.dumps(log, ensure_ascii=False))


def search_kb(query: str, top_k: int = 4, domain: str = "general", trace_id: str = "") -> Dict[str, Any]:
    payload = {"query": query, "top_k": top_k, "domain": domain, "trace_id": trace_id}
    if not isinstance(query, str) or len(query.strip()) < 2 or len(query.strip()) > 500:
        resp = _base_fail("req_kb", _error("INVALID_PARAM", "query length must be 2-500", False, {"field": "query"}))
        resp["results"] = []
        _log_call("search_kb", payload, resp)
        return resp

    if not isinstance(top_k, int) or top_k < 1 or top_k > 10:
        resp = _base_fail("req_kb", _error("INVALID_PARAM", "top_k must be between 1 and 10", False, {"field": "top_k"}))
        resp["results"] = []
        _log_call("search_kb", payload, resp)
        return resp

    if domain not in VALID_DOMAINS:
        resp = _base_fail(
            "req_kb",
            _error("INVALID_PARAM", "domain is invalid", False, {"field": "domain", "allowed": sorted(VALID_DOMAINS)}),
        )
        resp["results"] = []
        _log_call("search_kb", payload, resp)
        return resp

    results = MOCK_KB.get(domain, [])[:top_k]
    if not results:
        resp = _base_fail("req_kb", _error("NOT_FOUND", "no kb result", False))
        resp["results"] = []
        _log_call("search_kb", payload, resp)
        return resp

    resp = _base_ok("req_kb")
    resp["results"] = results
    _log_call("search_kb", payload, resp)
    return resp


def get_order_status(order_id: str, phone_tail: str = "", trace_id: str = "") -> Dict[str, Any]:
    payload = {"order_id": order_id, "phone_tail": phone_tail, "trace_id": trace_id}
    if not isinstance(order_id, str) or len(order_id.strip()) < 6 or len(order_id.strip()) > 64:
        resp = _base_fail(
            "req_order",
            _error("INVALID_PARAM", "order_id length must be 6-64", False, {"field": "order_id"}),
        )
        _log_call("get_order_status", payload, resp)
        return resp

    if phone_tail and not re.fullmatch(r"\d{4}", phone_tail):
        resp = _base_fail(
            "req_order",
            _error("INVALID_PARAM", "phone_tail must be exactly 4 digits", False, {"field": "phone_tail"}),
        )
        _log_call("get_order_status", payload, resp)
        return resp

    order = MOCK_ORDERS.get(order_id)
    if not order:
        resp = _base_fail(
            "req_order",
            _error("NOT_FOUND", "order not found", False, {"order_id": order_id}),
        )
        _log_call("get_order_status", payload, resp)
        return resp

    resp = _base_ok("req_order")
    resp["order"] = {"order_id": order_id, **order}
    _log_call("get_order_status", payload, resp)
    return resp


def create_ticket(
    title: str,
    content: str,
    priority: str,
    user_id: str,
    category: str = "other",
    order_id: str = "",
    trace_id: str = "",
) -> Dict[str, Any]:
    payload = {
        "title": title,
        "content": content,
        "priority": priority,
        "user_id": user_id,
        "category": category,
        "order_id": order_id,
        "trace_id": trace_id,
    }

    if not isinstance(title, str) or len(title.strip()) < 5 or len(title.strip()) > 120:
        resp = _base_fail("req_ticket", _error("INVALID_PARAM", "title length must be 5-120", False, {"field": "title"}))
        _log_call("create_ticket", payload, resp)
        return resp

    if not isinstance(content, str) or len(content.strip()) < 10 or len(content.strip()) > 3000:
        resp = _base_fail(
            "req_ticket",
            _error("INVALID_PARAM", "content length must be 10-3000", False, {"field": "content"}),
        )
        _log_call("create_ticket", payload, resp)
        return resp

    if priority not in VALID_PRIORITIES:
        resp = _base_fail(
            "req_ticket",
            _error("INVALID_PARAM", "priority must be one of P0/P1/P2/P3", False, {"field": "priority"}),
        )
        _log_call("create_ticket", payload, resp)
        return resp

    if category not in VALID_CATEGORIES:
        resp = _base_fail(
            "req_ticket",
            _error("INVALID_PARAM", "category is invalid", False, {"field": "category"}),
        )
        _log_call("create_ticket", payload, resp)
        return resp

    if not isinstance(user_id, str) or not user_id.strip() or len(user_id.strip()) > 64:
        resp = _base_fail("req_ticket", _error("INVALID_PARAM", "user_id is required", False, {"field": "user_id"}))
        _log_call("create_ticket", payload, resp)
        return resp

    if order_id and (len(order_id.strip()) < 6 or len(order_id.strip()) > 64):
        resp = _base_fail(
            "req_ticket",
            _error("INVALID_PARAM", "order_id length must be 6-64", False, {"field": "order_id"}),
        )
        _log_call("create_ticket", payload, resp)
        return resp

    sla_map = {"P0": 2, "P1": 24, "P2": 48, "P3": 72}
    resp = _base_ok("req_ticket")
    resp["ticket"] = {
        "ticket_id": f"T{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "status": "OPEN",
        "sla_hours": sla_map[priority],
        "created_at": _now_iso(),
    }
    _log_call("create_ticket", payload, resp)
    return resp


def _demo() -> None:
    parser = argparse.ArgumentParser(description="Week2 mock tools demo")
    sub = parser.add_subparsers(dest="tool", required=True)

    p_kb = sub.add_parser("search_kb")
    p_kb.add_argument("query")
    p_kb.add_argument("--top_k", type=int, default=4)
    p_kb.add_argument("--domain", default="general")

    p_order = sub.add_parser("get_order_status")
    p_order.add_argument("order_id")
    p_order.add_argument("--phone_tail", default="")

    p_ticket = sub.add_parser("create_ticket")
    p_ticket.add_argument("title")
    p_ticket.add_argument("content")
    p_ticket.add_argument("priority")
    p_ticket.add_argument("user_id")
    p_ticket.add_argument("--category", default="other")
    p_ticket.add_argument("--order_id", default="")

    args = parser.parse_args()

    if args.tool == "search_kb":
        out = search_kb(query=args.query, top_k=args.top_k, domain=args.domain)
    elif args.tool == "get_order_status":
        out = get_order_status(order_id=args.order_id, phone_tail=args.phone_tail)
    else:
        out = create_ticket(
            title=args.title,
            content=args.content,
            priority=args.priority,
            user_id=args.user_id,
            category=args.category,
            order_id=args.order_id,
        )
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _demo()
