from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from graph.state import RouterOutput, AgentState
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0,          # very low temperature for accurate routing
)

# Structured output
structured_llm = llm.with_structured_output(RouterOutput)

ROUTER_PROMPT = """You are a skill router for a multi-skill AI agent.

Available skills:
1. summarizer → when the user wants a summary / short version of a text
2. translator → when the user wants to translate text from one language to another
3. calculator → when the user asks a mathematical calculation or expression
4. general_chat → for greetings, small talk, general questions, or anything else

Rules:
- select 0, 1, or maximum 2 skills.
- If the prompt needs two skills (example: "summarize this and translate to English"), return both.
- If the prompt is ambiguous or does not clearly match any skill → return empty list [].
- Always respond with the exact skill names: summarizer, translator, calculator, general_chat
- Support both English and Persian (Farsi) prompts equally well.

User prompt:
{user_input}
"""

prompt = ChatPromptTemplate.from_template(ROUTER_PROMPT)

def router_node(state: AgentState) -> AgentState:
    """Routing node: detects which skill(s) are needed"""
    
    chain = prompt | structured_llm
    result: RouterOutput = chain.invoke({"user_input": state["user_input"]})
    
    print(f"\n[Router] Detected skills: {result.skills}")
    print(f"[Router] Reasoning: {result.reasoning}")
    
    return {
        **state,
        "detected_skills": result.skills,
        "reasoning": result.reasoning,
        "skill_results": {},
    }