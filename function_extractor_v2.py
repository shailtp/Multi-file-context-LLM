import ast
import json
from typing import List, Dict

class MultiFileFunctionExtractor:
    """
    A class to parse multiple Python files and extract details of functions/methods,
    including their file name, class name, parameters, docstrings, return types, and dependencies.
    """

    def __init__(self, file_paths: List[str], output_file: str) -> None:
        """
        Initializes the MultiFileFunctionExtractor with file paths and output file name.

        Args:
            file_paths (List[str]): List of paths to Python files to parse.
            output_file (str): Path to the output JSON file to save the extracted details.
        """
        self.file_paths = file_paths
        self.output_file = output_file
        self.function_details = []

    def extract(self) -> None:
        """
        Extracts details of all functions/methods from the specified files
        and saves them to the output JSON file.
        """
        for file_path in self.file_paths:
            self._process_file(file_path)

        self._save_to_json()

    def _process_file(self, file_path: str) -> None:
        """
        Parses a single file and extracts details of all functions/methods.

        Args:
            file_path (str): Path to the Python file to parse.
        """
        try:
            with open(file_path, "r") as file:
                source_code = file.read()

            tree = ast.parse(source_code)
            current_class_name = "Global"  # Tracks the current class context

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):  # If the node is a class definition
                    current_class_name = node.name
                    for sub_node in node.body:
                        if isinstance(sub_node, ast.FunctionDef):  # Methods within the class
                            self.function_details.append(
                                self._extract_function_details(sub_node, current_class_name, file_path)
                            )
                elif isinstance(node, ast.FunctionDef) and current_class_name == "Global":
                    # Global functions
                    self.function_details.append(
                        self._extract_function_details(node, "Global", file_path)
                    )
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    @staticmethod
    def _extract_function_details(node: ast.FunctionDef, class_name: str, file_path: str) -> Dict:
        """
        Extracts details for a single function/method.

        Args:
            node (ast.FunctionDef): The AST node representing the function/method.
            class_name (str): The name of the class containing this method, or "Global" for standalone functions.
            file_path (str): The file name where the function/method is defined.

        Returns:
            Dict: A dictionary containing function/method details.
        """
        func_name = node.name
        parameters = [arg.arg for arg in node.args.args]
        return_type = ast.unparse(node.returns) if node.returns else "None"
        docstring = ast.get_docstring(node) or ""

        # Extract function/method calls (dependencies)
        dependencies = []
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Call):
                if isinstance(sub_node.func, ast.Name):
                    dependencies.append(sub_node.func.id)  # Function call (e.g., foo())
                elif isinstance(sub_node.func, ast.Attribute):
                    dependencies.append(sub_node.func.attr)  # Method call (e.g., obj.bar())

        return {
            "file_name": file_path,
            "class_name": class_name,
            "function_name": func_name,
            "parameters": parameters,
            "return_type": return_type,
            "docstring": docstring,
            "dependencies": dependencies,
        }

    def _save_to_json(self) -> None:
        """
        Saves the extracted function details to the output JSON file.
        """
        with open(self.output_file, "w") as json_file:
            json.dump(self.function_details, json_file, indent=4)
        print(f"Function details saved to {self.output_file}")
