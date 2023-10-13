from fastapi import FastAPI
from pydantic import BaseModel
from storyline import get_output
from generate_images import generate_list_of_images
from create_video import generate_full_video

app = FastAPI()

class Prompt(BaseModel):
    text: str

@app.post("/generate/")
async def generate_response(prompt: Prompt):
    get_storyline = get_output(prompt.text)
    
    scenes = ["this is a cat", "this is a dog"]
    image_prompts = ["this is a photo of a  cat", "this is a photo of a dog"]


    image_links=generate_list_of_images(image_prompts)
    generate_full_video(image_links, scenes)