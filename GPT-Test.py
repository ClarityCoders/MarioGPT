import os
from openai import OpenAI
import base64

MODEL="gpt-4o"

APIKEY = os.getenv('API_KEY')
client = OpenAI(api_key=APIKEY)

IMAGE_PATH = ".\images\\test_striker.png"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
base64_image = encode_image(IMAGE_PATH)

completion = client.chat.completions.create(
    model=MODEL,
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": 
         """
Prentend your playing the game pick your next move.
JSON Format:
move: A dictionary specifying which buttons to press. 
Keys must include "left", "right", and "shoot", 
with boolean values (true/false).

thoughts: A comical explanation of why you are making that move."""},
        {"role": "user", "content": [
            {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
            ]}
    ]
)

print(base64_image)
print(completion.choices[0].message.content)
print(completion.usage)