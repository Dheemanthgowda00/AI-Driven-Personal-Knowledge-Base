import os
import shutil
from git import Repo
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def clone_repo(repo_url, target_path):
    """Clones a git repository to a target path."""
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    Repo.clone_from(repo_url, to_path=target_path)
    print(f"Cloned {repo_url} to {target_path}")

def index_repository(repo_path, collection_name):
    """Loads, splits, and indexes repository content in ChromaDB."""
    # Load code files
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".py", ".js", ".ts", ".go", ".cpp", ".c", ".java", ".md"],
        parser=LanguageParser()
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")

    # Split documents
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(docs)
    print(f"Split into {len(texts)} chunks")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Store in ChromaDB
    db_path = os.getenv("DB_PATH", "./data/chroma_db")
    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=db_path,
        collection_name=collection_name
    )
    print(f"Indexed repository into ChromaDB at {db_path}")
    return vector_db

if __name__ == "__main__":
    pass
