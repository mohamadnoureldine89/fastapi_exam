from fastapi import HTTPException, Depends, status
from pydantic import BaseModel, field_validator, Field
import pandas as pd
import random
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List


api_exam = FastAPI(
    title='Fast API Exam',
    description='This is a FastAPI application for fetching and managing exam questions.'
)

# Perform a healthcheck
@api_exam.get("/healthcheck")
def healthcheck():
    """Endpoint to verify the API is functional."""
    return {"status": "API is functional"}


users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}

security = HTTPBasic()


# Function to verify user credentials
def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = credentials.username
    password = credentials.password

    if user in users and users[user] == password:
        return user
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")



@api_exam.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

@api_exam.exception_handler(FileNotFoundError)
async def file_not_found_error_handler(request: Request, exc: FileNotFoundError):
    return JSONResponse(
        status_code=500,
        content={"message": "Questions file not found"},
    )


class Question_set_params(BaseModel):
    use: str = Field(description="The type of test")
    subject: str = Field(description="The subject of the test")
    number_questions: int = Field(description="The number of questions to fetch")

    @field_validator("number_questions")
    @classmethod
    def validate_number_questions(cls, value):
        if value not in [5, 10, 15]:
            raise ValueError("number_questions must be 5, 10, or 15")
        return value

"""class Question_set_params(BaseModel):
    use: str
    subject: str
    number_questions: int"""

class Question(BaseModel):
    question: str
    subject: str
    correct: str
    use: str
    answerA: str
    answerB: str
    answerC: str
    answerD: str

@api_exam.get("/get_questions",
    response_model=List[Question],
    tags=["Questions"],
    responses={
        404: {"description": "No questions found with the provided parameters"},
        401: {"description": "Invalid credentials"},
    },
    summary="Fetch questions",
    description="Fetches questions based on the provided test type and categories."
)
def get_questions(question_params: Question_set_params, user: str = Depends(verify_user)):

    """Fetches questions based on the provided test type and categories."""

    # Check if the file exists
    try:
        df = pd.read_csv("questions.csv")
    except FileNotFoundError as e:
        raise FileNotFoundError("The questions file could not be found") from e

    # Filter the questions based on the test type and categories
    filtered_df = df[(df["use"] == question_params.use) & (df["subject"] == question_params.subject)]

    # Check if we have questions in the df
    if filtered_df.empty:
        raise HTTPException(status_code=404, detail="No questions found with the provided parameters")

    try:
        # Replace NA values with "-"
        filtered_df = filtered_df.fillna("-")

        # Convert to list of dictionaries
        questions = filtered_df.to_dict(orient='records')

        # Return a random selection
        return random.sample(questions, min(len(questions), question_params.number_questions))

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {str(e)}")

        # Return an appropriate error response to the client
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while processing the request. SEE GET QUESTIONS")




@api_exam.post("/create_question")
def create_question(question: Question, user: str = Depends(verify_user)):
    # Check if the user is an admin
    if user != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create new questions")

    try:
        df = pd.read_csv("questions.csv")
    except FileNotFoundError as e:
        raise FileNotFoundError("The questions file could not be found") from e

    # Add the new question to the database
    try:
        # Convert to dictionary the
        new_question = question.model_dump()

        # Convert the dictionary to a DataFrame
        new_data = pd.DataFrame([new_question])

        # Concatenate the original DataFrame and the new DataFrame
        df = pd.concat([df, new_data], ignore_index=True)

        # Write to CSV
        df.to_csv("questions.csv", index=False)
        return new_question
    
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {str(e)}")

        # Return an appropriate error response to the client
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while processing the request. SEE CREATE QUESTION")


