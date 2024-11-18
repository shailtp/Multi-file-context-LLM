from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_context_db"]

# MongoDB Collections
functions_collection = db["functions"]
files_collection = db["code_files"]

def get_function_details(function_name):
    """
    Retrieve the file name and metadata for a specific function in the database.
    
    Parameters:
    function_name (str): The name of the function to search for.

    Returns:
    dict: A dictionary containing function details, file metadata, or a message if not found.
    """
    # Query the functions collection for the specified function name
    function = functions_collection.find_one({"function_name": function_name})
    
    if not function:
        return {"error": f"Function '{function_name}' not found in the database."}

    # Query the files collection for the file where the function is located
    file_id = function.get("file_id")
    file_data = files_collection.find_one({"_id": file_id})

    if not file_data:
        return {"error": f"File associated with function '{function_name}' not found."}

    # Return function details and file metadata
    return {
        "function_name": function_name,
        "file_name": file_data.get("file_name"),
        "file_path": file_data.get("file_path"),
        "start_line": function.get("start_line"),
        "end_line": function.get("end_line"),
        "called_functions": function.get("called_functions", []),
    }

if __name__ == "__main__":
    # Example usage
    func_name = input("Enter the function name you want to search for: ")
    details = get_function_details(func_name)
    print(details)
