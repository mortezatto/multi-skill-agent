from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.router import router_node
from graph.nodes import (
    summarizer_node,
    translator_node,
    calculator_node,
    general_chat_node,
    combine_results_node,
)

def create_agent():
    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("router", router_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("translator", translator_node)
    workflow.add_node("calculator", calculator_node)
    workflow.add_node("general_chat", general_chat_node)
    workflow.add_node("combine", combine_results_node)

    # Entry point
    workflow.set_entry_point("router")

    # After router: go to first skill (or fallback)
    def route_after_router(state: AgentState):
        skills = state.get("detected_skills", [])
        
        if not skills:
            return "general_chat"  
        
        return skills[0]

    workflow.add_conditional_edges(
        "router",
        route_after_router,
        {
            "summarizer": "summarizer",
            "translator": "translator",
            "calculator": "calculator",
            "general_chat": "general_chat",
        }
    )

    # After any skill: decide next step
    def after_skill(state: AgentState):
        skills = state.get("detected_skills", [])
        results = state.get("skill_results", {})
        
        # How many skills have already run?
        already_done = len(results)
        
        if already_done >= len(skills) or already_done >= 2:
            return "combine"
        
        # Run the next skill
        next_skill = skills[already_done]
        return next_skill

    for skill in ["summarizer", "translator", "calculator", "general_chat"]:
        workflow.add_conditional_edges(
            skill,
            after_skill,
            {
                "summarizer": "summarizer",
                "translator": "translator",
                "calculator": "calculator",
                "general_chat": "general_chat",
                "combine": "combine",
            }
        )

    # After combine: finish
    workflow.add_edge("combine", END)

    return workflow.compile()