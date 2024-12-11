from api.models import Question
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


dataset = [






    1
]


questions = [
    {
        "module": 1,
        "title": "Functionality",
        "questions": [
            {
                "skill": "CPU Identification",
                "type": "multipleChoice",
                "question": "Which component acts as the brain of the computer, processing all the instructions?",
                "options": ["CPU", "GPU", "RAM", "SSD"],
                "hint": "Think of the part responsible for carrying out commands and calculations.",
                "answer": "CPU"
            },
            {
                "skill": "Storage Type",
                "type": "multipleChoice",
                "question": "Which storage type is generally faster and more durable?",
                "options": ["SSD", "HDD", "RAM", "DVD"],
                "hint": "This type has no moving parts.",
                "answer": "SSD"
            },
            {
                "skill": "RAM Usage",
                "type": "fillInBlank",
                "question": "The ___ temporarily stores data for quick access while the computer is running.",
                "hint": "This memory is volatile and resets when the computer is turned off.",
                "answer": "ram"
            },
            {
                "skill": "RAM Purpose",
                "type": "trueFalse",
                "question": "RAM is used for long-term data storage.",
                "options": ["True", "False"],
                "hint": "Think about the purpose of RAM in relation to data storage.",
                "answer": False
            },
            {
                "skill": "CPU Socket Compatibility",
                "type": "fillInBlank",
                "question": "To check CPU compatibility with a motherboard, you must ensure the CPU socket type is the same as the motherboard ___.",
                "hint": "This part of the CPU must match the motherboard socket.",
                "answer": "brand"
            }
        ]
    },
    {
        "module": 2,
        "title": "Identification",
        "questions": [
            {
                "skill": "Component Matching",
                "type": "dragAndDrop",
                "question": "Match components with images.",
                "images": [
                    {"component": "cpu", "image": "/cpu.jpg"},
                    {"component": "gpu", "image": "/gpu.jpg"},
                    {"component": "ram", "image": "/ram.jpg"},
                    {"component": "ssd", "image": "/ssd.jpg"}
                ],
                "labels": ["CPU", "GPU", "RAM", "SSD"],
                "hint": "Match each label with the correct image based on component function.",
                "answer": {"cpu": "CPU", "gpu": "GPU", "ram": "RAM", "ssd": "SSD"}
            },
            {
                "skill": "Memory Slot Identification",
                "type": "componentMatch",
                "question": "Which component plugs into the motherboard shown in the center image?",
                "centerImage": "/memquestion.jpg",
                "options": [
                    {"label": "RAM", "image": "/ram.jpg"},
                    {"label": "CPU", "image": "/cpu.jpg"},
                    {"label": "SSD", "image": "/ssd.jpg"},
                    {"label": "GPU", "image": "/gpu.jpg"}
                ],
                "hint": "This component is typically long and thin, with multiple slots that plug directly into the motherboard.",
                "answer": "RAM"
            }
        ]
    },
    {
        "module": 3,
        "title": "Troubleshooting",
        "questions": [
            {
                "skill": "Power Supply Issues",
                "type": "fillInBlank",
                "question": "Your PC does not power on. The first component you should check is the ___ supply.",
                "hint": "This component provides power to the entire system.",
                "answer": "power"
            },
            {
                "skill": "Cooling Issues",
                "type": "fillInBlank",
                "question": "If your system randomly restarts during use, you should check for ___ issues.",
                "hint": "This component may be overheating or failing.",
                "answer": "cooling"
            },
            {
                "skill": "USB Troubleshooting",
                "type": "shortAnswer",
                "question": "USB devices aren't recognized when plugged in. What steps can you take to resolve this issue?",
                "hint": "Think about common troubleshooting steps for USB connection issues.",
                "answer": "Restart the computer"
            }
        ]
    }
]


for module_data in questions:
    module_number = module_data["module"]
    for question in module_data["questions"]:
        Question.objects.create(
            module=module_number,
            skill=question["skill"],
            question_text=question["question"],
            options=question.get("options"),
            answer=question["answer"],
            hint=question.get("hint"),
            question_type=question["type"],
            image=question.get("centerImage"),
            images=question.get("images"),
            labels=question.get("labels")
        )

print("Questions successfully imported!")
