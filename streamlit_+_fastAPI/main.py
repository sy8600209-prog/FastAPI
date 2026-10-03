import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
FILE = "patients.json"


# ---------- helper functions ----------
def load_data():
    with open(FILE, "r") as f:
        return json.load(f)          # dict return hota hai


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_verdict(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


# ---------- input validation (Pydantic) ----------
class Patient(BaseModel):
    id: str
    name: str
    city: str
    age: int
    gender: str
    height: float   # meters
    weight: float   # kg


# ---------- routes ----------
@app.get("/")
def home():
    return {"message": "Patient API chal rahi hai"}


@app.get("/patients")
def get_all_patients():
    return load_data()


@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return data[patient_id]


@app.post("/patients")
def add_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")

    bmi = round(patient.weight / (patient.height ** 2), 2)

    data[patient.id] = {
        "name": patient.name,
        "city": patient.city,
        "age": patient.age,
        "gender": patient.gender,
        "height": patient.height,
        "weight": patient.weight,
        "bmi": bmi,
        "verdict": get_verdict(bmi),
    }
    save_data(data)
    return {"message": "Patient add ho gaya", "bmi": bmi, "verdict": get_verdict(bmi)}