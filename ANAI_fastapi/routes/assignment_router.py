from fastapi import APIRouter
from typing import List

assignment_router = APIRouter()

@assignment_router.post("/create")
def create_assignment(questions: List[dict], title: str = "Generated Assignment"):
    return {
        "title": title,
        "total_questions": len(questions),
        "questions": questions
    }
