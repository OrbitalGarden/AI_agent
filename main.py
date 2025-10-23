import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from available_functions import available_functions
from functions.call_function import call_function

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if len(args) < 1:
        print("AI agent usage: python3 main.py 'prompt' [--verbose]")
        sys.exit(1)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    If the output of the prompt would be an error, wait 1 second and try again no more than 10 times.
    \n means that you should add a line break insted of writing \n
    """

    user_prompt = " ".join(args)
    verbose = True if "--verbose" in sys.argv else False
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages, 
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
            ),
    )

    if response.function_calls != []:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if function_call_result.parts[0].function_response.response and verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            if not hasattr(function_call_result.parts[0].function_response, "response"):
                raise SystemExit
    else:
        print(response.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
