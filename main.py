from fastapi import FastAPI, HTTPException, status
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated

# Initialize FastAPI app
app = FastAPI()

# Function to load patient data from JSON file
def load_Data():
    with open("./patients.json", "r") as f:
        return json.load(f)
        
# Base Model : Patient
class Patient(BaseModel):

    id: Annotated[str, Field(..., description = "Required an ID to identify the patient")]
    name: Annotated[str, Field(...,max_length=20, description = "Name should be less than 20 characters")]  
    city: Annotated[str, Field(..., max_length=14, description = "The Patient's City")]
    age: Annotated[int, Field(..., gt = 0, description = "Age must be greater than 0")]
    gender: Annotated[str, Field(..., description = "Specify the Gender")]
    height: Annotated[int, Field(..., description = "Specify the Height in metres")]
    weight: Annotated[int, Field(..., description = "Specify the weight in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi =  round(self.weight/(self.height*self.height),2)

    @computed_field
    @property
    def verdict(self) -> str:
        if( self.bmi < 18.5):
            return "UnderWeight"
        elif (self.bmi < 25):
            return "Normal"
        elif (self.bmi < 30):
            return "OverWeight"
        else:
            return "Obese"
             
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

# Query Parameters endpoint to view patients with sorting : 
@app.get("/view", status_code=status.HTTP_200_OK)
def viewQueryGetPatients(sort_by: str = None): # Optional query parameter for sorting
    data = load_Data()
    patients = list(data.values())

    if sort_by:
        if sort_by not in patients[0]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort_by field: {sort_by}"
            )
        
        # Sort patients by the specified field
        # lambda function to extract the sort_by field from each patient dictionary
        patients.sort(key=lambda x: x[sort_by])

    return {
        "message": "Data loaded successfully",
        "data": patients
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
# @app.post("/create-patient", status_code= status.HTTP_201_CREATED)
# def create_patient(patient: dict):
#     data = load_Data()

#     if patient["id"] in data:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Patient with this ID already exists"
#         )

#     data[patient["id"]] = patient

#     # indent: 4 for pretty printing
#     with open("./patients.json", "w") as f:
#         json.dump(data, f, indent=4)

#     return {
#         "message": "Patient created successfully",
#         "data": patient
#     }

# Endpoint to Create a Patient using a BaseModel Schema
@app.put("/create-patient", status_code = status.HTTP_201_CREATED)
def create_patient(patient : Patient):
    data = load_Data()

    if patient.id in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this Id already exists"
        )
    
    data[patient.id] = patient.model_dump()

    with open("./patients.json", "w") as f:
        json.dump(data, f, indent = 4)

    return {
        "message":"Patient Created Successfully",
        "data":patient
    }

# Endpoint to Update a Patient using a BaseModel Schema
@app.put("/update-patient/{patient_id}", status_code=status.HTTP_200_OK)
def update_patient(patient_id: str, patient: Patient):
    # Load existing patient data from JSON file
    data = load_Data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient does not exist"
        )

    # Ensure path ID and body ID are same (data consistency)
    if patient_id != patient.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient ID in path and body must be same"
        )

    # Update patient data
    data[patient_id] = patient.model_dump()

    # Write updated data back to JSON file
    with open("./patients.json", "w") as f:
        json.dump(data, f, indent=4)

    return {
        "message": "Patient updated successfully",
        "data": patient
    }

# Endpoint to Delete a Patient by ID
@app.delete("/delete-patient/{patient_id}", status_code=status.HTTP_200_OK)
def delete_patient(patient_id: str):
    # Load existing patient data from JSON file
    data = load_Data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Delete patient from data
    deleted_patient = data.pop(patient_id)

    # Write updated data back to JSON file
    with open("./patients.json", "w") as f:
        json.dump(data, f, indent=4)

    return {
        "message": "Patient deleted successfully",
        "data": deleted_patient
    }
