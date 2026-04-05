"""
LLM client module for AssessNex AI.

Supports:
- Azure OpenAI
- Google Gemini
- Grok
- Groq

Includes:
- Retry with exponential backoff
- Token-based chunking
- Map-Reduce summarization for large inputs
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
# 🔁 RETRY DECORATOR
# =========================
def retry_with_backoff(max_retries: int = 5, min_wait: float = 1, max_wait: float = 60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e)
                    last_exception = e

                    is_retryable = any(
                        x in error_str.lower()
                        for x in ["429", "rate", "tpm", "rpm", "500", "502", "503", "504"]
                    )

                    if not is_retryable or attempt == max_retries:
                        raise

                    wait_time = min(min_wait * (2 ** attempt), max_wait)
                    jitter = random.uniform(0, wait_time * 0.1)

                    total_wait = wait_time + jitter

                    logger.warning(
                        f"[Retry {attempt+1}] {error_str} → waiting {total_wait:.2f}s"
                    )

                    time.sleep(total_wait)

            raise last_exception

        return wrapper

    return decorator


# =========================
# ✂️ TOKEN CHUNKING
# =========================
def chunk_by_tokens(text: str, model: str = "gpt-4", max_tokens: int = 2000):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)

    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = enc.decode(tokens[i : i + max_tokens])
        chunks.append(chunk)

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
    # 💬 CORE GENERATION
    # =========================
    @retry_with_backoff()
    def _call_llm(self, prompt: str, system_message: Optional[str] = None) -> str:
        messages = []

        if system_message:
            messages.append(SystemMessage(content=system_message))

        messages.append(HumanMessage(content=prompt))

        response = self.llm.invoke(messages)

        return response.content if hasattr(response, "content") else str(response)

    # =========================
    # 🚀 PUBLIC METHODS
    # =========================
    def generate_message(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        use_chunking: bool = True,
    ) -> str:
        """
        Auto handles:
        - Token overflow
        - Rate limiting
        """

        # 🔹 Estimate tokens
        approx_tokens = len(prompt.split())

        # 🔴 If too large → chunk
        if use_chunking and approx_tokens > 3000:
            logger.info("Using chunking strategy...")

            chunks = chunk_by_tokens(prompt)

            partials = []

            for chunk in chunks:
                result = self._call_llm(chunk, system_message)
                partials.append(result)

                # ✅ throttle (VERY IMPORTANT)
                time.sleep(0.5)

            # 🔹 Reduce step
            final = self._call_llm(
                "Combine and summarize:\n" + "\n".join(partials),
                system_message,
            )

            return final

        # 🟢 Normal call
        return self._call_llm(prompt, system_message)

    def generate_json_message(self, prompt: str) -> str:
        system_msg = (
            "Return ONLY valid JSON. No explanation, no markdown, no extra text."
        )
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
# 🧩 FACTORY
# =========================
def get_llm_client() -> LLMClient:
    return LLMClient()
