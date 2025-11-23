from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from config import UPLOAD_FOLDER, ALLOWED_DOC_TYPES

upload_router = APIRouter()

@upload_router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()

    if ext not in ALLOWED_DOC_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed")

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    save_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(save_path, "wb") as f:
        f.write(await file.read())

    return {"message": "File uploaded", "path": save_path}
