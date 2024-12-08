# **Context Retention System**

## **Overview**
This project is a comprehensive system designed to aid software developers in generating and debugging code efficiently using context retention and AI-driven language models. The system integrates capabilities such as extracting function/method details, refining user prompts, and interacting with large language models (LLMs) through Groq's API.

---

## **Key Features**

### 1. **Centralized Data Extraction**
- Scrapes function and method details such as:
  - **Input/Output Parameters**
  - **Docstrings**
  - **Dependencies**
  - **File Paths**
- All extracted details are stored in a centralized JSON file for efficient access and future usage.

### 2. **User-Defined Prompts**
- Allows users to define an **initial prompt** that specifies:
  - **Objective**: The task or goal the user wants to achieve.
  - **Dependencies**: Relevant methods or functions, mentioned in double quotes (e.g., `"generate"` method of `"GenerateGoal"` class).

### 3. **Prompt Refinement**
- The initial prompt is processed by the `PromptGenerator` class, which:
  - Adds detailed information about the methods/functions referenced in the user’s prompt (e.g., docstrings, parameter details).
  - Refines the prompt to provide complete context for the LLM.

### 4. **LLM Interaction via Groq**
- The refined prompt is passed to the `call_llm` method, which interacts with Groq's API to query openly available LLMs.
- Supported models can be found on [Groq's Model Page](https://console.groq.com/models).

### 5. **End-to-End Flow**
- The entire process, from prompt creation to result inspection, is demonstrated in the `exp.ipynb` notebook.
- Users can test the system end-to-end and verify results.

---

## **Folder Structure**
- function_extrcator_v2.py  # Script for extracting function/method details
- prompt_generator.py       # Class to refine user-defined prompts
- call_llm.py               # Function to interact with LLM via Groq
- exp.ipynb                 # End-to-end example notebook
- README.md                 # Project documentation
- requirements.txt          # Dependencies
