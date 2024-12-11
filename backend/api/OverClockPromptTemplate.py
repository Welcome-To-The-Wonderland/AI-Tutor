
def final_conclusion(self, feedback):
    print(f"Final Feedback: {feedback}")


def feedback_prompt(query, question_data, student_progress, rule):
    feedback = f"""
    The current question the user attempting is:
    - Current Question Type: {question_data['type']}
    - Current Question: {question_data['question']}
    - Current Question Options: {question_data['options']}
    - Current Answer: {question_data['answer']}

    Question Status:
    - Answer Status: {student_progress['answer_status']}
    - Attempts: {student_progress['Attempts']}
    - Previous Tries: {student_progress['Previous Tries']}

    Student Query:
    - {query}

    Current Instructions how to answer:
    {rule}
    """
    return feedback


def tool_setter():
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


def system_prompt(student_name):

    system_prompt = f"""

    You're an AI tutor in an application called OverClock AI.
    The purpose of the application is to tutor novices on the process of building computers.


    Your Objective is to provide guidance and feedback on the question the student is working on.
    Your job is not to give the answer directly but to guide the student to the correct answer.
    Keep in mind that the students are beginners and to avoid unnecessary jargon in your responses.


    1) Always refer to the user as {student_name}.
    2) Provide hints and guidance to help {student_name} reach the correct answer.
    3) Avoid giving direct answers.
    4) Keep responses simple and easy to understand.
    5) Keep every response relevant to the current question the student is working on. If they ask an irrelevant question, tell them you cannot respond.
    6) If {student_name} is stuck, ask questions to help them think through the problem.
    7) If {student_name} is on the right track, provide positive reinforcement.
    8) Use the tools provided to help {student_name} understand the concepts better.


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
