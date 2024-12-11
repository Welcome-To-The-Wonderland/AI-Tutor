from openai import OpenAI
import base64
import json
import os
from urllib.parse import urlparse


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def process_response(response):
    json_string = response.choices[0].message.content
    json_string = json_string.replace("'''json\n", "").replace("\n'''", "")
    json_data = json.loads(json_string)

    filename_without_extension = os.path.splitext(
        os.path.basename(image_local))[0]
    json_filename = f"{filename_without_extension}.json"
    with open("./Data" + json_filename, "w") as file:
        json.dump(json_data, file, indent=4)
    print(f"JSON Data saved to {json_filename}")


def main():
    image_local = 'label.png'
    base64_img = f"data:image/png;base64,{encode_image(image_local)}"
    client = OpenAI(api_key="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")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user",
             "content":  [
                 {"type": "text", "text": "A student is working on a quiz about PC parts. Briefly describe the images, describe what options they clicked or didn't click. Describe what the right answer should be."},
                 {
                     "type": "image_url",
                     "image_url": {"url": f"{base64_img}"}
                 }
             ],
             }
        ],
        max_tokens=800,
    )

    print(response)


main()
