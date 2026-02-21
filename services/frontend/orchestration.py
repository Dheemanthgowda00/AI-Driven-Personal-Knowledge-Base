from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_retrieval_chain(collection_name):
    """Initializes the RAG chain for a specific repository collection."""
    # Setup LLM
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
        temperature=0.2,
    )

    # Load Vector DB
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db_path = os.getenv("DB_PATH", "./data/chroma_db")
    vector_db = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings,
        collection_name=collection_name
    )

    # Retrieval setup
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})

    # Prompt Template
    system_prompt = (
        "You are an expert software engineer. "
        "Use the following snippets of retrieved code to answer the user's question about the repository. "
        "If you don't know the answer, say that you don't know. "
        "Keep the answer concise and professional."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Create Chains
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

def ask_question(chain, question):
    """Processes a question through the RAG chain."""
    response = chain.invoke({"input": question})
    return {
        "answer": response["answer"],
        "context": [doc.page_content for doc in response["context"]]
    }
