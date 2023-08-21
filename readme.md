# FastAPI Exam API

This README presents the architecture choices and features of the FastAPI Exam API. This API provides endpoints for managing exam questions.

## Architecture Choices

### Pandas

Pandas is used for managing and manipulating the dataset of questions. It provides powerful data structures to make working with structured data fast, easy, and expressive.

### Pydantic

Pydantic is used for data validation by defining how data should be in pure Python, and it provides a clear and informative error message when data is invalid.

### Basic Authentication

HTTP Basic Authentication is used for simplicity. However, for a production application, a more secure authentication method like OAuth2 should be used.

## API Endpoints

### Healthcheck

A healthcheck endpoint is provided to verify the API is functional.

### Get Questions

The get_questions endpoint allows users to fetch a set of questions based on their preferences. Users must provide their credentials for authentication, and specify the following parameters:

- use: The type of test.
- subject: The subject of the test.
- number_questions: The number of questions to fetch (must be 5, 10, or 15).
If no questions are found that match the provided parameters, the API returns a 404 error.
If an invalid number of questions is provided, the API returns a 400 error.

### Error Handling

The API uses FastAPI's exception handlers to manage errors. If an error occurs, the API returns an HTTP error with a helpful error message.

## Future Improvements

- Use a more secure authentication method.
- Add rate limiting to prevent abuse.
- Improve code organization by splitting code into multiple files.
- Add tests using Pytest and FastAPI's TestClient.