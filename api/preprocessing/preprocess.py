import ast
from langchain.schema import Document

def extract_functions_ast(code):
    parsed = ast.parse(code)
    functions = [node for node in parsed.body if isinstance(node, ast.FunctionDef)]
    function_strings = []
    for func in functions:
        func_str = ast.get_source_segment(code, func)
        function_strings.append(func_str.strip())
    return function_strings

def create_function_chunks(functions, functions_per_chunk=2):
    chunks = []
    for i in range(len(functions) - functions_per_chunk + 1):
        chunk = "\n\n".join(functions[i:i + functions_per_chunk])
        chunks.append(chunk)
    return chunks

def preprocess_code_file(content, file_path, functions_per_chunk=2):
    docs = []
    functions = extract_functions_ast(content)
    if len(functions) < functions_per_chunk:
        docs.append(Document(page_content=content, metadata={"source": file_path, "note": "less than 2 functions"}))
        return docs

    chunks = create_function_chunks(functions, functions_per_chunk)
    for idx, chunk in enumerate(chunks):
        docs.append(Document(
            page_content=chunk,
            metadata={"source": file_path, "chunk_number": idx}
        ))
    return docs

# Example Usage:
if __name__ == "__main__":
    sample_code = '''
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b
'''

    docs = preprocess_code_file(sample_code, "src/utils.py")
    for doc in docs:
        print(f"Chunk {doc.metadata.get('chunk_number', 'N/A')} from {doc.metadata['source']}:\n{doc.page_content}\n{'-'*50}")
