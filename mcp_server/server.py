# mcp_server/server.py

from fastapi import FastAPI
from pydantic import BaseModel

# 🔥 Import tools
from mcp_server.tool import rag_tool, weather_tool, web_tool


# -----------------------------
# CREATE FASTAPI APP (IMPORTANT)
# -----------------------------
app = FastAPI(title="MCP Server", version="1.0")


# -----------------------------
# REQUEST SCHEMA
# -----------------------------
class MCPRequest(BaseModel):
    tool: str
    input: str


# -----------------------------
# HEALTH CHECK (optional but useful)
# -----------------------------
@app.get("/")
def root():
    return {"message": "MCP Server is running 🚀"}


# -----------------------------
# MAIN MCP ENDPOINT
# -----------------------------
@app.post("/mcp")
def call_tool(req: MCPRequest):

    print(f"📩 Received request → Tool: {req.tool}")

    try:
        # -----------------------------
        # ROUTING
        # -----------------------------
        if req.tool == "rag":
            result = rag_tool(req.input)

        elif req.tool == "weather":
            result = weather_tool(req.input)

        elif req.tool == "web":
            result = web_tool(req.input)

        else:
            return {
                "output": "Unknown tool requested",
                "source": "system"
            }

        # -----------------------------
        # RESPONSE FORMAT (STANDARD MCP)
        # -----------------------------
        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }