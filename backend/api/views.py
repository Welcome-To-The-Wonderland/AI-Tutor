from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer
from userauths.models import Profile
from .FeedbackAgent import OverClockTutor
from .KnowledgeAgent import KnowledgeAgent
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Thread, StudentData
from userauths.models import CustomUser
from django.db.models import Prefetch
from .models import Question
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from pyBKT.models import Model
from pyBKT.models.Roster import Roster, SkillRoster
import numpy as np
import pandas as pd
import logging
import random
import json
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

MODULES = [
    {
        "module": 1,
        "title": "Functionality",
        "questions": [
            {
                "activity": "Functionality",
                "type": "multipleChoice",
                        "question": "Which component acts as the brain of the computer, processing all the instructions?",
                        "skill": "CPU",
                        "options": ["CPU", "GPU", "RAM", "SSD"],
                        "hint": "This component handles all calculations and executes the operating system and applications.",
                        "answer": "CPU"
            },
            {
                "activity": "Functionality",
                "type": "multipleChoice",
                        "question": "Which storage type is generally faster and more durable?",
                        "skill": "Storage",
                        "options": ["SSD", "HDD", "RAM", "DVD"],
                        "hint": "Unlike traditional drives, this type stores data electronically rather than magnetically or mechanically.",
                        "answer": "SSD"
            },
            {
                "activity": "Functionality",
                "type": "fillInBlank",
                        "question": "The ___ temporarily stores data for quick access while the computer is running.",
                        "skill": "RAM",
                        "hint": "This is a type of volatile memory that clears when the computer shuts down.",
                        "answer": "ram"
            },
            {
                "activity": "Functionality",
                "type": "trueFalse",
                        "question": "RAM is used for long-term data storage.",
                        "skill": "RAM",
                        "options": ["True", "False"],
                        "hint": "This memory is primarily used to store data that the CPU needs to access quickly, not permanently.",
                        "answer": False
            },
            {
                "activity": "Functionality",
                "type": "fillInBlank",
                        "question": "To check CPU compatibility with a motherboard, you must ensure the CPU socket type is the same as the motherboard ___.",
                        "skill": "Motherboard",
                        "hint": "Think of the specific interface on the motherboard where the CPU is inserted.",
                        "answer": "brand"
            },
            {
                "activity": "Functionality",
                "type": "multipleChoice",
                "question": "Which of the following best explains why an SSD is more reliable than an HDD for mobile computing?",
                "skill": "Storage",
                "options": [
                    "SSDs generate less heat.",
                    "SSDs have no moving parts, reducing the risk of mechanical failure.",
                    "SSDs use less power.",
                    "SSDs are cheaper and easier to replace."
                ],
                "hint": "Think about what makes SSDs less susceptible to damage when moved around.",
                "answer": "SSDs have no moving parts, reducing the risk of mechanical failure."
            },
            {
                "activity": "Functionality",
                "type": "fillInBlank",
                "question": "The component responsible for regulating voltage levels across a motherboard is the ___.",
                "skill": "Motherboard",
                "hint": "This component ensures that all connected devices receive the correct voltage.",
                "answer": "voltage regulator module"
            },
            {
                "activity": "Functionality",
                "type": "trueFalse",
                "question": "An M.2 slot can be used to install both SSDs and GPUs.",
                "skill": "Motherboard",
                "options": ["True", "False"],
                "hint": "This slot is designed for a specific type of component that is not a GPU.",
                "answer": False
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
                        "skill": "Matching",
                        "images": [
                            {"component": "cpu", "image": "/cpu.jpg"},
                            {"component": "gpu", "image": "/gpu.jpg"},
                            {"component": "ram", "image": "/ram.jpg"},
                            {"component": "ssd", "image": "/ssd.jpg"}
                        ],
                "labels": ["CPU", "GPU", "RAM", "SSD"],
                "hint": "Pay attention to the unique shapes or functions of each component in the images.",
                        "answer": {"cpu": "CPU", "gpu": "GPU", "ram": "RAM", "ssd": "SSD"}
            },
            {
                "activity": "Identification",
                "type": "componentMatch",
                        "question": "Which component plugs into the motherboard shown in the center image?",
                        "skill": "Motherboard",
                        "centerImage": "/memquestion.jpg",
                        "options": [
                            {"label": "RAM", "image": "/ram.jpg"},
                            {"label": "CPU", "image": "/cpu.jpg"},
                            {"label": "SSD", "image": "/ssd.jpg"},
                            {"label": "GPU", "image": "/gpu.jpg"}
                        ],
                "hint": "This component is thin, rectangular, and fits into slots on the motherboard in pairs or sets.",
                        "answer": "RAM"
            },
            {
                "activity": "Identification",
                "type": "componentMatch",
                "question": "Which connector is used to transfer data between storage drives and the motherboard?",
                "skill": "Connections",
                "centerImage": "/a.jpg",  
                "options": [
                    {"label": "SATA Cable", "image": "/sata1.jpg"},
                    {"label": "PCIe Connector", "image": "/pcie1.jpg"},
                    {"label": "8-pin CPU Connector", "image": "/8pin1.jpg"},
                    {"label": "USB Cable", "image": "/usb1.jpg"}
                ],
                "hint": "This cable is commonly used to connect hard drives and solid-state drives to the motherboard.",
                "answer": "SATA Cable"
            },
            {
                "activity": "Identification",
                "type": "componentMatch",
                "question": "Which slot on the motherboard, shown in the center image, is designed to connect high-performance GPUs?",
                "skill": "Connections",
                "centerImage": "/b.jpg",
                "options": [
                    {"label": "PCIe x1 Slot", "image": "/pcie_x1.jpg"},
                    {"label": "PCI Slot", "image": "/pci_slots.jpg"},
                    {"label": "PCIe x16 Slot", "image": "/pcie_x16.jpg"},
                    {"label": "M.2 Slot", "image": "/m2.jpg"}
                ],
                "hint": "This slot is larger than others and provides higher bandwidth for GPUs.",
                "answer": "PCIe x16 Slot"
            },
            {
                "activity": "Identification",
                "type": "componentMatch",
                "question": "Which connector provides power from the PSU directly to the CPU on the motherboard?",
                "skill": "Connections",
                "options": [
                    {"label": "24-pin ATX Connector", "image": "/24.jpg"},
                    {"label": "6-pin PCIe Connector", "image": "/6.jpg"},
                    {"label": "8-pin CPU Connector", "image": "/8pin.jpg"},
                    {"label": "SATA Connector", "image": "/sata.jpg"}
                ],
                "hint": "This connector typically has 8 pins.",
                "answer": "8-pin CPU Connector"
            },
            {
                "activity": "Identification",
                "type": "componentMatch",
                "question": "Which of the following ports is commonly used to connect SSDs to the motherboard for high-speed data transfer?",
                "skill": "Connections",
                "options": [
                    {"label": "PCIe Slot", "image": "/pcie1.jpg"},
                    {"label": "SATA Port", "image": "/sata.jpg"},
                    {"label": "USB Port", "image": "/usb1.jpg"},
                    {"label": "Front Panel Header", "image": "/front.jpg"}
                ],
                "hint": "This port supports a wide variety of storage devices.",
                "answer": "SATA Port"
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
                        "skill": "Troubleshooting",
                        "question": "Your PC does not power on. The first component you should check is the ___ supply.",
                        "hint": "This component converts electrical energy from the wall outlet into usable power for the computer.",
                        "answer": "power"
            },
            {
                "activity": "Troubleshooting",
                "type": "fillInBlank",
                        "skill": "Troubleshooting",
                        "question": "If your system randomly restarts during use, you should check for ___ issues.",
                        "hint": "This issue can occur if the component responsible for dissipating heat is not functioning properly.",
                        "answer": "cooling"
            },
            {
                "activity": "Troubleshooting",
                "type": "shortAnswer",
                        "skill": "Troubleshooting",
                        "question": "USB devices aren't recognized when plugged in. What steps can you take to resolve this issue?",
                        "hint": "Think about restarting the system, reconnecting the devices, or updating drivers.",
                        "answer": "restart the computer"
            },
            {
                "activity": "Troubleshooting",
                "type": "multipleChoice",
                "question": "Your PC powers on, but the display shows no signal. Which component is most likely causing this issue?",
                "skill": "Troubleshooting",
                "options": [
                    "CPU",
                    "GPU",
                    "RAM",
                    "PSU"
                ],
                "hint": "This component is responsible for generating video output.",
                "answer": "GPU"
            },
            {
                "activity": "Troubleshooting",
                "type": "multipleChoice",
                "question": "You hear a series of long beeps during boot-up, and your system fails to start. Which component is most likely causing the issue?",
                "skill": "Troubleshooting",
                "options": [
                    "GPU",
                    "RAM",
                    "Motherboard",
                    "Storage Drive"
                ],
                "hint": "Beep codes are commonly associated with this type of memory.",
                "answer": "RAM"
            },
            {
                "activity": "Troubleshooting",
                "type": "multipleChoice",
                "question": "Your system randomly restarts while gaming. What is the most likely cause?",
                "skill": "Troubleshooting",
                "options": [
                    "A failing GPU",
                    "An insufficient PSU",
                    "A corrupted operating system",
                    "A damaged SSD"
                ],
                "hint": "Gaming often places high power demands on this component.",
                "answer": "An insufficient PSU"
            },
            {
                "activity": "Troubleshooting",
                "type": "multipleChoice",
                "question": "Your PC does not detect your SSD during boot. What should you check first?",
                "skill": "Troubleshooting",
                "options": [
                    "Ensure the SATA data cable is connected.",
                    "Reinstall the operating system.",
                    "Replace the power supply unit.",
                    "Upgrade the motherboard BIOS."
                ],
                "hint": "This connection is crucial for the SSD to communicate with the motherboard.",
                "answer": "Ensure the SATA data cable is connected."
            },
            {
                "activity": "Troubleshooting",
                "type": "multipleChoice",
                "question": "What should you do if your computer repeatedly freezes during use?",
                "skill": "Troubleshooting",
                "options": [
                    "Check the CPU temperature to ensure it is not overheating.",
                    "Install additional RAM.",
                    "Defragment your SSD.",
                    "Replace the GPU."
                ],
                "hint": "Freezing is often related to thermal or power issues.",
                "answer": "Check the CPU temperature to ensure it is not overheating."
            }
        ]
    }
]


def system_prompt():
    return (
        "You are a strict and knowledgeable tutor. Your task is to evaluate whether the student's "
        "response matches the concept of restarting a computer. Be concise and respond with either "
        "'Yes' or 'No' only."
    )


def evaluate_response_with_ai(user_input):
    load_dotenv()

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.beta.assistants.create(
            model="gpt-3.5-turbo",
            instructions=system_prompt(),
            temperature=0.4
        )
        client_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt()},
                {"role": "user", "content": user_input}
            ]
        )
        response_text = client_response.choices[0].message.content.strip(
        ).lower()
        if "yes" in response_text:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred while evaluating the response: {str(e)}")
        return False


def is_restart_mentioned(user_input):
    patterns = [
        r"restart(ing)? (the )?computer",
        r"reboot(ing)? (the )?system",
        r"turn(ing)? (it|the computer|the system)? off and on (again)?"
    ]
    user_input = user_input.lower()
    for pattern in patterns:
        if re.search(pattern, user_input):
            return True
    return False


@api_view(['POST'])
def evaluate_question(request):
    user_input = request.data.get('answer', '')

    if not user_input:
        return Response({"error": "Answer is required"}, status=status.HTTP_400_BAD_REQUEST)

    if is_restart_mentioned(user_input) or evaluate_response_with_ai(user_input):
        return Response({"correct": True, "feedback": "Correct! Restarting the computer is a common troubleshooting step."}, status=status.HTTP_200_OK)
    else:
        return Response({"correct": False, "feedback": "That's not quite right. Consider restarting the computer as a first step."}, status=status.HTTP_200_OK)


def parse_to_json():
    questions = Question.objects.all()
    data = []

    for question in questions:
        question_data = {
            "activity": question.activity,
            "type": question.question_type,
            "question": question.question_text,
            "skill": question.skill,
            "hint": question.hint,
            "answer": question.answer
        }
        if question.options:
            question_data["options"] = question.options
        if question.images:
            question_data["images"] = question.images
        if question.center_image:
            question_data["centerImage"] = question.center_image

        data.append(question_data)

    return json.dumps(data, indent=4)


@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
        '/api/register',
        '/api/profile',
    ]
    return Response(routes)


@api_view(['POST'])
def completion_view(request):
    data = request.data
    user_email = data.get('user')
    modules = data.get('modules')

    if not user_email or not modules:
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    for module in modules:
        module_title = module.get("title")
        questions = module.get("questions", [])

        for question in questions:
            activity_name = module_title
            is_correct = question.get(
                "answer_status", "Unanswered") == "Answered"
            attempts = question.get("attempts", 0)
            skill = question.get("skill")

            StudentData.objects.create(
                student=student,
                skill=skill,
                activity_name=activity_name,
                is_correct=is_correct,
                attempts=attempts
            )

    return Response({"message": "Completion data saved successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_ai_assistant(request):
    """
    Retrieve the AI assistant assigned to the authenticated user.
    """
    try:
        user = request.user
        ai_assistant = user.ai_assistant

        if ai_assistant:
            return Response({"ai_assistant": ai_assistant}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "No AI assistant assigned to this user."},
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def get_feedback(request):
    """
    API view to process two JSON inputs (question_data and student_progress)
    and pass them, along with a query, into the tutor methods for further handling.

    Example Expected JSON inputs:
    question_data = {
                    "activity": "Troubleshooting",
                    "type": "fillInBlank",
                    "question": "Your PC does not power on. The first component you should check is the ___ supply.",
                    "hint": "This component provides power to the entire system.",
                    "answer": "power"
     }

student_progress = {
        "answer_status": "Unanswered",
        "Attempts": 2,
        "Previous Tries": {"Power Supply": "Incorrect", "PSU": "Incorrect"},
}
query = "Why is this wrong?"
    """

    question_data = request.data.get('question_data')

    student_progress = request.data.get('student_progress')

    query = request.data.get('query')

    assistant_data = request.data.get('assistant_info')

    if not question_data or not student_progress or not query:
        return Response(
            {"error": "Both 'question_data', 'student_progress', and 'query' are required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        tutor = OverClockTutor(assistant_data['assistant_id'])
        result = tutor.infer(question_data, query,
                             student_progress, assistant_data['thread_id'])

        return Response({"feedback": result}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": f"An error occurred while processing the request: {
                str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_questions(request):
    modules = []
    email = request.query_params.get('email')

    if not email:
        return Response({"error": "Email is required to fetch questions."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
        has_entries = StudentData.objects.filter(student=user).exists()

    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    assistant_id = user.ai_assistant

    if not assistant_id:
        return Response({"error": "No AI assistant assigned to this user."}, status=status.HTTP_400_BAD_REQUEST)

    if has_entries:
        all_questions = Question.objects.all()
        student_progress = StudentData.objects.filter(student=user)
        student_record = []
        for progress in student_progress:
            student_record.append({
                "user_id": progress.student_id,
                "skill_name": progress.skill,
                "correct": progress.is_correct,
                "attempts": progress.attempts,
            })

        skills = list(student_progress.values_list(
            'skill', flat=True).distinct())
        KTAgent = KnowledgeAgent(skills=skills, student_record=student_record)
        KTAgent.train_model()

        modules = KTAgent.get_new_questions(all_questions)
    else:
        modules = MODULES

    for module in modules:
        for question in module['questions']:

            existing_thread = Thread.objects.filter(
                assistant_id=assistant_id,
                question=question['question']
            ).first()

            if existing_thread:

                thread_id = existing_thread.thread_id
            else:

                tutor = OverClockTutor(assistant_id)
                thread_id = tutor.start_question_thread(
                    query="Hello! I am a student working on a problem.",
                    question=question['question']
                )

                Thread.objects.create(
                    assistant_id=assistant_id,
                    question=question['question'],
                    thread_id=thread_id
                )

            question['thread_id'] = thread_id
            question['assistant_id'] = assistant_id
            question['module'] = module['module']
            question['attempts'] = 0
            question['Previous_tries'] = []
            question['answer_status'] = "Unanswered"

    return Response(modules, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_enrichment_questions(request):
    user_email = request.query_params.get('email')
    print(user_email)

    # Use get_or_create to prevent duplicate questions
    for module in MODULES:
        for question in module['questions']:
            try:
                Question.objects.get_or_create(
                    question_text=question['question'],
                    defaults={
                        'activity': question['activity'],
                        'question_type': question['type'],
                        'skill': question['skill'],
                        'hint': question['hint'],
                        'answer': question['answer'],
                        'options': question.get('options'),
                        'labels': question.get('labels'),
                        'images': question.get('images'),
                        'center_image': question.get('centerImage')
                    }
                )
            except Exception as e:
                print("The question didn't get added")
                continue

    try:
        all_questions = Question.objects.all()
        print("We have all questions")
        print(all_questions)

        student_progress_qs = StudentData.objects.filter(
            student__email=user_email)
        print("We queried the student progress")

        if not student_progress_qs.exists():
            print("No student progress")
            # Fallback data
            student_record = [
                {
                    "user_id": 1,
                    "skill_name": "CPU",
                    "correct": True,
                    "attempts": 1
                },
                {
                    "user_id": 1,
                    "skill_name": "Storage",
                    "correct": False,
                    "attempts": 2
                },
                {
                    "user_id": 2,
                    "skill_name": "Storage",
                    "correct": False,
                    "attempts": 2
                }
            ]
            skills = list({record["skill_name"] for record in student_record})
        else:
            student_record = [
                {
                    "user_id": progress.student.id,
                    "skill_name": progress.skill,
                    "correct": progress.is_correct,
                    "attempts": progress.attempts,
                }
                for progress in student_progress_qs
            ]
            print("We have student record")
            print(student_record)

            skills = list(student_progress_qs.values_list(
                'skill', flat=True).distinct())

        KTAgent = KnowledgeAgent(skills=skills, student_record=student_record)
        KTAgent.train_model()
        print("We have a trained model")

        enrichment_modules = KTAgent.get_new_questions(all_questions)
        print("We have enrichment modules")

        return Response({"modules": enrichment_modules}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_response(request):
    pass


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
