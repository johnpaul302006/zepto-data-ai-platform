from fastapi import FastAPI

try:
    from .graph import graph
    from .schemas import SupportRequest, SupportResponse
except ImportError:
    from graph import graph
    from schemas import SupportRequest, SupportResponse


app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline RAG support assistant using LangGraph and ChromaDB.",
    version="1.0.0",
)


@app.get("/")
def root() -> dict:
    return {
        "service": "Zepto Support Assistant",
        "status": "running",
    }


@app.post("/ask", response_model=SupportResponse)
def ask(request: SupportRequest) -> SupportResponse:
    result = graph.invoke(
        {
            "query": request.query,
        }
    )

    retrieved = result.get("retrieved", [])

    sources = [
        item["id"]
        for item in retrieved
    ]

    return SupportResponse(
        answer=result.get("answer", ""),
        sources=sources,
        confidence=1.0,
    )