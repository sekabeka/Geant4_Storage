from fastapi import FastAPI, File, UploadFile, responses
from pydantic import BaseModel

from storage import Storage
app = FastAPI()

class DataOfFile(BaseModel):
    filename: str

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    storage = Storage(
        file.filename,
        await file.read()
    )
    status = await storage.upload()
    if status:
        return {
            "message": "success."
        }
    return {
        "message": "file already exists.",
    }

@app.post("/update/")
async def update_file(file: UploadFile = File(...)):
    storage = Storage(
        file.filename,
        await file.read()
    )
    status = await storage.update()
    if status:
        return {
            "message": "success."
        }
    return {
        "message": "file not found.",
    }

@app.post("/remove/")
async def remove_file(file: DataOfFile):
    filename = file.filename
    storage = Storage(
        filename=filename
    )
    status = await storage.remove()
    if status:
        return {
            "message": "file is removed."
        }
    return {
        "message": "file not found or other reasons."
    }

@app.post("/retrieve/")
async def retrieve_file(file: DataOfFile):
    filename = file.filename
    storage = Storage(
        filename=filename
    )
    filepath = await storage.retrieve()
    if filepath is None:
        return {
            "message": "file not found."
        }
    return responses.FileResponse(
        path=filepath, filename=filename
    )

    
