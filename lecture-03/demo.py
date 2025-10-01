import ollama

def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers
    
    Args:
      a: The first integer number
      b: The second integer number
    
    Returns:
      int: The sum of the two numbers
    """
    return a + b


response = ollama.chat(
  'llama3.1',
  messages=[{'role': 'user', 'content': 'What is 10 + 10?'}],
  tools=[add_two_numbers], # Actual function reference
)

available_functions = {
  'add_two_numbers': add_two_numbers,
}

for tool in response.message.tool_calls or []:
    function_to_call = available_functions.get(tool.function.name)
    if function_to_call:
        print('Function output:', function_to_call(**tool.function.arguments))
    else:
        print('Function not found:', tool.function.name)
