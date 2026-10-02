from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from graph.state import AgentState
from prompts.prompts import SUMMARIZER_PROMPT, TRANSLATOR_PROMPT, GENERAL_CHAT_PROMPT
import os
from dotenv import load_dotenv
import re
import math

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)

# ---------- Calculator Tool (real computation) ----------
def safe_calculate(expression: str) -> str:
    """Safely evaluate math expressions, including natural language like 'square root of 144'"""
    
    expr = expression.lower().strip()
    
    # Handle "square root of X" or "sqrt of X" or "√X"
    match = re.search(r'(?:square root of|sqrt of|√)\s*([\d\.]+)', expr)
    if match:
        number = match.group(1)
        try:
            return str(math.sqrt(float(number)))
        except:
            return "Error calculating square root"
    
    # Handle simple power: "X to the power of Y" or "X squared"
    match = re.search(r'([\d\.]+)\s*(?:to the power of|power)\s*([\d\.]+)', expr)
    if match:
        base, exp = match.groups()
        try:
            return str(float(base) ** float(exp))
        except:
            return "Error calculating power"
    
    if "squared" in expr:
        match = re.search(r'([\d\.]+)\s*squared', expr)
        if match:
            try:
                return str(float(match.group(1)) ** 2)
            except:
                return "Error calculating square"
    
    # Normal math expression cleaning
    expr = expr.replace("x", "*").replace("×", "*").replace("÷", "/")
    expr = re.sub(r'[^0-9+\-*/().%\s]', '', expr)  # keep only valid math characters
    
    if not expr.strip():
        return "Could not find a valid math expression"
    
    try:
        allowed = {
            "abs": abs, "round": round, "min": min, "max": max,
            "pow": pow, "sqrt": math.sqrt,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "pi": math.pi, "e": math.e
        }
        result = eval(expr, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"




# ---------- Skill Nodes ----------

def summarizer_node(state: AgentState) -> AgentState:
    print("[Skill] Running Summarizer...")
    prompt = ChatPromptTemplate.from_template(SUMMARIZER_PROMPT)
    chain = prompt | llm
    result = chain.invoke({"text": state["user_input"]})
    
    return {
        **state,
        "skill_results": {
            **state.get("skill_results", {}),
            "summarizer": result.content
        }
    }


def translator_node(state: AgentState) -> AgentState:
    print("[Skill] Running Translator...")
    prompt = ChatPromptTemplate.from_template(TRANSLATOR_PROMPT)
    chain = prompt | llm
    result = chain.invoke({"text": state["user_input"]})
    
    return {
        **state,
        "skill_results": {
            **state.get("skill_results", {}),
            "translator": result.content
        }
    }


def calculator_node(state: AgentState) -> AgentState:
    print("[Skill] Running Calculator...")
    
    result = safe_calculate(state["user_input"])
    
    return {
        **state,
        "skill_results": {
            **state.get("skill_results", {}),
            "calculator": f"Result: {result}"
        }
    }

def general_chat_node(state: AgentState) -> AgentState:
    print("[Skill] Running General Chat...")
    prompt = ChatPromptTemplate.from_template(GENERAL_CHAT_PROMPT)
    chain = prompt | llm
    result = chain.invoke({"text": state["user_input"]})
    
    return {
        **state,
        "skill_results": {
            **state.get("skill_results", {}),
            "general_chat": result.content
        }
    }


def combine_results_node(state: AgentState) -> AgentState:
    """Combine results from one or two skills into final response"""
    results = state.get("skill_results", {})
    
    if not results:
        final = "I couldn't understand your request. Can you please rephrase it?"
    elif len(results) == 1:
        final = list(results.values())[0]
    else:
        # Two skills
        parts = []
        for skill, content in results.items():
            parts.append(f"**{skill.capitalize()}**:\n{content}")
        final = "\n\n".join(parts)
    
    return {
        **state,
        "final_response": final
    }