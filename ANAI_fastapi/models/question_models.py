from pydantic import BaseModel

class QuestionGenerationRequest(BaseModel):
    difficulty: str  # easy, medium, hard
    num_questions: int
    type: str  # mcq, descriptive, mix
    context_text: str  # extracted text from documents
