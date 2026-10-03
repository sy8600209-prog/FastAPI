from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
# use of path function use for  variable path info
import json

# pydantic concepts
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",examples=['P001'])]
    name:Annotated[str,Field(...,description="name of te patient")]
    city:str
    age:Annotated[int,Field(...,gt=0,lt=120,description="age of the patient")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,gt=0,description='height of the patients in kgs')]
    weight:Annotated[float,Field(...,gt=0,descirption="weight of teh patient")]


    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "underweight"
        elif self.bmi<25:
            return "normal"
        elif self.bmi<30:
            return "normal"
        else:
            return "obese"


def dataload():
    with open('data.json','r') as f:
        data=json.load(f)
        return data # return dict

def save_data(data):
    with open('data.json','w') as f:
        json.dump(data,f)


@app.get("/")
def hello():
    return{"message":"hello world"}

@app.get("/about")
def about():
    return{"message":" sagar yadav b tech second year student"}

@app.get("/view")
def view():
    data=dataload() 
    return data




# DYNAMIC PATH

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description="ID of the patient in the DB",example="P001")):
    #load all the patinet
    data=dataload()
    if(patient_id in data):
       return data[patient_id] 
    
    # return {"ERROR":"patinet not found"} in this status code is 200 

    raise HTTPException(status_code=404,detail="patient not found")

    # query perameter
@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description="sort by on the basis of height,weight or bmi"),order:str=Query('asc',description="sort in asc and desc order")):
    valid_field=['height','weight','bmi']

    if sort_by not in valid_field:
        raise HTTPException(satus_code=400,detail="invalid field select from {valid_field}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail="invalid order between asc and desc")

    data=dataload()
    sort_order=True if order=="desc" else False 
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data


# post
@app.post('/create')
def create_patient(patient:Patient):

    # load existing data
    data=dataload()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail="patient alread exists")
    # new patients add to the data base
    data[patient.id]=patient.model_dump(exclude=["id"])# pydentic object to dict

    # save into json file
    save_data(data)

    return JSONResponse(status_code=201,content={"message":"patient created successfully"})

