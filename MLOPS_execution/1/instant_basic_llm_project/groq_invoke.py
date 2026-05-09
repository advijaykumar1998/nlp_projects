from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

class GroqLLM:
    def __init__(self, model="qwen/qwen3-32b", temperature=0.5):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.temperature = temperature

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    llm = GroqLLM()
    prompt = "Explain the theory of relativity in simple terms."
    response = llm.invoke(prompt)
    print("Response from Groq LLM:")
    print(response)