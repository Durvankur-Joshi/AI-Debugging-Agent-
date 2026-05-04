from typing import TypedDict
from langgraph.graph import StateGraph

from app.agents.fix_generator import generate_fix
from app.agents.retriever import retrieve_context
from app.utils.parser import clean_json_response


# ✅ Graph State
class DebugState(TypedDict):
    error: str
    code: str
    project_id: str
    context: str
    analysis: dict
    fix: dict


def build_graph(analyze_fn):

    graph = StateGraph(DebugState)

    # ==========================================
    # 🔹 RETRIEVER NODE
    # ==========================================
    def retriever_node(state: DebugState):

        error = state.get("error", "")
        code = state.get("code", "")
        project_id = state.get("project_id", "")

        context = retrieve_context(
            error,
            code,
            project_id
        )

        print("Retrieved Context:", context)

        return {
            **state,
            "context": context
        }

    # ==========================================
    # 🔹 ANALYZE NODE
    # ==========================================
    def analyze_node(state: DebugState):

        print("Incoming State:", state)

        error = state.get("error", "")
        code = state.get("code", "")
        context = state.get("context", "")

        if not error or not code:
            return {
                **state,
                "analysis": {
                    "error": "Error or code not provided properly."
                }
            }

        result = analyze_fn(
            error,
            code,
            context
        )

        if hasattr(result, "content"):
            analysis_text = result.content
        else:
            analysis_text = str(result)

        parsed_analysis = clean_json_response(analysis_text)

        return {
            **state,
            "analysis": parsed_analysis
        }

    # ==========================================
    # 🔹 FIX NODE
    # ==========================================
    def fix_node(state: DebugState):

        print("Fix Node State:", state)

        error = state.get("error", "")
        code = state.get("code", "")
        analysis = state.get("analysis", {})

        if not analysis:
            return {
                **state,
                "fix": {
                    "error": "No analysis available."
                }
            }

        result = generate_fix(
            error,
            code,
            analysis
        )

        if hasattr(result, "content"):
            fix_text = result.content
        else:
            fix_text = str(result)

        parsed_fix = clean_json_response(fix_text)

        return {
            **state,
            "fix": parsed_fix
        }

    # ==========================================
    # 🔹 GRAPH NODES
    # ==========================================
    graph.add_node("retrieve", retriever_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("fix", fix_node)

    # ==========================================
    # 🔹 GRAPH FLOW
    # ==========================================
    graph.set_entry_point("retrieve")

    graph.add_edge("retrieve", "analyze")
    graph.add_edge("analyze", "fix")

    # ==========================================
    return graph.compile()