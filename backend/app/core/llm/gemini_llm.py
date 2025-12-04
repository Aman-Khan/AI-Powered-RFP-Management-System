import google.generativeai as genai
from app.core.llm.base import BaseLLM
from app.core.config import settings

class GeminiLLM(BaseLLM):
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-flash-latest", generation_config={"response_mime_type": "application/json"})

    async def generate_rfp_structure(self, text: str):
        prompt = f"""
        Convert this procurement text into STRICT JSON:
        {{
          "summary": "",
          "budget": 0,
          "items": [
            {{ "name": "", "quantity": 0, "specs": {{}} }}
          ],
          "delivery_days": 0,
          "payment_terms": "",
          "warranty": "",
          "additional_requirements": []
        }}
        Input: {text}
        """

        resp = self.model.generate_content(prompt)
        return resp.text

    async def extract_vendor_proposal(self, raw_text: str):
        prompt = f"""
        Convert vendor email into JSON:
        {{
          "items": [
            {{
              "name": "",
              "unit_price": 0,
              "quantity": 0,
              "total_price": 0,
              "specs": {{}}
            }}
          ],
          "taxes": 0,
          "delivery_time": "",
          "payment_terms": "",
          "warranty": "",
          "notes": ""
        }}

        Email:
        {raw_text}
        """

        resp = self.model.generate_content(prompt)
        return resp.text
