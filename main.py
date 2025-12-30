# main.py
from fastapi import FastAPI, HTTPException, status
import json

# Initialize FastAPI app
app = FastAPI()

# Function to load patient data from JSON file
def load_Data():
    with open("./patients.json", "r") as f:
        return json.load(f)

# Base Model : Patient

# Root endpoint
@app.get("/")
def hello_world():
    return {"message": "Patient Management System API is running."}

# Endpoint to view all patients
@app.get("/view-patients", status_code=status.HTTP_200_OK)
def view_data():
    data = load_Data()
    return {
        "message": "Data loaded successfully",
        "data": data
    }

# Endpoint to get patient by ID
@app.get("/get-patient/{patient_id}", status_code=status.HTTP_200_OK)
def get_patient_by_id(patient_id: str):
    data = load_Data()

    if patient_id not in data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return {
        "message": "Patient found",
        "data": data[patient_id]
    }

# Endpoint to Create a Patient
@app.post("/create-patient", statrus_code= status.HTTP_201_CREATED)
def create_patient(patient: dict):
    data = load_Data()

    if patient["id"] in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this ID already exists"
        )

    data[patient["id"]] = patient

    with open("./patients.json", "w") as f:
        json.dump(data, f, indent=4)

    return {
        "message": "Patient created successfully",
        "data": patient
    }