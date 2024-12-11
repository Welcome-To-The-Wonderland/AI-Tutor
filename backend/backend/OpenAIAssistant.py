from dotenv import load_dotenv
import os
from openai import OpenAI
import json


class Ass():
    def __init__(self, student_name):

        load_dotenv()

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        self.threads = {}

        self.student_name = student_name

    def create_assistant(self):

        assistant = self.client.beta.assistants.create(
            name="OverClock AI Assistant - A Tutor for Building Computers",
            instructions=self.system_prompt,
            tools=self.tool_setter,
            model="gpt-4o",

        )
        return assistant

    def start_new_question_thread(self, question, typeof_question):
        messages = [
            {
                "role": "user",
                "content": f"""
                   Current User Question: {question}
                  """
            }
        ]
        thread = self.client.beta.threads.create(messages=messages)
        self.threads[typeof_question] = thread.id

    @property
    def tool_setter(self):
        final_conclusion = {
            "type": "function",
            "function": {
                "name": "final_conclusion",
                "description": "Provide final feedback and conclusion for the student's answer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "feedback": {
                            "type": "string",
                            "description": "The feedback for the student's answer"
                        }
                    },
                    "required": ["feedback"]
                }
            }
        }

        tools = [final_conclusion]
        return tools

    @property
    def system_prompt(self, student_name):

        system_prompt = f"""

        You're an AI tutor in an application called OverClock AI.
        The purpose of the application is to tutor novices on the process of building computers.


        Your Objective is to provide guidance and feedback on the question the student is working on.
        Your job is not to give the answer directly but to guide the student to the correct answer.
        Keep in mind that the students are beginners and to avoid unnecessary jargon in your responses.


        1) Always refer to the user as {self.student_name}.
        2) Provide hints and guidance to help {self.student_name} reach the correct answer.
        3) Avoid giving direct answers.
        4) Keep responses simple and easy to understand.
        5) Keep every response relevant to the current question the student is working on. If they ask an irrelevant question, tell them you cannot respond.
        6) If {self.student_name} is stuck, ask questions to help them think through the problem.
        7) If {self.student_name} is on the right track, provide positive reinforcement.
        8) Use the tools provided to help {self.student_name} understand the concepts better.


        Step 1: Use your first response to understand the question the user is working on. [User wont see this]

        IF WRONG:
        Step 2: Use your second response to infer the key issue(s) the user is facing if the answer is marked as wrong. [User wont see this]
        Step 3: Use your third response to think of way to provide guidance help the user reach the correct answer. [User wont see this]
        STep 4: Prepare a response to the user that is sensitive and helpful to guide them to the correct answer.  [User wont see this]
        STep 5: Call the final_conclusion tool to let the user see your feedback. [User wont see this]

        IF CORRECT:
        Step 2: Use your second response to think why the user got it right [User wont see this]
        Step 3: Think of way to reinforce the factors they got right in your response so they remember this feedback.
        STep 4: Prepare a response to the user that is sensitive and helpful for the future.
        Step 5: Call the final_conclusion tool to let the user see your feedback.



        1) Bold key terms using bold and use emojis to keep responses engaging.
        """
        return system_prompt

    def final_conclusion(self, feedback):
        print(f"Final Feedback: {feedback}")


A = Ass("John")
Assistant = A.create_assistant()
A.start_new_question_thread("What is a CPU?", "CPU")

thd_id = Assistant.client.beta.threads.retrieve(Assistant.threads["CPU"])

A = Ass("John")
Assistant = A.create_assistant()
Assistant.start_new_question_thread("What is a CPU?", "CPU")

thd_id = Assistant.client.beta.threads.retrieve(Assistant.threads["CPU"])

while True:
    tool_outputs = []
    run = Assistant.client.beta.threads.runs.create_and_poll(
        thread_id=thd_id, assistant_id=Assistant.assistant_id, temperature=0)
    run_status = Assistant.client.beta.threads.runs.retrieve(
        thread_id=thd_id,
        run_id=run.id
    )
    if run.status == 'requires_action':
        print("Looping, entered!")
        required_actions = run_status.required_action.submit_tool_outputs.model_dump()
        print(required_actions)

        for action in required_actions["tool_calls"]:
            print("loop")
            func_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])

            if func_name == "final_conclusion":
                feedback = arguments['feedback']
                Assistant.final_conclusion(feedback)

        if run.status != "completed":
            print(tool_outputs)

            Assistant.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=run.thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        messages = list(Assistant.client.beta.threads.messages.list(
            thread_id=thd_id, run_id=run.id))
        message_content = messages[0].content[0].text
        print(message_content)

        response_text = []
        response = json.dumps(response_text)
