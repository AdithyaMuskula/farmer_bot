# mcp_server/tool.py

import sys
import os

# Ensure project root is on the path so rag_loader can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_loader import hybrid_search
from agents.weather_agent import weather_agent
from agents.external_agent import external_agent


# -----------------------------
# RAG TOOL (HYBRID)
# -----------------------------
def rag_tool(query: str):

    print("RAG tool called")

    try:
        docs = hybrid_search(query)
    except Exception as e:
        return {
            "output": f"RAG error: {str(e)}",
            "source": "rag"
        }

    if not docs:
        return {
            "output": "No relevant agricultural data found.",
            "source": "rag"
        }

    # Clean + limit content
    context = "\n\n".join([d.page_content[:300] for d in docs])

    return {
        "output": context,
        "source": "rag"
    }


# -----------------------------
# WEATHER TOOL
# -----------------------------
def weather_tool(query: str):

    print("Weather tool called")

    try:
        result = weather_agent(query)
    except Exception as e:
        return {
            "output": f"Weather error: {str(e)}",
            "source": "weather"
        }

    return {
        "output": result,
        "source": "weather"
    }


# -----------------------------
# WEB TOOL (DuckDuckGo)
# -----------------------------
def web_tool(query: str):

    print("Web tool called")

    try:
        result = external_agent(query)
    except Exception as e:
        return {
            "output": f"Web error: {str(e)}",
            "source": "web"
        }

    return {
        "output": result,
        "source": "web"
    }