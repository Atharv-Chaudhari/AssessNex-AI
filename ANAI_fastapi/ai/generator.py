def generate_mcq(text, difficulty, n):
    return [
        {
            "question": f"MCQ {i+1} based on {difficulty}",
            "options": ["A", "B", "C", "D"],
            "answer": "A"
        } for i in range(n)
    ]

def generate_descriptive(text, difficulty, n):
    return [
        {
            "question": f"Descriptive Question {i+1} ({difficulty})",
            "answer_hint": "Explain your reasoning."
        } for i in range(n)
    ]

def generate_mix(text, difficulty, n):
    half = n // 2
    return generate_mcq(text, difficulty, half) + generate_descriptive(text, difficulty, n - half)
