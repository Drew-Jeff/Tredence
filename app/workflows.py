from .engine import WorkflowEngine
from .tools import registry

# --- Node Functions ---

def node_extract(state):
    code = state.get("code", "")
    funcs = registry.get_tool("extract_functions")(code)
    state["functions"] = funcs
    print(f"Extracted {len(funcs)} functions.")
    return state

def node_analyze(state):
    # Analyze complexity of the first function found
    funcs = state.get("functions", [])
    if funcs:
        score = registry.get_tool("calculate_complexity")(funcs[0])
        state["complexity_score"] = score
    else:
        state["complexity_score"] = 0
    return state

def node_improve(state):
    # Mock improvement: add comments to lower "perceived" complexity or fix issues
    state["code"] = "# Reviewed\n" + state["code"]
    # Artificially lower complexity to simulate improvement so loop ends
    state["complexity_score"] = max(0, state["complexity_score"] - 5)
    print("Applied improvements to code.")
    return state

def node_check_quality(state):
    # Condition function: Returns True if quality is good enough
    threshold = state.get("threshold", 10)
    current = state.get("complexity_score", 100)
    return current <= threshold

# --- Graph Assembly ---

def build_code_review_graph():
    workflow = WorkflowEngine()
    
    # Register Nodes
    workflow.add_node("extract", node_extract)
    workflow.add_node("analyze", node_analyze)
    workflow.add_node("improve", node_improve)
    
    # Define Flow
    workflow.set_entry_point("extract")
    
    # extract -> analyze
    workflow.add_edge("extract", "analyze")
    
    # analyze -> (Conditional) -> END or improve
    # If complexity is LOW (True), we are done.
    # If complexity is HIGH (False), we go to improve.
    workflow.add_conditional_edge(
        "analyze", 
        node_check_quality, 
        routes={True: None, False: "improve"} # None means Stop
    )
    
    # improve -> extract (Loop back to start to re-evaluate)
    workflow.add_edge("improve", "extract")
    
    return workflow

# Global instance
code_review_workflow = build_code_review_graph()