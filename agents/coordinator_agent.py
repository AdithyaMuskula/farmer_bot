from langgraph.graph import StateGraph, END
from typing import TypedDict
from groq import Groq
import os
import base64
import requests

from agents.external_agent import external_agent
from agents.weather_agent import weather_agent

from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# IMPORTS
# -----------------------------

# -----------------------------
# LOAD BM25 code in notepad past if it is not working
# -----------------------------


# -----------------------------
# GROQ CLIENT (VISION)
# -----------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY_1"))

# -----------------------------
# MCP CLIENT (IMPORTANT 🔥)
# -----------------------------
def call_mcp(tool, query):
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001")
    try:
        res = requests.post(
            f"{mcp_url}/mcp",
            json={
                "tool": tool,
                "input": query
            }
        )

        return res.json()["data"]["output"]

    except Exception as e:
        return f"MCP error: {str(e)}"


# -----------------------------
# STATE
# -----------------------------
class AgentState(TypedDict, total=False):
    question: str
    answer: str
    image: bytes
    plan: str
    combined: str


# -----------------------------
# VISION NODE
# -----------------------------
def vision_node(state):

    print("Vision node called")

    # If no image → skip
    if "image" not in state or state["image"] is None:
        return state

    image_bytes = state["image"]
    encoded_image = base64.b64encode(image_bytes).decode()

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
Analyze this crop image.

User question:
{state['question']}

Identify crop disease or visible issue.
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    vision_result = response.choices[0].message.content

    return {
        "question": state["question"] + "\nImage analysis: " + vision_result
    }


# -----------------------------
# PLANNER NODE
# -----------------------------
def planner_node(state):

    print("Planner node called")

    question = state["question"].lower()

    prompt = f"""
You are an AI planner.

Select ONLY the necessary tools.

Available tools:
- rag → for agriculture knowledge (diseases, pests, fertilizers)
- weather → ONLY if question depends on weather (rain, spray timing)
- external → ONLY for latest info (prices, news, market)

STRICT RULES:
- Do NOT select all tools
- Be minimal
- Choose only what is needed

Examples:

Q: Which insects are controlled by stomach poisons?
A: rag

Q: Can I spray pesticide today?
A: rag, weather

Q: Wheat price today?
A: external

Q: What is photosynthesis?
A: rag

Now answer:

Question: {question}
"""

    response = llm.invoke(prompt)

    raw_plan = response.content.lower().strip()
    print("LLM plan:", raw_plan)

    # -----------------------------
    # 🔥 RULE-BASED CORRECTION
    # -----------------------------
    plan = []

    # WEATHER intent
    if any(word in question for word in [
        "weather", "rain", "temperature", "spray", "today"
    ]):
        plan.append("weather")

    # EXTERNAL intent
    if any(word in question for word in [
        "price", "rate", "market","sell", "buy"
    ]):
        plan.append("external")

    # RAG intent (default for knowledge)
    if any(word in question for word in [
        "disease", "leaf", "yellow", "pest", "fertilizer", "crop"
    ]) or not plan:
        plan.append("rag")

    # remove duplicates
    plan = list(set(plan))

    print("Final plan:", plan)

    return {
        "question": question,
        "plan": ",".join(plan)
    }


# ----------------------------- 
# EXECUTION NODE()
# -----------------------------
def execution_node(state):

    print("Execution node called")

    plan = state["plan"]
    question = state["question"]

    results = []

    # -----------------------------
    # RAG via MCP
    # -----------------------------
    if "rag" in plan:
        print("→ Using RAG (MCP)")
        results.append("RAG:\n" + call_mcp("rag", question))

    # -----------------------------
    # WEATHER via MCP
    # -----------------------------
    if "weather" in plan:
        print("→ Using Weather (MCP)")
        results.append("Weather:\n" + call_mcp("weather", question))

    # -----------------------------
    # EXTERNAL via MCP
    # -----------------------------
    if "external" in plan:
        print("→ Using External (MCP)")
        results.append("External:\n" + call_mcp("web", question))

    return {
        "question": question,
        "combined": "\n\n".join(results)
    }

    # -----------------------------
    # EXTERNAL
    # -----------------------------
    if "external" in plan:
        print("→ Using External")
        results.append("External:\n" + external_agent(question, llm))

    return {
        "question": question,
        "combined": "\n\n".join(results)
    }



# -----------------------------
# FINAL NODE
# -----------------------------
def final_node(state):

    print("Final node called")

    question = state["question"]
    data = state["combined"]

    q = question.lower()

    # -----------------------------
    # 🔥 CHECK IF CONTEXT IS WEAK
    # -----------------------------
    use_context = True

    if not data or len(data.strip()) < 50:
        print("⚠️ Weak context → using LLM knowledge")
        use_context = False

    # -----------------------------
    # 🔥 DETECT QUESTION TYPE
    # -----------------------------
    if any(word in q for word in ["price", "rate", "cost", "market"]):
        mode = "price"

    elif "what is" in q or "define" in q:
        mode = "definition"

    elif "what happens" in q or "symptom" in q:
        mode = "effect"

    else:
        mode = "problem"

    print("Detected mode:", mode)

    # -----------------------------
    # 🔥 SELECT PROMPT
    # -----------------------------
    if mode == "price":

        base_prompt = f"""
You are an agriculture expert.

Give the latest price clearly.

Question:
{question}

Data:
{data if use_context else "Use your general knowledge"}

Rules:
- Give direct price answer
- Mention range if needed
- Keep it short
- No extra sections
"""

    elif mode == "definition":

        base_prompt = f"""
You are an agriculture expert.

Answer clearly.

If the given data is not useful, use your own knowledge.

Question:
{question}

Data:
{data if use_context else "Use your general knowledge"}

Rules:
- Keep it short
- No unnecessary sections
"""

    elif mode == "effect":

        base_prompt = f"""
You are an agriculture expert.

Explain what happens (symptoms/effects).

Question:
{question}

Data:
{data if use_context else "Use your general knowledge"}
"""

    else:  # problem

        base_prompt = f"""
You are an agriculture expert.

Answer ONLY in this format:

Cause:
Solution:
Fertilizer:

Question:
{question}

Data:
{data if use_context else "Use your general knowledge"}

Rules:
- Be practical
- Do NOT mix crops
"""

    # -----------------------------
    # 🔁 AGENTIC LOOP
    # -----------------------------
    max_iter = 2
    answer = ""

    for i in range(max_iter):

        print(f"Iteration {i+1}")

        response = llm.invoke(base_prompt)
        answer = response.content.split("</think>")[-1].strip()

        # -----------------------------
        # ✅ CHECKPOINT
        # -----------------------------
        if len(answer) > 40 and "not sure" not in answer.lower():
            print("✅ Good answer")
            break

        print("🔁 Refining answer...")
        base_prompt += "\nImprove clarity and correctness."

    return {
        "answer": answer
    }


# -----------------------------
# CREATE GRAPH
# -----------------------------
def create_coordinator_agent(llm_model, retriever_model):

    global llm
    global retriever

    llm = llm_model
    retriever = retriever_model

    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("vision", vision_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("execution", execution_node)
    workflow.add_node("final", final_node)

    # Entry
    workflow.set_entry_point("vision")

    # Flow
    workflow.add_edge("vision", "planner")
    workflow.add_edge("planner", "execution")
    workflow.add_edge("execution", "final")
    workflow.add_edge("final", END)

    graph = workflow.compile()

    return graph