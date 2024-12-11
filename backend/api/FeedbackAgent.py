"""Current file being used
Prompts need further optimization!
Multiple CHoice and True False questions are working fine.
Fill in the blank and short answer questions are not working as expected.
Image questions are not fully implemented, but the structure is there.
"""

from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from .OverClockPromptTemplate import system_prompt, tool_setter, final_conclusion
import time
import atexit
import base64


class assistant:
    def __init__(self, assistant):
        self.id = assistant


def assign_ai_assistant(student_name):
    """Initializes the AI Assistant"""
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    assistant = client.beta.assistants.create(
        name="OverClock AI Assistant - A Tutor for Building Computers",
        instructions=system_prompt(student_name),
        model="gpt-4o",
        temperature=0.4,
    )
    print("Created the Assistant:", assistant.id)
    return assistant.id


class OverClockTutor:
    def __init__(self, assistant_id) -> None:
        load_dotenv()
        self.assistant = assistant(assistant_id)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.ComputerVisionAgent = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.threads = {}

        atexit.register(self.cleanup)

    def start_question_thread(self, query, question):
        """Associates each question with a thread"""
        messages = [
            {
                "role": "user",
                "content": f"""
                Current User Question: {query}
                """
            }
        ]
        thread = self.client.beta.threads.create(messages=messages)
        self.threads[question] = thread.id
        print(f"Created the thread for '{question}':", thread.id)
        return thread.id

    def call_computerVision(self, img):
        base64_img = img
        response = self.ComputerVisionAgent.chat.completions.create(
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
        return response

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode("utf-8")
        return encoded_string

    def get_SpecializedPromptInjections(self, question_data, student_progress):
        print("Entered Specialized Prompt Injections")
        if question_data['type'] == "multipleChoice" or question_data['type'] == "trueFalse":
            print("Question Data:", question_data)
            print("question_data['options']:", question_data['options'])
            print("question_data['answer']:", question_data['answer'])
            print("student_progress['answer_status']:",
                  student_progress['answer_status'])
            print("student_progress['Attempts']:",
                  student_progress['Attempts'])
            print("student_progress['Previous_tries']:",
                  student_progress['Previous_tries'])
            initial = f"""
             Question: {question_data['question']}
             Options: {question_data['options']}
             Answer: {question_data['answer']}

             Their current status:
             Answer Status: {student_progress['answer_status']}
             Attempts: {student_progress['Attempts']}
             Previous Tries: {student_progress['Previous_tries']}
             """

            if student_progress['answer_status'] == 'Unanswered':
                steps = [
                    "The user cannot see this message. Analyze the answer the user provided and think through why this choice does not satisfy the question's requirements. Focus only on this specific answer's limitations in the context of the question, without considering or mentioning other options.",

                    "The user cannot see this message. Plan a response that explains why the user's choice is incorrect by focusing solely on the selected answer’s shortcomings. Avoid referencing other options, suggesting the correct answer, or providing any form of encouragement or praise.",

                    f"The user can see this message. Explain why the user's chosen answer is incorrect by detailing only the limitations of their specific choice in relation to the question '{
                        question_data['question']}'. Keep feedback analytical and encourage them, but avoid mentioning other options, or hinting at the correct answer.",
                ]

            else:
                steps = [
                    "The user cannot see this message. Have an inner monologue with yourself about what aspects of the answer you should emphasize so the user better understands why it is correct.",
                    "The user cannot see this message. Given the example, think of a contrasting cases example or a real-life example you can use. This will help the user understand why the answer is correct.",
                    f"The user can see this message. Provide a response that is sensitive and helpful to help them understand the answer of {
                        question_data['question']} using the analysis you've performed in the last two steps."
                ]

        elif question_data['type'] == "fillInBlank" or question_data['type'] == "shortAnswer":
            initial = f"""
              Question: {question_data['question']}

              Their current status:
              Answer Status: {student_progress['answer_status']}
              Attempts: {student_progress['Attempts']}
              Previous Tries: {student_progress['Previous_tries']}
              """

            if student_progress['answer_status'] == 'Unanswered':
                steps = [
                    "The user cannot see this message. Have an inner monologue with yourself about the question the user is working on.  Infer the key issues they are most likely facing.",
                    "The user cannot see this message. Think about ways you can help them understand the key issue(s) they are facing. What are some signifers that could help them? If their answer is clearly right or has a typo, tell them the right answer since the tutoring system requires an exact answer.",
                    f"The user can see this message. Provide a response that is sensitive and helpful to guide them to the correct answer of {question_data['question']} which is '{
                        question_data['answer']}' using the analysis you've performed in the last two steps. Since the system answer is very specific, give them answer ONLY IF their answer has a typo or similar.",
                ]
            else:
                steps = [
                    "The user cannot see this message. Have an inner monologue with yourself about what aspects of the answer you should emphasize so the user better understands why it is correct.",
                    "The user cannot see this message. Given the example, think of a contrasting cases example or a real-life example you can use. This will help the user understand why the answer is correct.",
                    f"The user can see this message. Provide a response that is sensitive and helpful to help them understand the answer of {
                        question_data['question']} which is '{question_data['answer']}' using the analysis you've performed in the last two steps."
                ]
        else:
            print("Identification Questions", student_progress['Image'])

            initial = f"""
            Question: {question_data['question']}

            Their current status:
            Answer Status: {student_progress['answer_status']}
            Attempts: {student_progress['Attempts']}
             """
            print("Identification Questions")

            if student_progress['answer_status'] == 'Unanswered':
                information = self.call_computerVision(
                    student_progress['Image'])
                steps = [
                    f"The user cannot see this message. Have an inner monologue with yourself about the question the user is working on.  Infer the key issues they are most likely facing. A description of the user current progress is given through computer vision: {
                        information}",
                    "The user cannot see this message. Given the example, think of a contrasting cases example or a real-life example you can use. This will help the user understand why the answer is correct.",
                    f"The user can see this message. Provide a response that is sensitive and helpful to help them understand the answer of {
                        question_data['question']} which is '{question_data['answer']}' using the analysis you've performed in the last two steps.",
                ]
            else:
                steps = [
                    "",
                    "",
                    ""
                ]

        return initial, steps

    def infer(self, question_data, student_message, student_progress, thread_id):
        print("Entered infer")
        initial, steps = self.get_SpecializedPromptInjections(
            question_data, student_progress)

        student_message = f"""
        The current question the user attempting is:
        Type: {question_data['type']}
        {initial}

        The question they asked you: {student_message}
       """
        print(student_message)

        try:
            message = self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=student_message)

            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id, assistant_id=self.assistant.id, temperature=0)
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run.id)

            while run_status.status != 'completed':
                print("Job Status :", run_status.status)
                print("Waiting a few seconds to retieve ", thread_id, "...")
                time.sleep(10)
            print("Done waiting!")
        except Exception as e:
            print("Error in infer:", e)

        try:
            final_response = "ERROR"
            for i in range(0, 3):
                student_message = steps[i]
                print(student_message)
                print("\n")

                message = self.client.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=student_message)
                run = self.client.beta.threads.runs.create_and_poll(
                    thread_id=thread_id, assistant_id=self.assistant.id, temperature=0)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id)
                while run_status.status != 'completed':
                    print("Job Status :", run_status.status)
                    print("Waiting a few seconds to retieve ", thread_id, "...")
                    time.sleep(10)
                print("Done waiting!")

                messages = list(self.client.beta.threads.messages.list(
                    thread_id=thread_id, run_id=run.id))
                message_content = messages[0].content[0].text
                print(student_message)
                print("\n")
                print("AI REPLY:", message_content.value)
                print("\n")
                final_response = message_content.value
            return final_response
        except Exception as e:
            print("Error in infer:", e)

    @property
    def initialize_assistant(self):
        """Initializes the AI Assistant"""
        self.assistant = self.client.beta.assistants.create(
            name="OverClock AI Assistant - A Tutor for Building Computers",
            instructions=system_prompt(self.student_name),
            model="gpt-4o",
            temperature=0.4,
        )
        print("Created the Assistant:", self.assistant.id)

    @property
    def delete_assistant_and_thread(self):
        """Deletes the AI Assistant"""
        self.client.beta.assistants.delete(self.assistant.id)
        print("Deleted the Assistant:", self.assistant.id)

    def cleanup(self):
        """Cleanup function to delete the assistant on exit"""
        """
        for x in range(0,3):
          try:
            time.sleep(5)
            if hasattr(self, 'assistant') and self.assistant:
                self.delete_assistant_and_thread
            break
          except Exception as e:
                print("Error in cleanup:", e)
        """


"""
question_data = {
                    "activity": "Functionality",
                    "type": "multipleChoice",
                    "question": "Which component acts as the brain of the computer, processing all the instructions?",
                    "options": ["CPU", "GPU", "RAM", "SSD"],
                    "hint": "Think of the part responsible for carrying out commands and calculations.",
                    "answer": "CPU"
    }


query = "Why is this right?"

student_progress = {
        "answer_status": "Answered",
        "Attempts": 1,
        "Previous Tries": {"CPU":"Correct"},
    }

x.start_question_thread(query=query, question=question_data['question'])
x.infer(question_data, query, student_progress)

"""


"""


progress = print(tutor.call_computerVision("label.png"))
"""


"""
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

"""
question_data = {
                    "activity": "Functionality",
                    "type": "multipleChoice",
                    "question": "Which component acts as the brain of the computer, processing all the instructions?",
                    "options": ["CPU", "GPU", "RAM", "SSD"],
                    "hint": "Think of the part responsible for carrying out commands and calculations.",
                    "answer": "CPU"
    }


query = "Why is this right?"

student_progress = {
        "answer_status": "Answered",
        "Attempts": 1,
        "Previous Tries": {"CPU":"Correct"},
    }
"""

"""
question_data = {
                    "activity": "Functionality",
                    "type": "multipleChoice",
                    "question": "Which component acts as the brain of the computer, processing all the instructions?",
                    "options": ["CPU", "GPU", "RAM", "SSD"],
                    "hint": "Think of the part responsible for carrying out commands and calculations.",
                    "answer": "CPU"
    }


query = "I don't understand this!"

student_progress = {
        "answer_status": "Unanswered",
        "Attempts": 1,
        "Previous Tries": {"GPU": "Incorrect"},
    }

tutor.start_question_thread(query=query, question=question_data['question'])
tutor.infer(question_data, query, student_progress)
"""
