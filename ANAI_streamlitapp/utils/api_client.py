# app/utils/api_client.py
"""API Client for AssessNex AI - handles mock and real API calls"""
import time
import random
import io
import requests
import json
from typing import Dict, Any, Optional, List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import ENDPOINTS, ENABLE_MOCKS, MOCK_RESPONSES

def _simulate_latency():
    """Simulate network latency for better UX"""
    time.sleep(0.4 + random.random() * 0.3)

def post(endpoint_key: str, data: Dict = None, files: List = None, headers: Dict = None) -> Dict:
    """POST request to API"""
    url = ENDPOINTS.get(endpoint_key, endpoint_key)
    if ENABLE_MOCKS and endpoint_key in MOCK_RESPONSES:
        _simulate_latency()
        return MOCK_RESPONSES[endpoint_key](data if data is not None else files)
    else:
        # For real API: handle file uploads
        files_payload = None
        if files:
            files_payload = []
            for f in files:
                name = getattr(f, 'name', getattr(f, 'filename', str(f)))
                try:
                    content = f.getvalue() if hasattr(f, 'getvalue') else None
                except Exception:
                    content = None
                if content is not None:
                    files_payload.append(("files", (name, io.BytesIO(content), "application/octet-stream")))
        
        try:
            resp = requests.post(url, json=data, files=files_payload or None, headers=headers or {}, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

def get(endpoint_key: str, params: Dict = None, headers: Dict = None) -> Dict:
    """GET request to API"""
    url = ENDPOINTS.get(endpoint_key, endpoint_key)
    if ENABLE_MOCKS and endpoint_key in MOCK_RESPONSES:
        _simulate_latency()
        return MOCK_RESPONSES[endpoint_key](params if params is not None else {})
    else:
        try:
            resp = requests.get(url, params=params, headers=headers or {}, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

def put(endpoint_key: str, data: Dict = None, headers: Dict = None) -> Dict:
    """PUT request to API"""
    url = ENDPOINTS.get(endpoint_key, endpoint_key)
    if ENABLE_MOCKS:
        _simulate_latency()
        return {"success": True, "message": "Updated (mock)"}
    else:
        try:
            resp = requests.put(url, json=data, headers=headers or {}, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
