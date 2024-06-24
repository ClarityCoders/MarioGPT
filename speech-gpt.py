from pathlib import Path
from openai import OpenAI
import os
from utils.directory import create_directory

APIKEY = os.getenv('API_KEY')
client = OpenAI(api_key=APIKEY)

# Let's store in speech folder.
# Check to see if it exists first.
create_directory("speech")
file_name = input("What would you like to call your file? ")

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="onyx",
    input="""Clarity Coders!""",
) as response:
    response.stream_to_file(f".\speech\{file_name}.mp3")