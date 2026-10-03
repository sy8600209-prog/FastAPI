# FastAPI Project

A beginner-friendly project built with **FastAPI**, **SQLite**, and **Streamlit** to understand how APIs work and how they are used in real applications.

## Introduction

### What is an API?

An API (Application Programming Interface) is a way for one program to talk to another program.

```
Client (browser / app)  ->  API  ->  Server (logic + model + database)
```

Example: in a restaurant, the customer is the client, the waiter is the API, and the kitchen is the server.

### What is FastAPI?

FastAPI is a modern Python framework used to build APIs quickly. It is fast, simple, and beginner friendly.

**Key features:**

- High performance (built on Starlette and Pydantic)
- Automatic data validation using Pydantic
- Automatic interactive docs at `/docs`
- Supports `async` and `await`
- Uses Python type hints for clean code
- Easy to test and deploy

### My first FastAPI code

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "hello world"}
```

Run it:

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs

## Uses of FastAPI

### 1. Serving machine learning models
The most common use in ML. A trained model is wrapped in an API, and any app can send input and get a prediction.

```python
@app.post("/predict")
def predict(data: InputData):
    return {"prediction": model.predict([data.features]).tolist()}
```

### 2. Backend for web and mobile apps
A website or mobile app sends requests to FastAPI to save data, log in users, or fetch information.

### 3. Connecting a database
FastAPI works with SQLite, PostgreSQL, MySQL, and MongoDB, so apps can store and read data safely.

### 4. LLM and RAG applications
Chatbots, document search, and AI assistants are usually exposed through FastAPI endpoints.

### 5. Microservices
Large systems are split into small services. FastAPI is popular for building each small service.

### 6. Connecting different systems
One company's software can share data with another through APIs (payments, maps, notifications).

### 7. Data and automation pipelines
Used in MLOps for triggering jobs, batch predictions, monitoring, and sending results to dashboards.

### 8. File handling
Upload images, PDFs, and CSV files for processing (image classification, OCR, document analysis).

### 9. Frontend + backend separation
One API can serve many clients at the same time: Streamlit, React website, and a mobile app.

```
Streamlit  --\
Website    ----> FastAPI --> Database / ML Model
Mobile app --/
```

## Uses of This Project

- Learn how GET and POST requests work
- Understand routes and decorators
- Practice SQL (CREATE, INSERT, SELECT) with SQLite
- Understand how a frontend (Streamlit) talks to a backend (FastAPI)
- Base project for adding an ML model `/predict` endpoint
- Practice before deploying on AWS

## Why FastAPI Over Flask?

| | Flask | FastAPI |
|---|---|---|
| Released | 2010 | 2018 |
| Data validation | Manual | Automatic |
| API docs | Manual | Automatic |
| Async support | Limited | Built in |
| Best for | Small apps | APIs and ML serving |

## Tech Stack

- FastAPI
- Uvicorn (ASGI web server)
- Pydantic
- SQLite
- Streamlit (optional frontend)

## Project Structure

```
Fastapi/
├── main.py
├── app.py            # Streamlit frontend
├── mydata.db         # created automatically
└── README.md
```

## How to Run

```bash
pip install fastapi uvicorn streamlit requests

# Terminal 1 (backend)
uvicorn main:app --reload

# Terminal 2 (frontend)
streamlit run app.py
```

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Streamlit: http://localhost:8501

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Add a new user |
| GET | `/users` | Get all users |

## Future Improvements

- [ ] Add PUT and DELETE routes
- [ ] Add API key authentication
- [ ] Add an ML model `/predict` endpoint
- [ ] Dockerize the app
- [ ] Deploy on AWS

## License

For learning purposes.
