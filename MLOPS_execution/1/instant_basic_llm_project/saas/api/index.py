from fastapi import FastAPI  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

class GroqLLM:
    def __init__(self, model="mixtral-8x7b-32768", temperature=0.7):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.temperature = temperature

    def stream_invoke(self, prompt: str):
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"

@app.get("/")
def idea():
    client = GroqLLM()
    prompt = "Come up with a new business idea for AI Agents. Format with headings, sub-headings and bullet points."
    return StreamingResponse(client.stream_invoke(prompt), media_type="text/event-stream")