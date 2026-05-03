from fastapi import APIRouter, UploadFile, File
import shutil
import os
import zipfile
import uuid

from app.services.ingestion import ingest_repo

router = APIRouter()

UPLOAD_DIR = "../temp_repos"


@router.post("/upload")
async def upload_repo(file: UploadFile = File(...)):
    try:

        # ✅ Generate UNIQUE project id PER upload
        project_id = str(uuid.uuid4())

        # ✅ Clean old temp folder
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)

        # ✅ Save ZIP
        zip_path = f"{UPLOAD_DIR}.zip"

        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ Extract ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(UPLOAD_DIR)

        # ✅ Ingest repo with project_id
        result = ingest_repo(UPLOAD_DIR, project_id)

        return {
            "success": True,
            "project_id": project_id,
            "data": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }