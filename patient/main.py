from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
# use of path function use for  variable path info
import json

# pydantic concepts
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

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
# second pydentic model for update
class PatientsUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(...,gt=0,lt=120,description="age of the patient")]
    gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]

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



# update and delete patients
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientsUpdate):
    data=dataload()
    if patient_id  not in data:
        raise HTTPException(status_code=404,detail="patient id is not correct")
    ex_data=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True) # to dict and exclude_unset=True for given data values include

    for key ,values in updated_patient_info.items():
        ex_data[key]=values

    # ex_data->pydentic object->updated bmi +verdict -> pydentic object ->dict
    ex_data['id']=patient_id
    patient_pydenti_objc=Patient(**ex_data)

    ex_data=patient_pydenti_objc.model_dump(exclude='id')
    data[patient_id]=ex_data

    # save data
    save_data(data)

    return JSONResponse(status_code=200,content={"message":"patient updated"})




# delete
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):

    # load data
    data=dataload()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patients not found")
    del data[patient_id]

    save_data(data)

    raise JSONResponse(status_code=200, content={"message":"patient delete successfully"})

