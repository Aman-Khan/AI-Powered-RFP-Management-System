from app.core.config import settings
from app.core.llm.openai_llm import OpenAILLM
from app.core.llm.gemini_llm import GeminiLLM
from app.core.llm.groq_llm import GroqLLM
from app.core.llm.claude_llm import ClaudeLLM

def get_llm():
    provider = (settings.LLM_PROVIDER or "openai").lower()

    if provider == "openai":
        return OpenAILLM()

    if provider == "gemini":
        return GeminiLLM()

    if provider == "groq":
        return GroqLLM()

    if provider == "claude":
        return ClaudeLLM()

    raise ValueError(f"Unknown LLM provider: {provider}")
