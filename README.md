# 🤖 GitChat: AI-Driven Personal Knowledge Base

**GitChat** is a powerful, local knowledge base that allows you to "Chat with your GitHub Repositories." Leveraging Google's Gemini LLM, LangChain for RAG (Retrieval-Augmented Generation), and ChromaDB for local vector storage, GitChat provides an intelligent, context-aware interface to explore and understand any public codebase.

---

## 🚀 Features

- **Context-Aware Q&A**: Ask complex questions about any part of a repository and get answers backed by source code snippets.
- **Local Vector Store**: Uses ChromaDB to store code embeddings locally, ensuring speed and cost-effectiveness.
- **Multi-Language Support**: Supports Python, JavaScript, TypeScript, Go, C++, Java, and Markdown.
- **Artifact Preview**: Automatically displays the retrieved code blocks used to generate responses.
- **Dockerized Architecture**: Simplified deployment using Docker Compose.
- **Agentic Design**: Coordinates distinct agents for Data Ingestion, AI Orchestration, and Frontend UX.

---

## 🛠️ Tech Stack

- **Large Language Model**: [Google Gemini 1.5 Flash / 2.0 Flash](https://ai.google.dev/)
- **Orchestration**: [LangChain](https://www.langchain.com/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Embeddings**: `models/gemini-embedding-001`
- **Environment**: Docker & Docker Compose

---

## 📋 Architecture: Three-Agent Coordination

The system is designed around three specialized agents:

1.  **Agent 1 (Data Ingestion & Indexing)**:
    - Clones repositories from GitHub.
    - Loads and parses code files using `LanguageParser`.
    - Chunks code blocks and generates embeddings.
    - Persists data in a local ChromaDB collection named after the repository.
2.  **Agent 2 (AI Orchestration)**:
    - Initializes the RAG (Retrieval-Augmented Generation) chain.
    - Takes user queries and performs semantic search against ChromaDB.
    - Feeds retrieved context into Gemini for a precise answer.
3.  **Agent 3 (Frontend & UX)**:
    - Provides a modern Streamlit interface.
    - Manages repository selection and chat history.
    - Visualizes code artifacts in the chat window.

---

## 📦 Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose installed.
- A **Google AI Studio API Key**. Get one [here](https://aistudio.google.com/).

---

## ⚙️ Installation & Setup

1.  **Clone the project**:
    ```bash
    git clone <your-repository-url>
    cd AI-Driven-Personal-Knowledge-Base
    ```

2.  **Configure Environment Variables**:
    Create a `.env` file in the project root (or edit the existing one):
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    DB_PATH=./data/chroma_db
    REPO_TEMP_PATH=./data/temp_repos
    MODEL_NAME=gemini-flash-latest
    ```

3.  **Start the Services**:
    Run Docker Compose in detached mode:
    ```bash
    docker-compose up -d --build
    ```

---

## 📖 Usage Guide

1.  **Access the UI**: Navigate to `http://localhost:8502` in your browser.
2.  **Index a Repo**: Enter a public GitHub URL in the sidebar (e.g., `https://github.com/langchain-ai/langchain`).
3.  **Chat**: Once indexed, ask questions in the chat box:
    - *"How does the authentication module work?"*
    - *"Explain the database schema in this project."*
    - *"Where is the main entry point for the application?"*
4.  **View Sources**: Click on the **🔍 View Source Snippets** expander below any answer to see the exact code blocks used.

---

## 📂 Project Structure

```text
.
├── data/                   # Persistent storage (Git repos & Vector DB)
├── services/
│   ├── backend/            # Source logic (Ingestion & Orchestration)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── ingestion.py
│   │   └── orchestration.py
│   └── frontend/           # Streamlit application
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app.py
├── .env                    # Environment configuration
└── docker-compose.yml      # Service orchestration
```

---

## 🔧 Troubleshooting & Known Fixes

- **Port Conflicts**: By default, the frontend runs on port **8502** and the backend on **8001** to avoid common conflicts with other local services.
- **ImportErrors**: The backend logic is shared with the frontend container via volume mapping; ensure you use `docker-compose up --build` if you modify core logic.
- **Model Availability**: The system uses `models/gemini-flash-latest` and `models/gemini-embedding-001` for maximum compatibility with the Gemini free tier.

---

## 📄 License

This project is open-source and available under the MIT License.

---
*Created with 🤖 by Antigravity*
