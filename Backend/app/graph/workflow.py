from typing import TypedDict
from langgraph.graph import StateGraph
from app.agents.fix_generator import generate_fix
from app.utils.parser import clean_json_response
from app.agents.retriever import retrieve_context

class DebugState(TypedDict):
    error: str
    code: str
    context : str
    analysis: str
    fix: str


def build_graph(analyze_fn):

    graph = StateGraph(DebugState)

    # 🔹 Analyze Node
    def analyze_node(state: DebugState):
        print("Incoming State:", state)
        
        context = state.get("context", "")
        error = state.get("error", "")
        code = state.get("code", "")

        if not error or not code:
            return {
                "error": error,
                "code": code,
                "analysis": "Error or code not provided properly.",
                "fix": ""
            }

        result = analyze_fn(error, code , context)

        if hasattr(result, "content"):
            analysis_text = result.content
        else:
            parsed_fix = clean_json_response(result)

        return {
            "error": error,
            "code": code,
            "analysis": parsed_fix,
            "fix": ""
        }
        
        print("CONTEXT:", context)
        

    # 🔹 Fix Node
    def fix_node(state: DebugState):
        print("Fix Node State:", state)

        error = state.get("error", "")
        code = state.get("code", "")
        analysis = state.get("analysis", "")

        if not analysis:
            return {
                **state,
                "fix": "No analysis available to generate fix."
            }

        result = generate_fix(error, code, analysis)

        if hasattr(result, "content"):
            fix_text = result.content
        else:
            parsed_fix = clean_json_response(result)

        return {
            **state,
            "fix": parsed_fix
        }
        
    def retriever_node(state : DebugState):
        error = state.get("error" , "")
        
        context = retrieve_context(error , code)
        
        return {
            **state,
            "context": context
        }
        


    # Add nodes
    graph.add_node("analyze", analyze_node)
    graph.add_node("fix", fix_node)
    graph.add_node("retrieve" , retriever_node)

    # Flow
    graph.set_entry_point("retrieve")
    
    graph.add_edge("retrieve", "analyze")
    graph.add_edge("analyze", "fix")

    return graph.compile()