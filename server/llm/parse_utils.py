import re


def extract_python_code(llm_output):
    """
    Extracts Python code from an LLM output.

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


def extract_name_and_description(llm_output):
    """
    Extracts JSON from an LLM output and returns a dictionary with name, description,
    input_json_schema, and output_json_schema.

    Args:
    llm_output (str): The output from the LLM containing the JSON.

    Returns:
    dict: A dictionary with 'name', 'description', 'input_json_schema', and 'output_json_schema' keys,
          or None if no JSON is found or parsing fails.
    """
    # Pattern to match JSON block
    pattern = r"```json\n(.*?)```"

    # Use re.DOTALL flag to match across multiple lines
    match = re.search(pattern, llm_output, re.DOTALL)

    if match:
        # Extract the content inside the JSON block
        json_str = match.group(1).strip()
        # Parse the JSON string into a Python dictionary
        import json

        try:
            json_dict = json.loads(json_str)
            # Return a dictionary with all required fields
            return {
                "name": json_dict.get("name"),
                "description": json_dict.get("description"),
                "input_json_schema": json_dict.get("input_json_schema"),
                "output_json_schema": json_dict.get("output_json_schema"),
            }
        except json.JSONDecodeError:
            # Return None if JSON parsing fails
            return None
    else:
        # Return None if no JSON block is found
        return None
