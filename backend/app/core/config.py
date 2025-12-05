import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Email system (SMTP + IMAP)
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASS: str = os.getenv("SMTP_PASS")
    IMAP_HOST: str = os.getenv("IMAP_HOST")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM")

    # LLM Providers
    SENDGRID_KEY: str = os.getenv("SENDGRID_API_KEY")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")


settings = Settings()
