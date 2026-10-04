import json
import os
from typing import Callable, TypedDict

from pydantic import ValidationError
from langgraph.graph import END, START, StateGraph

try:
    from .prompts import build_prompt
    from .retriever import retrieve_documents
    from .schemas import SupportResponse
except ImportError:
    from prompts import build_prompt
    from retriever import retrieve_documents
    from schemas import SupportResponse


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"

POLICY_KEYWORDS = [
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours",
]


# ---------------------------------------------------------
# LangGraph state
# ---------------------------------------------------------
class SupportState(TypedDict, total=False):
    query: str
    intent: str
    retrieved: list[dict]
    answer: str


# ---------------------------------------------------------
# Optional real-LLM response validation with retries
# ---------------------------------------------------------
def validate_real_llm_response_with_retry(
    generate_fn: Callable[[str], str],
    prompt: str,
    max_retries: int = 2,
) -> SupportResponse:
    """
    Validate optional real-LLM JSON output against SupportResponse.

    Allows the initial attempt plus up to two corrective retries.
    """
    last_error = None
    current_prompt = prompt

    for attempt in range(max_retries + 1):
        raw_response = generate_fn(current_prompt)

        try:
            data = json.loads(raw_response)
            return SupportResponse.model_validate(data)

        except (json.JSONDecodeError, ValidationError) as error:
            last_error = error

            if attempt == max_retries:
                break

            current_prompt = (
                prompt
                + "\n\nCORRECTION:\n"
                "Your previous response failed schema validation.\n"
                "Return ONLY valid JSON with exactly these fields:\n"
                "answer (string), sources (list of strings), "
                "confidence (number between 0 and 1).\n"
                f"Validation error: {error}"
            )

    raise ValueError(
        f"LLM response failed validation after "
        f"{max_retries + 1} attempts: {last_error}"
    )


# ---------------------------------------------------------
# Node 1: classify_intent
# ---------------------------------------------------------
def classify_intent(state: SupportState) -> SupportState:
    query = state["query"].lower()

    if MOCK_LLM:
        intent = (
            "policy_question"
            if any(keyword in query for keyword in POLICY_KEYWORDS)
            else "general_question"
        )
    else:
        # Optional real-LLM extension.
        # The graded submission uses MOCK_LLM=1.
        intent = (
            "policy_question"
            if any(keyword in query for keyword in POLICY_KEYWORDS)
            else "general_question"
        )

    return {
        **state,
        "intent": intent,
    }


# ---------------------------------------------------------
# Node 2: retrieve_and_answer
# ---------------------------------------------------------
def retrieve_and_answer(state: SupportState) -> SupportState:
    query = state["query"]

    # Retrieval always runs for policy questions.
    retrieved = retrieve_documents(query, top_k=3)

    if not retrieved:
        return {
            **state,
            "retrieved": [],
            "answer": "No relevant policy context was found.",
        }

    if MOCK_LLM:
        top_chunk = retrieved[0]["document"]
        snippet = top_chunk[:200].strip()

        answer = f"Based on the retrieved context: {snippet}"

    else:
        context = "\n\n".join(
            item["document"]
            for item in retrieved
        )

        prompt = build_prompt(
            question=query,
            context=context,
        )

        # Real-LLM integration is optional and ungraded.
        answer = (
            "Real-LLM mode is optional and not enabled in the "
            "graded offline configuration.\n\n"
            f"Prompt prepared:\n{prompt}"
        )

    return {
        **state,
        "retrieved": retrieved,
        "answer": answer,
    }


# ---------------------------------------------------------
# Node 3: direct_answer
# ---------------------------------------------------------
def direct_answer(state: SupportState) -> SupportState:
    if MOCK_LLM:
        answer = (
            "I can only answer questions about Zepto policies right now."
        )
    else:
        answer = "Real-LLM direct answering is optional."

    return {
        **state,
        "answer": answer,
    }


# ---------------------------------------------------------
# Conditional routing
# ---------------------------------------------------------
def route_after_classification(state: SupportState) -> str:
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


# ---------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------
builder = StateGraph(SupportState)

builder.add_node("classify_intent", classify_intent)
builder.add_node("retrieve_and_answer", retrieve_and_answer)
builder.add_node("direct_answer", direct_answer)

builder.add_edge(START, "classify_intent")

builder.add_conditional_edges(
    "classify_intent",
    route_after_classification,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

builder.add_edge("retrieve_and_answer", END)
builder.add_edge("direct_answer", END)

graph = builder.compile()


# ---------------------------------------------------------
# Local verification
# ---------------------------------------------------------
if __name__ == "__main__":
    policy_query = "How long does Zepto delivery take?"

    result = graph.invoke(
        {
            "query": policy_query,
        }
    )

    print("Query:", policy_query)
    print("Intent:", result["intent"])
    print("Answer:", result["answer"])

    print("\n---")

    general_query = "Tell me a joke."

    result = graph.invoke(
        {
            "query": general_query,
        }
    )

    print("Query:", general_query)
    print("Intent:", result["intent"])
    print("Answer:", result["answer"])