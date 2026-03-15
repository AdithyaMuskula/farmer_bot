from langchain_community.document_loaders import WebBaseLoader


def external_agent(query: str, llm):

    print("External agent called")

    urls = [
        "https://www.fao.org/home/en",
        "https://www.icar.org.in/",
    ]

    docs = []

    for url in urls:
        loader = WebBaseLoader(url)
        docs.extend(loader.load())

    if not docs:
        return "No external data found."

    content = docs[0].page_content[:2000]

    # LLM Summarization
    prompt = f"""
Summarize the following farming information for a farmer.

Farmer question:
{query}

Information:
{content}

Give a short, clear farming answer.
"""

    response = llm.invoke(prompt)

    return response.content