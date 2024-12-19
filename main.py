import os
from groq import Groq, AsyncGroq
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Union

app = FastAPI()
load_dotenv()

#Open data
with open('./data/handbook.json', 'r') as file:
    handbook_data = json.load(file)
with open('./data/tutorresources.json', 'r') as file:
    tutor_resources_data = json.load(file);

client = AsyncGroq(
    api_key=os.getenv("GROQ_API_KEY"),
)


class Item(BaseModel):
    message : str


@app.post("/process-message")
async def read_item(message: Item):

    try:

        response = await call_Groq(message.message)
        return response

    except Exception as e:
        print("Read Item Exception")
        raise HTTPException(status_code = 500, detail = f"Error in processing query {e}")


# @cached(ttl = 3600)
async def call_Groq(query : str) -> str:
    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{handbook_data} {tutor_resources_data} Your are a helpful assistant answering questions based off the data given",
                },
                {
                    "role": "system",
                    "content": f"Provide links as much as possible",
                },
                {
                    "role":"system",
                    "content" : "Always provide the CONNECT_ME_HANDBOOK link if necessary to answer the prompt"
                },
                {
                    "role": "system",
                    "content": "Keep the response under 2000 characters"
                },
                {
                    "role": "user",
                    "content": f"{query}",
                },
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("GROQ EXCEPTION")
        raise HTTPException(status_code = 500, detail = f"Error in Groq call {e}")
        # return "Please wait for a moment before sending another prompt"
    