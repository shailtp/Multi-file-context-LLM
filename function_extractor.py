import os
import ast
import base64
from pymongo import MongoClient
from datetime import datetime

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_context_db"]

# MongoDB Collections
users_collection = db["users"]
files_collection = db["code_files"]
functions_collection = db["functions"]

def extract_functions(file_path):
    """
    Extract function names, start and end lines, and called functions from a Python file.
    """
    with open(file_path, "r") as f:
        content = f.read()
    tree = ast.parse(content)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            called_functions = [
                n.func.id if isinstance(n.func, ast.Name) else None
                for n in ast.walk(node)
                if isinstance(n, ast.Call)
            ]
            functions.append({
                "function_name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                "called_functions": list(filter(None, called_functions)),
            })
    return functions

def store_file_and_functions(user_id, file_path):
    """
    Store file content and extracted functions in MongoDB.
    """
    # Encode file content
    with open(file_path, "r") as f:
        content = f.read()
    encoded_content = base64.b64encode(content.encode()).decode()

    # Insert file metadata
    file_data = {
        "user_id": user_id,
        "file_name": os.path.basename(file_path),
        "file_path": file_path,
        "content": encoded_content,
        "last_modified": datetime.now().isoformat()
    }
    file_id = files_collection.insert_one(file_data).inserted_id

    # Extract and store functions
    functions = extract_functions(file_path)
    for func in functions:
        func["file_id"] = file_id
        func["called_functions"] = [
            {"function_name": cf, "file_id": None} for cf in func["called_functions"]
        ]
        functions_collection.insert_one(func)

if __name__ == "__main__":
    # Example user ID
    user_id = users_collection.insert_one({
        "name": "Test User",
        "email": "testuser@example.com",
        "date_created": datetime.now().isoformat()
    }).inserted_id

    # Specify the Python file to extract functions from
    python_file_path = "example.py"  # Replace with the path to your Python file
    store_file_and_functions(user_id, python_file_path)
    print("File and functions stored successfully!")
