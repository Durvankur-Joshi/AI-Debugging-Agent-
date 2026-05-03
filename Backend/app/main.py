from fastapi import FastAPI
from app.api.routes import router 
from app.api.upload import router as  upload_router


app = FastAPI(title="AI Debugging Agent")

app.include_router(router)
app.include_router(upload_router)

@app.get("/")
def home():
    return("Everthing is working...")

