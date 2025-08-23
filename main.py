from fastapi import FastAPI

app = FastAPI(title="Version Control System")


@app.get("/")
def readroot():
    return {"message": "welcome"}
