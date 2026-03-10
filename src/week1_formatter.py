import argparse
import json
import re
from dataclasses import dataclass
from typing import Dict, List


INTENT_RULES: Dict[str, List[str]] = {
    "催单": ["催单", "催", "物流", "单号", "进度", "状态", "到哪", "还没到", "不到", "什么时候到", "一直不发货", "还没发货", "快递"],
    "退款": ["退款", "退钱", "申请退款", "申请退", "退货退款"],
    "改地址": ["改地址", "地址错", "换地址", "改收货地址"],
    "投诉": ["投诉", "差评", "态度差", "举报"],
    "咨询": ["怎么", "是否", "可以", "吗", "?", "？", "规则", "支持", "发票", "运费险", "活动"],
}


REQUIRED_INFO_BY_INTENT: Dict[str, List[str]] = {
    "催单": ["order_id"],
    "退款": ["order_id", "refund_reason"],
    "改地址": ["order_id", "new_address"],
    "投诉": ["issue_detail"],
    "咨询": [],
    "未知": [],
}


@dataclass
class StructuredOutput:
    intent: str
    entities: Dict[str, str]
    required_info: List[str]
    reply: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "intent": self.intent,
            "entities": self.entities,
            "required_info": self.required_info,
            "reply": self.reply,
        }


def detect_intent(text: str) -> str:
    lower = text.lower()
    ordered_intents = ["退款", "改地址", "投诉", "催单", "咨询"]
    for intent in ordered_intents:
        keywords = INTENT_RULES.get(intent, [])
        if any(k.lower() in lower for k in keywords):
            return intent
    return "未知"


def extract_entities(text: str) -> Dict[str, str]:
    entities: Dict[str, str] = {}

    # Simple order id pattern: letters/digits with at least 6 chars.
    match = re.search(r"(?<![A-Za-z0-9])([A-Za-z0-9]{6,})(?![A-Za-z0-9])", text)
    if match:
        entities["order_id"] = match.group(1)

    # Naive phone tail detection for customer service scenarios.
    phone_tail = re.search(r"(?:尾号|后四位)[^\d]*(\d{4})", text)
    if phone_tail:
        entities["phone_tail"] = phone_tail.group(1)

    return entities


def build_reply(intent: str, required_info: List[str]) -> str:
    if required_info:
        missing = "、".join(required_info)
        return f"为了继续处理你的问题，请先补充：{missing}。"

    if intent == "催单":
        return "我已理解你的催单诉求，正在为你查询订单最新状态。"
    if intent == "退款":
        return "我已收到退款诉求，正在核对订单和退款条件。"
    if intent == "改地址":
        return "我已收到改地址诉求，正在核验是否在可修改时效内。"
    if intent == "投诉":
        return "我已收到你的投诉，会立即记录并转交专人跟进。"
    if intent == "咨询":
        return "我已收到你的咨询，请稍等，我将根据规则给你明确答复。"
    return "我已收到你的问题。请补充订单号或更具体的诉求，便于我继续处理。"


def format_question(question: str) -> StructuredOutput:
    intent = detect_intent(question)
    entities = extract_entities(question)

    required_info = []
    for field in REQUIRED_INFO_BY_INTENT.get(intent, []):
        if field not in entities:
            required_info.append(field)

    reply = build_reply(intent=intent, required_info=required_info)
    return StructuredOutput(
        intent=intent,
        entities=entities,
        required_info=required_info,
        reply=reply,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Week1 formatter: convert user text into a structured customer-service JSON."
    )
    parser.add_argument("question", nargs="?", help="User input text")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    question = args.question or input("请输入用户问题: ").strip()
    if not question:
        raise SystemExit("问题不能为空。")

    result = format_question(question).to_dict()
    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()




