from app.core.prisma import prisma
from app.utils.ids import new_id
from app.core.llm.factory import get_llm

async def create_rfp(text: str, userId: str):
    llm = get_llm()

    prompt = f"""
    Convert this procurement request into structured JSON:
    Fields: budget, items, quantities, warranty, delivery_days, payment_terms.
    Input: {text}
    """

    structured = await llm.generate_json(prompt)

    return await prisma.rfp.create(
        data={
            "id": new_id(),
            "userId": userId,
            "title": "Auto-generated RFP",
            "description": text,
            "structuredRequirements": structured,
        }
    )
