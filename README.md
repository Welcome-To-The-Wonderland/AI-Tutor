
# django-nextjs-jwt-starter

  

A sample setup integrating Django REST Framework, React/NextJS, and JWT Authentication for your development needs.

  

## Demo

#### Main

![demo-1](https://res.cloudinary.com/dotera808/image/upload/v1724405550/Demo-1_tbvd6a.gif)

  #### Admin
![demo-2](https://res.cloudinary.com/dotera808/image/upload/v1724405550/Demo-2_keiyxj.gif)
  

## Setup

  

Clone the repo

  

```

$ git clone https://github.com/kalvincalimag/django-nextjs-jwt-starter.git

```

  

### Setup Backend (Django)

  
  
  

First, create a `.env` file in the root of the backend folder & add your Django secret key:

```

DJ_SECRET_KEY=<your_django_secret_key_here>

```

For generating a key, refer [here](https://www.makeuseof.com/django-secret-key-generate-new/).
  

Enter Directory

```

cd backend

```

  

Install dependencies:

```

pip install -r requirements.txt

```

  

Set up the database:

```

python manage.py makemigrations

python manage.py migrate

```

  

Run server:

```

python manage.py runserver

```

  

### Setup Frontend (NextJS)

  

Enter directory

  

```

$ cd frontend

```

  

Install dependencies

  

```

npm install

```

  

Run the app

  

```

npm run dev

```

  

## Contact

  

### Let's connect

  

- Twitter [@kalvincalimag_](https://twitter.com/kalvincalimag_)

  

### If you find this project helpful, please consider giving it a ⭐.

  

[⭐](https://github.com/kalvincalimag/django-nextjs-jwt-starter) this repo or follow me on:

  

- Github [@kalvincalimag](https://github.com/kalvincalimag)

- Medium [@kalvincalimag](https://medium.com/@kalvincalimag)

  

## License

  

[BSD](LICENSE.md) @kalvincalimag

[
    {
        "module": 1,
        "title": "Functionality",
        "questions": [
            {
                "activity": "Functionality",
                "type": "multipleChoice",
                "question": "Which component acts as the brain of the computer, processing all the instructions?",
                "options": [
                    "CPU",
                    "GPU",
                    "RAM",
                    "SSD"
                ],
                "hint": "Think of the part responsible for carrying out commands and calculations.",
                "answer": "CPU",
                "thread_id": "thread_4vXcU0fmNobsFt0tbM5NgWnc",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 1,
                "attempts": 1,
                "Previous_tries": [
                    "CPU"
                ],
                "answer_status": "Answered"
            },
            {
                "activity": "Functionality",
                "type": "multipleChoice",
                "question": "Which storage type is generally faster and more durable?",
                "options": [
                    "SSD",
                    "HDD",
                    "RAM",
                    "DVD"
                ],
                "hint": "This type has no moving parts.",
                "answer": "SSD",
                "thread_id": "thread_rqCd7YNNv6fT4LPmzCJK5tH1",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 1,
                "attempts": 1,
                "Previous_tries": [
                    "SSD"
                ],
                "answer_status": "Answered"
            },
            {
                "activity": "Functionality",
                "type": "fillInBlank",
                "question": "The ___ temporarily stores data for quick access while the computer is running.",
                "hint": "This memory is volatile and resets when the computer is turned off.",
                "answer": "ram",
                "thread_id": "thread_IN7pnITeVKe8Ea13YZVRySf4",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 1,
                "attempts": 1,
                "Previous_tries": [
                    "ram"
                ],
                "answer_status": "Answered"
            },
            {
                "activity": "Functionality",
                "type": "trueFalse",
                "question": "RAM is used for long-term data storage.",
                "options": [
                    "True",
                    "False"
                ],
                "hint": "Think about the purpose of RAM in relation to data storage.",
                "answer": false,
                "thread_id": "thread_TTQOylvfrAozfClY3RIlUSsy",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 1,
                "attempts": 1,
                "Previous_tries": [
                    "false"
                ],
                "answer_status": "Answered"
            },
            {
                "activity": "Functionality",
                "type": "fillInBlank",
                "question": "To check CPU compatibility with a motherboard, you must ensure the CPU socket type is the same as the motherboard ___.",
                "hint": "This part of the CPU must match the motherboard socket.",
                "answer": "brand",
                "thread_id": "thread_hsrAoNw8Lp0NxotRcNAU0nLN",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 1,
                "attempts": 1,
                "Previous_tries": [
                    "brand"
                ],
                "answer_status": "Answered"
            }
        ]
    },
    {
        "module": 2,
        "title": "Identification",
        "questions": [
            {
                "activity": "Identification",
                "type": "dragAndDrop",
                "question": "Match components with images.",
                "images": [
                    {
                        "component": "cpu",
                        "image": "/cpu.jpg"
                    },
                    {
                        "component": "gpu",
                        "image": "/gpu.jpg"
                    },
                    {
                        "component": "ram",
                        "image": "/ram.jpg"
                    },
                    {
                        "component": "ssd",
                        "image": "/ssd.jpg"
                    }
                ],
                "labels": [
                    "CPU",
                    "GPU",
                    "RAM",
                    "SSD"
                ],
                "hint": "Match each label with the correct image based on component function.",
                "answer": {
                    "cpu": "CPU",
                    "gpu": "GPU",
                    "ram": "RAM",
                    "ssd": "SSD"
                },
                "thread_id": "thread_PYp1udM0H9E9kd6tpLAatpaE",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 2,
                "attempts": 2,
                "Previous_tries": [
                    {
                        "cpu": "CPU",
                        "gpu": "GPU",
                        "ram": "RAM",
                        "ssd": "SSD"
                    }
                ],
                "answer_status": "Answered",
                "image": ""
            },
            {
                "activity": "Identification",
                "type": "componentMatch",
                "question": "Which component plugs into the motherboard shown in the center image?",
                "centerImage": "/memquestion.jpg",
                "options": [
                    {
                        "label": "RAM",
                        "image": "/ram.jpg"
                    },
                    {
                        "label": "CPU",
                        "image": "/cpu.jpg"
                    },
                    {
                        "label": "SSD",
                        "image": "/ssd.jpg"
                    },
                    {
                        "label": "GPU",
                        "image": "/gpu.jpg"
                    }
                ],
                "hint": "This component is typically long and thin, with multiple slots that plug directly into the motherboard.",
                "answer": "RAM",
                "thread_id": "thread_48WtEqfoqVgoXqJ6EebmEKFC",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 2,
                "attempts": 1,
                "Previous_tries": [
                    "RAM"
                ],
                "answer_status": "Answered",
                "image": ""
            }
        ]
    },
    {
        "module": 3,
        "title": "Troubleshooting",
        "questions": [
            {
                "activity": "Troubleshooting",
                "type": "fillInBlank",
                "question": "Your PC does not power on. The first component you should check is the ___ supply.",
                "hint": "This component provides power to the entire system.",
                "answer": "power",
                "thread_id": "thread_DwGVJBSvu1SxHAT5iKw5J8qP",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 3,
                "attempts": 1,
                "Previous_tries": [
                    "power"
                ],
                "answer_status": "Answered"
            },
            {
                "activity": "Troubleshooting",
                "type": "fillInBlank",
                "question": "If your system randomly restarts during use, you should check for ___ issues.",
                "hint": "This component may be overheating or failing.",
                "answer": "cooling",
                "thread_id": "thread_Kh4r4zGIXhOn3O7y5D4icCTj",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 3,
                "attempts": 1,
                "Previous_tries": [
                    "cooling"
                ],
                "answer_status": "Answered"
            },
            {
                "activity": "Troubleshooting",
                "type": "shortAnswer",
                "question": "USB devices aren't recognized when plugged in. What steps can you take to resolve this issue?",
                "hint": "Think about common troubleshooting steps for USB connection issues.",
                "answer": "Restart the computer",
                "thread_id": "thread_GRc9pJLmQkw7Zf2632GILfep",
                "assistant_id": "asst_09FjDLZ7hGIkqB1WmU3Oc79q",
                "module": 3,
                "attempts": 1,
                "Previous_tries": [
                    "Restart the computer"
                ],
                "answer_status": "Answered"
            }
        ]
    }
]