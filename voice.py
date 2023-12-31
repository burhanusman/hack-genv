
import requests
from fastapi.responses import Response
from fastapi import  HTTPException

def convert_text_to_speech(text):

    XI_API_KEY = "53d136eb2f65ca3c72f1ceb9ede669af"  # Replace with your actual API key
    VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Replace with your desired voice ID

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": XI_API_KEY
    }
    elevenlabs_data = {
      "text": text,
      "model_id": "eleven_monolingual_v1",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }
    try:
        response = requests.post(url, json=elevenlabs_data, headers=headers)
        if response.status_code == 200:
            return response
            return Response(content=response.content, media_type="audio/mpeg")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Call the FastAPI endpoint
    # response = requests.post("http://localhost:8000/text_to_speech/", json=text_data)   