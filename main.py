# main.py
from fastapi import FastAPI, HTTPException, status
import json

# Initialize FastAPI app
app = FastAPI()

# Function to load patient data from JSON file
def load_Data():
    with open("./patients.json", "r") as f:
        return json.load(f)

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
