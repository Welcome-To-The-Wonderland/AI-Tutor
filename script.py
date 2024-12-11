import requests
import json

# Define the API endpoint and payload
api_url = "http://127.0.0.1:8000/api/completion/"
payload = {
    "user": "test@example.com",  # Replace with an actual user email if needed
    "status": "All questions answered",
    "modules": [
        {
            "module": 1,
            "title": "Functionality",
            "questions": [
                {
                    "activity": "Functionality",
                    "type": "multipleChoice",
                    "question": "Which component acts as the brain of the computer, processing all the instructions?",
                    "options": ["CPU", "GPU", "RAM", "SSD"],
                    "hint": "Think of the part responsible for carrying out commands and calculations.",
                    "answer": "CPU",
                    "attempts": 1,
                    "Previous_tries": ["CPU"],
                    "answer_status": "Answered"
                }
            ]
        }
    ]
}

# Send the POST request
try:
    response = requests.post(api_url, json=payload)
    response.raise_for_status()  # Raise an error for non-2xx HTTP status codes

    # Print the response
    print("Status Code:", response.status_code)
    print("Response JSON:", json.dumps(response.json(), indent=4))

except requests.exceptions.RequestException as e:
    print("Error:", e)
