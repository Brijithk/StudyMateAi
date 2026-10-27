import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-5.5")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found in .env")

try:
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        instructions="You are StudyMate AI, a helpful Python tutor.",
        input="Explain Python functions in two simple sentences.",
        max_output_tokens=150,
    )

    print("OpenAI API connection successful!")
    print("Model:", model)
    print("\nResponse:")
    print(response.output_text)

except Exception as error:
    print("OpenAI API request failed.")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))