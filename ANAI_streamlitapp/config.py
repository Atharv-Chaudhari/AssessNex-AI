# config.py — central endpoints & settings for AssessNex Streamlit frontend

import time
import hashlib
import json

API_BASE = "https://api.example.com"
ENABLE_MOCKS = True

ENDPOINTS = {
    "auth_login": f"{API_BASE}/api/auth/login",
    "auth_register": f"{API_BASE}/api/auth/register",
    "auth_me": f"{API_BASE}/api/user/me",
    "upload": f"{API_BASE}/api/upload",
    "parse": f"{API_BASE}/api/parse",
    "generate_questions": f"{API_BASE}/api/generate-questions",
    "list_questions": f"{API_BASE}/api/list-questions",
    "save_exam": f"{API_BASE}/api/save-exam",
    "student_questions": f"{API_BASE}/api/student/questions",
    "list_docs": f"{API_BASE}/api/list-docs",
    "notify": f"{API_BASE}/api/notify",
    "list_emails": f"{API_BASE}/api/list-emails"
}

# Premium AI SaaS Color Palette
THEME = {
    "primary": "#3B82F6",
    "accent": "#6366F1",
    "bg": "#F8FAFC",
    "card": "#FFFFFF",
    "muted": "#64748B",
    "danger": "#EF4444",
    "text": "#1E293B",
    "soft": "#E2E8F0",
    "success": "#10B981",
    "warning": "#F59E0B",
    "dark_bg": "#0F172A",
    "gradient_start": "#3B82F6",
    "gradient_end": "#6366F1"
}

# In-memory mock store to simulate backend state
MOCK_STORE = {
    "files": [],
    "next_file_id": 1,
    "exams": [],
    "emails": []
}

def _generate_jwt(user_id, role, email):
    """Generate a simple mock JWT token"""
    header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    payload = {
        "sub": user_id,
        "role": role,
        "email": email,
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400
    }
    payload_str = json.dumps(payload)
    signature = "mock_signature_" + hashlib.md5(payload_str.encode()).hexdigest()[:16]
    return f"{header}.{payload_str}.{signature}"

def _mock_auth_login(payload):
    """Mock login endpoint"""
    email = payload.get("email", "demo@example.com")
    role = payload.get("role", "Professor")
    name = payload.get("name", "Demo User")
    
    user_id = 1
    token = _generate_jwt(user_id, role, email)
    return {
        "success": True,
        "token": token,
        "user": {"id": user_id, "name": name, "role": role, "email": email}
    }

def _mock_auth_register(payload):
    """Mock register endpoint"""
    email = payload.get("email", "")
    name = payload.get("name", "New User")
    role = payload.get("role", "Student")
    
    user_id = 2
    token = _generate_jwt(user_id, role, email)
    return {
        "success": True,
        "message": "Registration successful",
        "token": token,
        "user": {"id": user_id, "name": name, "role": role, "email": email}
    }

def _mock_auth_me(token=None):
    """Mock get current user endpoint"""
    return {
        "success": True,
        "user": {"id": 1, "name": "Current User", "role": "Professor", "email": "user@example.com"}
    }

def _mock_upload(files=None):
    """Mock file upload endpoint"""
    files = files or []
    files_out = []
    for f in files:
        fid = MOCK_STORE["next_file_id"]
        MOCK_STORE["next_file_id"] += 1
        name = getattr(f, 'name', getattr(f, 'filename', str(f)))
        try:
            content = f.getvalue() if hasattr(f, 'getvalue') else None
        except Exception:
            content = None
        rec = {"id": fid, "name": name, "bytes": content, "parsed_text": None}
        MOCK_STORE["files"].append(rec)
        files_out.append({"id": fid, "name": name, "status": "uploaded", "size": len(content) if content else 0})
    return {"success": True, "status": "ok", "files": files_out}

def _mock_parse(params=None):
    """Mock document parsing endpoint"""
    params = params or {}
    doc_id = params.get("doc_id") if isinstance(params, dict) else params
    
    doc = None
    for d in MOCK_STORE["files"]:
        if d["id"] == doc_id or d["name"] == doc_id:
            doc = d
            break
    
    if not doc:
        return {"success": False, "error": "Document not found"}
    
    parsed = """Chapter 1: Fundamentals
    
Definition: A fundamental concept in physics...

Key points:
- Point 1: Important detail
- Point 2: Another detail
- Point 3: Critical information

The mathematical formula is: E = mc²

Applications and examples in real world scenarios."""
    
    doc["parsed_text"] = parsed
    return {"success": True, "doc_id": doc["id"], "status": "parsed", "text": parsed}

def _mock_generate_questions(params=None):
    """Mock question generation endpoint"""
    params = params or {}
    
    sample_questions = [
        {"id": 101, "type": "MCQ", "text": "What is Newton's second law of motion?", "choices": ["F=ma", "E=mc²", "F=mg", "p=mv"], "answer": 0, "difficulty": "Medium", "marks": 2},
        {"id": 102, "type": "Short", "text": "Define the term 'inertia' in physics.", "answer": "Inertia is the property of matter to resist changes in motion", "difficulty": "Easy", "marks": 3},
        {"id": 103, "type": "Long", "text": "Explain Newton's three laws of motion with real-world examples.", "answer": "Detailed explanation required...", "difficulty": "Hard", "marks": 8},
        {"id": 104, "type": "MCQ", "text": "Which SI unit represents force?", "choices": ["Newton", "Pascal", "Joule", "Watt"], "answer": 0, "difficulty": "Easy", "marks": 1},
        {"id": 105, "type": "Fill", "text": "The acceleration of an object is directly proportional to _____ and inversely proportional to _____", "answer": "force, mass", "difficulty": "Medium", "marks": 2}
    ]
    
    return {"success": True, "questions": sample_questions, "meta": {"count": len(sample_questions)}}

def _mock_list_questions(params=None):
    """Mock list questions endpoint"""
    return {"success": True, "questions": []}

def _mock_save_exam(payload=None):
    """Mock save exam endpoint"""
    payload = payload or {}
    eid = 9001 + len(MOCK_STORE["exams"])
    exam = {
        "id": eid,
        "title": payload.get("title", "Untitled Exam"),
        "sections": payload.get("sections", []),
        "questions": payload.get("questions", []),
        "status": "saved",
        "timestamp": int(time.time())
    }
    MOCK_STORE["exams"].append(exam)
    return {"success": True, "exam_id": eid, "message": "Exam saved successfully"}

def _mock_student_questions(params=None):
    """Mock get assigned questions for student endpoint"""
    params = params or {}
    return {
        "success": True,
        "assigned": [
            {"id": 1001, "title": "Physics MCQ Set - Chapter 1", "due": "2025-12-15", "questions": 5},
            {"id": 1002, "title": "Mathematics Problem Set", "due": "2025-12-20", "questions": 8},
            {"id": 1003, "title": "Biology Short Answer Quiz", "due": "2025-12-22", "questions": 10}
        ]
    }

def _mock_list_docs(params=None):
    """Mock list documents endpoint"""
    docs = []
    for d in MOCK_STORE["files"]:
        docs.append({
            "id": d["id"],
            "name": d["name"],
            "parsed": bool(d.get("parsed_text")),
            "size": len(d.get("bytes", b""))
        })
    return {"success": True, "docs": docs}

def _mock_notify(payload=None):
    """Mock notification endpoint"""
    payload = payload or {}
    email_record = {
        "to": payload.get("to"),
        "subject": payload.get("subject"),
        "message": payload.get("message"),
        "timestamp": int(time.time())
    }
    MOCK_STORE["emails"].append(email_record)
    return {"success": True, "message": "Notification sent"}

def _mock_list_emails(params=None):
    """Mock list emails endpoint"""
    return {"success": True, "emails": MOCK_STORE.get("emails", [])}

# Map all endpoints to their mock handlers
MOCK_RESPONSES = {
    "auth_login": _mock_auth_login,
    "auth_register": _mock_auth_register,
    "auth_me": _mock_auth_me,
    "upload": _mock_upload,
    "parse": _mock_parse,
    "generate_questions": _mock_generate_questions,
    "list_questions": _mock_list_questions,
    "save_exam": _mock_save_exam,
    "student_questions": _mock_student_questions,
    "list_docs": _mock_list_docs,
    "notify": _mock_notify,
    "list_emails": _mock_list_emails
}
