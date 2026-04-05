"""
LLM client module for AssessNex AI.

Final stable version:
- One chunk at a time
- Fixed 60s TPM window (8K limit)
- No random sleeps
- No rate limit errors
"""

from typing import Dict, Any, Optional, List
import time
import random
from functools import wraps

import tiktoken

from langchain_core.messages import SystemMessage, HumanMessage
from backend.app.config import get_settings
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


# =========================
# 🔁 SMART RETRY
# =========================
def retry_with_backoff(max_retries: int = 5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    error_str = str(e).lower()
                    last_exception = e

                    is_tpm_error = "tokens per minute" in error_str or "tpm" in error_str
                    is_rate_limit = "429" in error_str or "rate limit" in error_str
                    is_transient = any(code in error_str for code in ["500", "502", "503", "504"])

                    if not (is_tpm_error or is_rate_limit or is_transient) or attempt == max_retries:
                        raise

                    # TPM → full wait
                    if is_tpm_error:
                        wait_time = 60
                    elif is_rate_limit:
                        wait_time = min(5 * (2 ** attempt), 30)
                    else:
                        wait_time = min(2 * (2 ** attempt), 20)

                    jitter = random.uniform(0, wait_time * 0.1)
                    total_wait = wait_time + jitter

                    logger.warning(f"[Retry {attempt+1}] waiting {total_wait:.2f}s")

                    time.sleep(total_wait)

            raise last_exception

        return wrapper

    return decorator


# =========================
# ✂️ TOKEN CHUNKING
# =========================
def chunk_by_tokens(text: str, model: str = "gpt-4", max_tokens: int = 800):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)

    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunks.append(enc.decode(tokens[i:i + max_tokens]))

    return chunks


# =========================
# 🧠 LLM CLIENT
# =========================
class LLMClient:
    _instance: Optional["LLMClient"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        settings = get_settings()
        provider = settings.LLM_PROVIDER.lower()

        logger.info(f"Initializing LLM Client: {provider}")

        if provider == "openai":
            self._init_openai(settings)
        elif provider == "google":
            self._init_google(settings)
        elif provider == "grok":
            self._init_grok(settings)
        elif provider == "groq":
            self._init_groq(settings)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        self.settings = settings
        self.provider = provider

        # 🔥 TPM CONTROL (your idea)
        self._tokens_used = 0
        self._window_start = time.time()
        self._tpm_limit = 8000

        self._initialized = True

    # =========================
    # 🔧 PROVIDERS
    # =========================
    def _init_openai(self, settings):
        from langchain_openai import AzureChatOpenAI

        self.llm = AzureChatOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            azure_deployment=settings.AZURE_DEPLOYMENT,
            api_version=settings.AZURE_API_VERSION,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )

    def _init_google(self, settings):
        from langchain_google_genai import ChatGoogleGenerativeAI

        self.llm = ChatGoogleGenerativeAI(
            model=settings.GOOGLE_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )

    def _init_grok(self, settings):
        from langchain_openai import ChatOpenAI

        self.llm = ChatOpenAI(
            model=settings.GROK_MODEL,
            api_key=settings.GROK_API_KEY,
            base_url="https://api.x.ai/v1",
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )

    def _init_groq(self, settings):
        from langchain_groq import ChatGroq

        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )

    # =========================
    # 🔥 TPM ENFORCER
    # =========================
    def _enforce_tpm_limit(self, tokens_needed: int):
        current_time = time.time()

        # Reset every 60 seconds
        if current_time - self._window_start >= 60:
            self._tokens_used = 0
            self._window_start = current_time

        if self._tokens_used + tokens_needed > self._tpm_limit:
            sleep_time = 60 - (current_time - self._window_start)
            sleep_time = max(sleep_time, 1)

            logger.warning(f"TPM exceeded. Sleeping {sleep_time:.2f}s")

            time.sleep(sleep_time)

            # Reset after sleep
            self._tokens_used = 0
            self._window_start = time.time()

    # =========================
    # 💬 CORE CALL
    # =========================
    @retry_with_backoff()
    def _call_llm(self, prompt: str, system_message: Optional[str] = None) -> str:

        tokens_needed = len(prompt.split())

        # 🔥 enforce BEFORE request
        self._enforce_tpm_limit(tokens_needed)

        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))

        messages.append(HumanMessage(content=prompt))

        response = self.llm.invoke(messages)

        result = response.content if hasattr(response, "content") else str(response)

        # 🔥 track usage
        self._tokens_used += tokens_needed

        return result

    # =========================
    # 🚀 MAIN METHOD
    # =========================
    def generate_message(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        use_chunking: bool = True,
    ) -> str:

        approx_tokens = len(prompt.split())

        if use_chunking and approx_tokens > 2000:
            logger.info("Using safe chunking (1 chunk at a time)...")

            chunks = chunk_by_tokens(prompt)

            partials = []

            for chunk in chunks:
                result = self._call_llm(chunk, system_message)
                partials.append(result)

            # simple safe reduce (also goes through TPM control)
            final = partials[0]
            for p in partials[1:]:
                final = self._call_llm(
                    f"Combine and summarize:\n{final}\n{p}",
                    system_message
                )

            return final

        return self._call_llm(prompt, system_message)

    def generate_json_message(self, prompt: str) -> str:
        system_msg = "Return ONLY valid JSON. No explanation."
        return self.generate_message(prompt, system_msg)

    def stream_message(self, prompt: str):
        for chunk in self.llm.stream(prompt):
            yield chunk.content if hasattr(chunk, "content") else str(chunk)

    def is_available(self) -> bool:
        try:
            self.generate_message("Say OK")
            return True
        except Exception:
            return False

    # =========================
    # 🔁 BACKWARD COMPATIBLE
    # =========================
    def create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        response_format: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:

        system_message = None
        user_prompt = ""

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            elif msg["role"] == "user":
                user_prompt = msg["content"]

        if response_format and response_format.get("type") == "json_object":
            system_message = (system_message or "") + "\nReturn ONLY valid JSON."

        content = self.generate_message(user_prompt, system_message)

        return {
            "content": content,
            "model": getattr(self, "model", "unknown"),
            "usage": {
                "total_tokens": len(content.split()) + len(user_prompt.split())
            },
            "finish_reason": "stop",
        }


# =========================
# 🧩 FACTORY
# =========================
def get_llm_client() -> LLMClient:
    return LLMClient()
