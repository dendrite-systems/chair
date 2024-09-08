import re


def extract_python_code(llm_output):
    """
    Extracts Python code from an LLM output that contains the CODE_PROMPT.

    Args:
    llm_output (str): The output from the LLM containing the Python code.

    Returns:
    str: The extracted Python code, or None if no code is found.
    """
    # Pattern to match Python code block
    pattern = r"```python\n(.*?)```"

    # Use re.DOTALL flag to match across multiple lines
    match = re.search(pattern, llm_output, re.DOTALL)

    if match:
        # Return the content inside the Python code block
        return match.group(1).strip()
    else:
        # Return None if no Python code block is found
        return None
