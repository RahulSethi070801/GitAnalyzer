import tiktoken
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
import json

# Map file extensions to LangChain Language enums
LANGUAGE_SPLITTER_MAP = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".cpp": Language.CPP,
    ".java": Language.JAVA,
    ".php": Language.PHP,
    ".go": Language.GO,
    ".rst": Language.RST,
    ".scala": Language.SCALA,
    ".swift": Language.SWIFT,
    ".md": Language.MARKDOWN,
    ".tex": Language.LATEX,
    ".html": Language.HTML,
    ".sol": Language.SOL,
    ".proto": Language.PROTO,
}

# Token-based chunking for unsupported file types
def chunk_by_tokens(encoded_tokens, chunk_size, overlap_size):
    chunks = []
    start_idx = 0
    while start_idx < len(encoded_tokens):
        end_idx = start_idx + chunk_size
        chunk = encoded_tokens[start_idx:end_idx]
        chunks.append(chunk)
        start_idx += chunk_size - overlap_size
    return chunks

# Main preprocessing function
def preprocess_repository(repo_data, chunk_size=500, overlap_size=50, model_name="gpt-3.5-turbo"):
    processed_docs = []
    encoding = tiktoken.encoding_for_model(model_name)

    for file_info in repo_data["files"]:
        file_path = file_info["file_path"]
        content = file_info["content"]
        file_extension = "." + file_path.split(".")[-1]

        if file_extension in LANGUAGE_SPLITTER_MAP:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=LANGUAGE_SPLITTER_MAP[file_extension],
                chunk_size=chunk_size,
                chunk_overlap=overlap_size,
            )
            docs = splitter.create_documents([content], metadatas=[{"source": file_path}])
        else:
            # Token-based chunking for unknown file types
            encoded_content = encoding.encode(content)
            token_chunks = chunk_by_tokens(encoded_content, chunk_size, overlap_size)
            docs = [
                Document(
                    page_content=encoding.decode(chunk),
                    metadata={"source": file_path}
                )
                for chunk in token_chunks
            ]

        processed_docs.extend(docs)

    # Add repo structure as context
    structure_content = "\n".join([f["file_path"] for f in repo_data["files"]])
    structure_doc = Document(
        page_content=structure_content,
        metadata={"source": f"{repo_data['repo_name']}_folder_structure"}
    )
    processed_docs.append(structure_doc)

    return processed_docs

# Example Usage:
if __name__ == "__main__":
    # sample_repo_data = {
    #     "repo_name": "example_repo",
    #     "files": [
    #         {
    #             "file_path": "src/main.py",
    #             "content": "# Example Python\nprint('Hello, World!')"
    #         },
    #         {
    #             "file_path": "README.md",
    #             "content": "# Example Repo\nThis repo demonstrates preprocessing."
    #         }
    #     ]
    # }
    
    with open('/Users/rahul/Desktop/MCS/Spring25/CS410/Project/GitAnalyzer/repo_data.json', 'r') as file:
        sample_repo_data = json.load(file)

    docs = preprocess_repository(sample_repo_data)
    for doc in docs:
        print(f"Source: {doc.metadata['source']}\nContent: {doc.page_content}\n{'-'*50}\n")
