from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
import os
import re

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192"
)

class Query(BaseModel):
    question: str
    excel_data: list
    tracked_changes: list = []

def clean_excel_data(excel_data):
    cleaned = []
    for row in excel_data:
        new_row = []
        for cell in row:
            val = cell.get("value", "")
            col = cell.get("color", None)
            new_row.append({
                "value": str(val).strip() if val else "",
                "color": col
            })
        cleaned.append(new_row)
    return cleaned

@app.post("/ask")
async def ask_question(query: Query):
    try:
        excel_data = clean_excel_data(query.excel_data)

        prompt = f"""
You are an Excel assistant bot. Based on the user's question, determine which schedule cells need to be updated or removed.

Only respond in this strict JSON format:

{{
  "summary": "short summary here",
  "updated_cells": [
    {{
      "row": "t1",
      "columns": ["B", "C"],         // columns to add yellow color
      "remove_columns": ["E", "F"]   // optional, columns to clear color
    }}
  ]
}}

- Match row values like "t1", "t2" from first column
- Columns are A, B, C, D...
- If user says "reduce", that means you remove from `remove_columns`
- Do not include anything except valid JSON

User Question:
{query.question}

Current Excel Color Data:
{json.dumps(excel_data)}

Detected Manual Changes:
{json.dumps(query.tracked_changes)}
"""

        llm_response = llm.invoke([HumanMessage(content=prompt)])
        content = llm_response.content.strip()

        # Fix malformed JSON manually
        try:
            if content.startswith("{"):
                response = json.loads(content)
            elif content.startswith("["):
                response = {
                    "summary": "Updates applied based on schedule.",
                    "updated_cells": json.loads(content)
                }
            else:
                # Try to extract first valid JSON object using regex
                json_block = re.search(r'\{[\s\S]+\}', content)
                if json_block:
                    response = json.loads(json_block.group(0))
                else:
                    return {
                        "error": "Failed to parse LLM response",
                        "raw": content
                    }

            return response

        except Exception as e:
            return {
                "error": "Failed to parse LLM response",
                "details": str(e),
                "raw": content
            }

    except Exception as e:
        return {
            "error": "Unhandled backend error",
            "details": str(e)
        }
