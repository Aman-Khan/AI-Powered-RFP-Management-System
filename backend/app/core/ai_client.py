from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_rfp_structure(text: str):
    prompt = f"""
    Convert this procurement request into structured JSON fields:
    budget, items, quantities, warranty, delivery_days, payment_terms.
    Input: {text}
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message["content"]


async def extract_vendor_proposal(raw_text: str):
    prompt = f"""
    Extract pricing, items, taxes, delivery_time, warranty, and payment_terms
    from this vendor email:

    {raw_text}

    Output valid JSON only.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message["content"]
