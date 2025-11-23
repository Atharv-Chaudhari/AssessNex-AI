from fastapi import APIRouter, HTTPException
from models.auth_models import LoginModel
from auth.jwt_handler import create_access_token

auth_router = APIRouter()

# Dummy user DB
users = {
    "prof@test.com": {"password": "1234", "role": "professor"},
    "assistant@test.com": {"password": "1234", "role": "assistant"},
    "student@test.com": {"password": "1234", "role": "student"},
}

@auth_router.post("/login")
def login(request: LoginModel):
    if request.email not in users:
        raise HTTPException(status_code=404, detail="User not found")

    user = users[request.email]

    if request.password != user["password"]:
        raise HTTPException(status_code=401, detail="Wrong password")

    if request.role != user["role"]:
        raise HTTPException(status_code=403, detail="Role mismatch")

    token = create_access_token({"email": request.email, "role": user["role"]})

    return {"message": "Login successful", "token": token, "role": user["role"]}
