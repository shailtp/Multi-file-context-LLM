import json
import re
from typing import Dict, List

class PromptGenerator:
    """
    A class to generate user prompts by extracting relevant method details 
    from a centralized JSON file containing details of multiple Python files.
    """

    def __init__(self, json_file: str):
        """
        Initializes the PromptGenerator with the centralized JSON file.

        Args:
            json_file (str): Path to the JSON file containing function/method details.
        """
        self.json_file = json_file
        self.method_data = self._load_json()

    def _load_json(self) -> List[Dict]:
        """
        Loads the centralized JSON file.

        Returns:
            List[Dict]: A list of dictionaries containing function/method details.
        """
        try:
            with open(self.json_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {self.json_file}")

    def _find_method_docstring(self, class_name: str, method_name: str) -> str:
        """
        Finds the docstring for a specific method from the centralized JSON data.

        Args:
            class_name (str): Name of the class.
            method_name (str): Name of the method.

        Returns:
            str: The docstring of the method, or a message if the method is not found.
        """
        for method in self.method_data:
            if method["class_name"] == class_name and method["function_name"] == method_name:
                return method["docstring"]
        return f"Docstring for {class_name}.{method_name} not found."

    def _find_class_docstring(self, class_name: str) -> str:
        """
        Finds the `__init__` method's docstring for a class.

        Args:
            class_name (str): Name of the class.

        Returns:
            str: The docstring of the `__init__` method or a message if not found.
        """
        return self._find_method_docstring(class_name, "__init__")

    def generate_prompt(self, user_prompt: str) -> str:
        """
        Parses the user prompt, fetches relevant method details, and generates the final prompt.

        Args:
            user_prompt (str): The user-provided input prompt.

        Returns:
            str: The final prompt to send to the LLM.
        """
        # Static system prompt
        system_prompt = (
            "You are a smart Software Developer who handles large-scale Machine Learning Projects. "
            "Your task is to help the user by writing or improving code based on their input. "
            "You have access to all relevant class and method details."
        )

        # Extract references to methods and classes using regex
        method_matches = re.findall(r'"(\w+)" method of the "(\w+)" class', user_prompt)
        class_matches = re.findall(r'"(\w+)" class', user_prompt)
        method_details = []

        # Fetch docstrings for specific methods, including __init__ by default
        for method_name, class_name in method_matches:
            # Fetch the __init__ docstring
            init_docstring = self._find_class_docstring(class_name)
            # Fetch the specific method's docstring
            method_docstring = self._find_method_docstring(class_name, method_name)

            # Append both docstrings to the details
            method_details.append(f"**{class_name}.__init__**:\n{init_docstring}")
            method_details.append(f"**{class_name}.{method_name}**:\n{method_docstring}")

        # Fetch docstrings for classes (default to __init__)
        for class_name in class_matches:
            if not any(class_name == m[1] for m in method_matches):  # Avoid duplicates
                docstring = self._find_class_docstring(class_name)
                method_details.append(f"**{class_name}.__init__**:\n{docstring}")

        # Construct the final prompt
        final_prompt = f"{system_prompt}\n\nThe user requested the following:\n\n{user_prompt}\n\nRelevant Method Details:\n"
        final_prompt += "\n".join(method_details) if method_details else "No relevant method details found."

        return final_prompt
