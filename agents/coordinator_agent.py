from langgraph.graph import StateGraph, END
from typing import TypedDict
from groq import Groq
import os
import base64

from agents.external_agent import external_agent
from agents.weather_agent import weather_agent

from dotenv import load_dotenv
load_dotenv()


# -----------------------------
# GROQ CLIENT (VISION)
# -----------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY_1"))


# -----------------------------
# STATE
# -----------------------------
class AgentState(TypedDict):
    question: str
    answer: str
    image: bytes


# -----------------------------
# ROUTER
# -----------------------------
def router(state):

    question = state["question"].lower()

    # WEATHER related
    if any(word in question for word in [
        "weather", "rain", "temperature", "humidity",
        "wind", "forecast", "climate",
        "spray today", "can i spray", "should i spray",
        "good day to spray", "is it good to spray"
    ]):
        return {"next": "weather"}

    # LLM knowledge questions
    if any(word in question for word in [
        "what is", "why", "cause", "benefit",
        "how does", "explain", "reason"
    ]):
        return {"next": "llm"}

    # RAG knowledge base
    if any(word in question for word in [
        "fertilizer", "disease", "pest", "treatment",
        "fungicide", "insecticide", "crop disease",
        "yellow leaves", "leaf spots"
    ]):
        return {"next": "rag"}

    # Default → external web knowledge
    return {"next": "external"}

# -----------------------------
# VISION NODE
# -----------------------------
def vision_node(state):

    print("Vision node called")

    # If no image uploaded → skip vision
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

Identify crop disease or visible issue if present.
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
# LLM NODE
# -----------------------------
def llm_node(state: AgentState):

    print("LLM node called")

    response = llm.invoke(state["question"])

    return {
        "answer": response.content
    }


# -----------------------------
# RAG NODE
# -----------------------------
def rag_node(state: AgentState):

    print("RAG node called")

    docs = retriever.invoke(state["question"])

    context = "\n".join([d.page_content for d in docs])

    response = llm.invoke(
        f"""
Context:
{context}

Question:
{state['question']}

Give farmer-friendly advice.
"""
    )

    return {
        "answer": response.content
    }


# -----------------------------
# WEATHER NODE
# -----------------------------
def weather_node(state: AgentState):

    print("Weather node called")

    result = weather_agent(state["question"])

    return {
        "answer": result
    }


# -----------------------------
# EXTERNAL NODE
# -----------------------------
def external_node(state: AgentState):

    print("External node called")

    result = external_agent(state["question"], llm)

    return {
        "answer": result
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
    workflow.add_node("router", router)
    workflow.add_node("llm", llm_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("weather", weather_node)
    workflow.add_node("external", external_node)

    # Entry point
    workflow.set_entry_point("vision")

    # Vision → Router
    workflow.add_edge("vision", "router")

    # Router logic
    workflow.add_conditional_edges(
        "router",
        lambda x: x["next"],
        {
            "llm": "llm",
            "rag": "rag",
            "weather": "weather",
            "external": "external"
        }
    )

    # End edges
    workflow.add_edge("llm", END)
    workflow.add_edge("rag", END)
    workflow.add_edge("weather", END)
    workflow.add_edge("external", END)

    graph = workflow.compile()

    return graph