import requests
import pandas as pd
import random
from requests.auth import HTTPBasicAuth

df = pd.read_csv("questions.csv")

print(df.shape)
# print(df["subject"].unique())
# print(df["use"].unique())

url = "http://127.0.0.1:8000/get_questions"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

data = {
    "use": "Total Bootcamp",
    "subject": "Data Science",
    "number_questions": 5
}

response = requests.get(url, json=data, headers=headers, auth=HTTPBasicAuth('alice', 'wonderland'))

print(response.status_code)

print(response.json())


data = {
    "category": "Geography",
    "difficulty": "Easy",
    "question": "What is the capital of France?",
    "subject": "Data Science",
    "correct": "Paris",
    "use": "Total Bootcamp",
    "answerA": "Paris",
    "answerB": "Paris",
    "answerC": "Paris",
    "answerD": "Paris"
}

response = requests.post("http://127.0.0.1:8000/create_question", json=data, auth=HTTPBasicAuth('admin', '4dm1N'))

print(response.status_code)
print(response.json())

