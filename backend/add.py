import json
from api.models import Question
import os


def add_questions_from_file():
    """
    Reads questions from a JSON file named 'dataset.json' in the current directory and adds them to the database.
    """
    file_path = os.path.join(os.getcwd(), "dataset.json")

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON file. {e}")
        return

    for module in data:
        for question_data in module.get("questions", []):
            question = Question(
                activity=question_data["activity"],
                question_type=question_data["type"],
                question_text=question_data["question"],
                skill=question_data["skill"],
                hint=question_data.get("hint", ""),
                answer=question_data["answer"],
                options=question_data.get("options", []),
                images=question_data.get("images", None),
                center_image=question_data.get("centerImage", None),
                labels=question_data.get("labels", None)
            )
            question.save()

    print("Questions added to the database successfully.")


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
        print(data)

    return json.dumps(data, indent=4)
