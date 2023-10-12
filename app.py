from fastapi import FastAPI
from pydantic import BaseModel
from storyline import get_output

app = FastAPI()

class Prompt(BaseModel):
    text: str

@app.post("/generate/")
async def generate_response(prompt: Prompt):
    response = get_output(prompt.text)
    return {"response": response}