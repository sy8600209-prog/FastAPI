from fastapi import FastAPI,Path,HTTPException,Query
# use of path function use for  variable path info
import json
app=FastAPI()


def dataload():
    with open('data.json','r') as f:
        data=json.load(f)
        return data # return dict

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

