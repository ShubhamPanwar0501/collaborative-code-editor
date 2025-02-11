import openai

openai.api_key = "your-openai-api-key-here"

def get_ai_suggestions(code: str):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use Codex or another model here
        prompt=f"Please debug the following Python code:\n{code}",
        max_tokens=150
    )
    return response.choices[0].text.strip()
