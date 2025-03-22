from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.preprocessing.preprocess2 import preprocess_repository
import json


def create_faiss_index(documents, embedding_model="text-embedding-ada-002"):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), model=embedding_model)
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

if __name__ == "__main__":
    
    with open('repo_data.json') as f:
        repo_data = json.load(f)

    docs = preprocess_repository(repo_data)
    create_faiss_index(docs)
    print(docs)
