import pandas as pd
from pyBKT.models import Model

# Step One: Define the data and preprocess it for the nodel
# Student_id just represents the user
# question is irrelevant for the model
# correct is the binary correctness of the response
# attempts is the number of attempts for that question which is really important
# skill_id is the concept or skill being tested which is really important 
# (this should be the activity)
student_progress = [
    {
        "student_id": 1,
        "question": "Which component acts as the brain of the computer, processing all the instructions?",
        "response": "CPU",
        "answer_status": "Correct",
        "Attempts": 1,
        "module": "Functionality"
    },
    {
        "student_id": 1,
        "question": "Which storage type is generally faster and more durable?",
        "response": "HDD",
        "answer_status": "Incorrect",
        "Attempts": 2,
        "module": "Functionality"
    },
    {
        "student_id": 2,
        "question": "Which storage type is generally faster and more durable?",
        "response": "HDD",
        "answer_status": "Incorrect",
        "Attempts": 2,
        "module": "Functionality"
    }
]

# This is the data that we will be using to give to the bayesian inference model
# Some of these parameters are not necessary for the model but are maybe useful for analysis
data = []
for progress in student_progress:
    data.append({
        "student_id": progress["student_id"],
        "skill_id": progress["module"],  # Skill or concept
        "question": progress["question"],  # Optional: Question text
        "correct": 1 if progress["answer_status"] == "Correct" else 0,  # Binary correctness
        "attempts": progress["Attempts"]
    })

df = pd.DataFrame(data)

# Prints out the data frame
print("DataFrame columns:", df.columns)
print(df)

# Initialize the BKT model with proper column mapping
model = Model(
    seed=42,
    defaults={
        "user_id": "student_id",  # Map user ID column
        "skill_name": "skill_id",     # Map skills column
        "correct": "correct"      # Map correctness column
    }
)

# Trains the model
model.fit(data=df)

# Predict mastery
# Correct predictions are the probability of correctness
# Thiis identifies areas where students need more support aka more questions on
# concepts



# State predictions are the probability they already mastered the skill
# It reflects the student's latent knowledge state 
# (what they "know" or "don't know") as inferred by the model.
# This is useful for deciding if the student should move to the next topic
# and what skills require more mastery, so we need to a threshold for this
predictions = model.predict(data=df)

# It is important to group the predictions by student_id and skill_id
# We want the averages of how they performed on each skill (functionality, identification, etc.)
# This makes it easy to deliver the questions to the student. 
# Group by student_id and skill_id, aggregating numeric columns
grouped_predictions = predictions.groupby(["student_id", "skill_id"]).agg({
    "correct": "mean",                  # Average correctness
    "attempts": "sum",                  # Sum up attempts
    "correct_predictions": "mean",     # Average of predictions
    "state_predictions": "mean"        # Average of state predictions
}).reset_index()

print(grouped_predictions)
