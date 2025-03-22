from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

def retrieve_documents(query, top_k=5, embedding_model="text-embedding-ada-002"):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), model=embedding_model)
    vectorstore = FAISS.load_local("faiss_index", embeddings)
    docs = vectorstore.similarity_search(query, k=top_k)
    return docs

if __name__ == "__main__":
    query = "How to print Hello World in Python?"
    retrieved_docs = retrieve_documents(query)
    for doc in retrieved_docs:
        print(f"Source: {doc.metadata['source']}\n{doc.page_content}\n{'-'*40}")
