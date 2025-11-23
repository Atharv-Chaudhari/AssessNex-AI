from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.upload_router import upload_router
from routes.question_router import question_router
from routes.assignment_router import assignment_router
from auth.auth_router import auth_router

app = FastAPI(title="AssessNex AI Backend",
              description="Automated Question Paper & Assignment Generator",
              version="1.0.0")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(upload_router, prefix="/upload")
app.include_router(question_router, prefix="/generate")
app.include_router(assignment_router, prefix="/assignment")

@app.get("/")
def home():
    return {"status": "AssessNex AI API running!"}
