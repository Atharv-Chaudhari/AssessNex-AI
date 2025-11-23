from fastapi import APIRouter
from models.question_models import QuestionGenerationRequest
from ai.generator import generate_mcq, generate_descriptive, generate_mix

question_router = APIRouter()

@question_router.post("/questions")
def generate_questions(request: QuestionGenerationRequest):
    if request.type == "mcq":
        return generate_mcq(request.context_text, request.difficulty, request.num_questions)
    elif request.type == "descriptive":
        return generate_descriptive(request.context_text, request.difficulty, request.num_questions)
    else:
        return generate_mix(request.context_text, request.difficulty, request.num_questions)
