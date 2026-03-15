🌾 Farmer Bot AI

Farmer Bot AI is an intelligent assistant designed to help farmers by providing information about weather, crop diseases, fertilizers, and farming practices. The system uses Natural Language Processing (NLP), Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG) to answer agricultural questions in real time.

The goal of this project is to support farmers with AI-driven recommendations that improve productivity and decision-making.

🚜 Features

🌦️ Weather Information – Provides weather updates for farming decisions

🌱 Crop Disease Detection Support – Gives guidance on common crop diseases

🧪 Fertilizer Recommendations – Suggests suitable fertilizers for crops

📚 Agriculture Knowledge Base (RAG) – Retrieves farming information from documents

🤖 LLM-based Question Answering – Answers general agriculture-related questions

🔀 Smart Query Routing – Routes queries to the appropriate module (Weather / RAG / LLM)

🧠 System Architecture

The system uses a router-based architecture:

User asks a question

Router identifies the type of query

Query is sent to the appropriate module:

Weather API

RAG Knowledge Base

LLM

Example routing logic:

def router(state):

    question = state["question"].lower()

    if "weather" in question or "rain" in question or "temperature" in question:
        return {"next": "weather"}

    if "cause" in question or "benefit" in question or "what is" in question:
        return {"next": "llm"}

    if "fertilizer" in question or "disease" in question:
        return {"next": "rag"}
🛠️ Tech Stack

Python

LangChain

LLMs (OpenAI / Hugging Face models)

Vector Databases

RAG (Retrieval-Augmented Generation)

Weather API

FastAPI / CLI Interface

📂 Project Structure
farmer-bot-ai/
│
├── router.py           # Query routing logic
├── weather.py          # Weather API integration
├── rag_pipeline.py     # RAG knowledge retrieval
├── llm_module.py       # LLM response generation
├── data/               # Agricultural knowledge base
├── app.py              # Main application
└── requirements.txt
⚙️ Installation

Clone the repository

git clone https://github.com/your-username/farmer-bot-ai.git

Move into the project folder

cd farmer-bot-ai

Install dependencies

pip install -r requirements.txt
▶️ Running the Project
python app.py

Then ask questions like:

What fertilizer is best for rice?

What causes leaf blight in crops?

Will it rain tomorrow?

📊 Example Queries
User Question	System Module
What is nitrogen fertilizer?	LLM
What fertilizer is good for wheat?	RAG
Will it rain today?	Weather
🎯 Future Improvements

Crop yield prediction using ML models

Voice-based farmer assistant

Mobile application integration

Multilingual support for farmers

Image-based crop disease detection
