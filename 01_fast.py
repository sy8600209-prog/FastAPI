from fastapi import FastAPI

app=FastAPI()
@app.get("/") # route /
def hello():
    return {"message":"hello meous"}
@app.get("/sagar") # route /
def hello():
    return {"message":"hello sagar yadav"}


