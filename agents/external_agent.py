from langchain_community.tools import DuckDuckGoSearchRun


# Initialize search tool
search = DuckDuckGoSearchRun()


def external_agent(query: str, llm):

    print("External agent (Web Search) called")

    # -----------------------------
    # 🔍 STEP 1: SEARCH WEB
    # -----------------------------
    try:
        search_results = search.run(query)
    except Exception as e:
        return f"Web search failed: {str(e)}"

    if not search_results:
        return "No web data found."

    # Limit content size (important)
    content = search_results[:2000]

    # -----------------------------
    # 🔥 STEP 2: DYNAMIC PROMPT (NO FIXED FORMAT)
    # -----------------------------
    q = query.lower()

    if any(word in q for word in ["price", "rate", "cost", "market"]):

        prompt = f"""
You are an agriculture expert.

Give the latest price clearly.

Question:
{query}

Web Data:
{content}

Rules:
- Give direct answer
- Mention price range if available
- Keep it short
- No Cause/Solution format
"""

    else:

        prompt = f"""
You are an agriculture expert.

Answer clearly using the web information.

Question:
{query}

Web Data:
{content}

Rules:
- Be accurate and concise
- Use only relevant information
- Do NOT include thinking
"""

    # -----------------------------
    # 🤖 STEP 3: LLM RESPONSE
    # -----------------------------
    response = llm.invoke(prompt)

    answer = response.content.split("</think>")[-1].strip()

    return answer