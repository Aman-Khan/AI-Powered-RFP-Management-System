# app/api/recommendation.py
from fastapi import APIRouter
from app.services.recommendation_service import generate_rfp_recommendation

router = APIRouter(tags=["Recommendations"])


@router.get("/{rfp_id}")
async def get_recommendations(rfp_id: str):
    """
    Returns ranked vendor proposal recommendations for a given RFP.
    """
    return await generate_rfp_recommendation(rfp_id)
