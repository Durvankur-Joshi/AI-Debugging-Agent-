from fastapi import APIRouter
from pydantic import BaseModel
from app.graph.workflow import build_graph
from app.agents.error_analyzer import analyze_error

router = APIRouter()

# Build graph once
graph = build_graph(analyze_error)


class DebugRequest(BaseModel):
    error: str
    code: str


@router.post("/debug")
def debug_error(request: DebugRequest):
    try:
        result = graph.invoke({
            "error": request.error,
            "code": request.code
        })

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }