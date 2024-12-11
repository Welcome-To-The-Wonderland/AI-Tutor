from pyBKT.models import Model
from pyBKT.models.Roster import Roster, SkillRoster
import pandas as pd
import random
import json
from collections import defaultdict

class KnowledgeAgent:
    def __init__(self, student_record, skills):
        self.skills = skills
        self.record = student_record
        self.model = Model(seed=42)
        self.defaults = {
            "learns": 0.15,
            "forgets": 0.02,
            "guesses": 0.2,
            "slips": 0.15,
            "prior": 0.3
        }

        self.student = student_record[0]['user_id']
        self.roster = Roster(students=[self.student], skills=skills)

    def train_model(self):
        df = pd.DataFrame(self.record)
        self.model.fit(
            data=df,
            skills=self.skills,
            defaults=self.defaults
        )
        self.roster.set_model(self.model)

        predictions = self.model.predict(data=df)

        grouped_predictions = predictions.groupby(["user_id", "skill_name"]).agg({
            "correct": "mean",
            "attempts": "sum",
            "correct_predictions": "mean",
            "state_predictions": "mean"
        }).reset_index()

        print(grouped_predictions)
        print(self.roster.skill_rosters.items())

    def get_new_questions(self, questions):
        print("We are in the get_new_questions method")
        selected_questions = []
        selected_question_texts = set()
        print(f"The questions we were given are {questions}")

        for skill_name, skill_roster in self.roster.skill_rosters.items():
            student = skill_roster.students.get(self.student)
            if student:
                mastery_prob = student.get_mastery_prob()
                if mastery_prob < 0.8:
                    print(f"Student {student} needs more practice on {
                          skill_name}")
                    skill_questions = questions.filter(skill=skill_name).exclude(
                        question_text__in=selected_question_texts)
                    mastery_questions = skill_questions[:5]
                    selected_questions.extend(mastery_questions)
                    selected_question_texts.update(
                        mastery_questions.values_list("question_text", flat=True))
        print("We are done with the mastery questions")

        remaining_questions = questions.exclude(
            question_text__in=selected_question_texts)
        required_questions = max(0, (3 * 5) - len(selected_questions))
        random_questions = random.sample(
            list(remaining_questions),
            min(required_questions, len(remaining_questions))
        )
        selected_questions.extend(random_questions)
        selected_question_texts.update(
            q.question_text for q in random_questions)
        print("We are done with the random questions")

        modules = []
        module_counter = 1
        while selected_questions and module_counter <= 3:
            module_questions = selected_questions[:5]
            selected_questions = selected_questions[5:]

            module_data = {
                "module": module_counter,
                "title": f"Knowledge Tracing {module_counter}",
                "questions": []
            }

            for question in module_questions:
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
                if hasattr(question, "images") and question.images:
                    question_data["images"] = question.images
                if hasattr(question, "center_image") and question.center_image:
                    question_data["centerImage"] = question.center_image
                if hasattr(question, "labels") and question.labels:
                    question_data["labels"] = question.labels

                module_data["questions"].append(question_data)

            modules.append(module_data)
            module_counter += 1

        return modules
    """
    def get_new_questions(self, Question):
        questions = Question.objects.all()
        selected_questions = []
        for skill_name, skill_roster in self.roster.skill_rosters.items():
           student = skill_roster.students.get(self.student)
           if student:
               mastery_prob = student.get_mastery_prob()
               if mastery_prob < 0.8:
                     print(f"Student {student} needs more practice on {skill_name}")
                     skill_questions = questions.filter(skill=skill_name)
                     print(f'questions for {skill_name}: {skill_questions}')
                     selected_questions.extend(skill_questions[:2]) 
        
        
        if len(selected_questions) < 3:
            remaining_questions = questions.exclude(id__in=[q.id for q in selected_questions])
            random.shuffle(remaining_questions)
            selected_questions.extend(remaining_questions[:3 - len(selected_questions)])

"""


"""

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
"""


def format_questions(self, questions):
    pass
