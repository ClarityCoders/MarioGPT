from openai import OpenAI
import base64
import os

def get_message(IMAGE_PATH, PROMPT, last_move):
    MODEL="gpt-4o"
    APIKEY = os.getenv('API_KEY')
    client = OpenAI(api_key=APIKEY)

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    base64_image = encode_image(IMAGE_PATH)

    completion = client.chat.completions.create(
        model=MODEL,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": 
            PROMPT},
            {"role": "system", "content": 
            f"Your move last time was: {last_move} Below are the previous image then the current image"},
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

    # print(completion.choices[0].message.content)
    # print(completion.usage)
    return completion.choices[0].message.content