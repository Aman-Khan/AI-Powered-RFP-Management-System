from app.core.db_client import prisma
from app.core.llm.factory import get_llm
from fastapi import HTTPException


async def generate_rfp_recommendation(rfp_id: str):
    """
    Fetch an RFP + its proposals → use AI to create a structured comparison.
    """

    # 1️⃣ Fetch RFP with vendor proposals
    rfp = await prisma.rfp.find_unique(
        where={"id": rfp_id},
        include={
            "rfpVendors": {
                "include": {
                    "vendor": True,
                    "proposals": True
                }
            }
        }
    )

    if not rfp:
        raise HTTPException(404, "RFP not found")

    # ❌ OLD: rfp["structuredRequirements"]
    # ✅ FIX:
    if not rfp.structuredRequirements:
        raise HTTPException(400, "RFP is missing structuredRequirements")

    # Collect proposals
    vendor_proposals = []
    for rv in rfp.rfpVendors:

        if rv.proposals:
            vendor_proposals.append({
                "rfpVendorId": rv.id,
                "vendor_name": rv.vendor.name,
                "proposal": rv.proposals[0].extractedData
            })

    if not vendor_proposals:
        raise HTTPException(400, "No proposals found for this RFP")

    llm = get_llm()

    # 2️⃣ Build comparison LLM prompt
    prompt = f"""
    You are a procurement evaluation expert.

    Task: Compare vendor proposals against the RFP requirements and return a 
    STRICT JSON response that ranks vendors and summarizes comparison.

    # RFP REQUIREMENTS (GROUND TRUTH)
    {rfp.structuredRequirements}

    # PROPOSALS
    {vendor_proposals}

    Return JSON ONLY in this EXACT format:

    {{
    "comparison_summary": "",
    "vendors_ranked": [
        {{
        "vendor_name": "",
        "score": 0,
        "price_total": 0,
        "delivery_match": "",
        "warranty_match": "",
        "payment_terms_match": "",
        "item_coverage_score": 0,
        "notes": ""
        }}
    ],
    "recommendation_reasoning": "",
    "recommended_vendor": ""
    }}

    Rules:
    - Score each vendor from 0–100.
    - scoring factors:
        - Pricing value & completeness (40%)
        - Item match accuracy (30%)
        - Warranty & payment terms (20%)
        - Delivery time match (10%)
    - Compute missing fields sensibly.
    - Be fair & objective.
    - Always sort vendors in DESCENDING order of score.
    """


    result = await llm.generate_json(prompt)
    return result
