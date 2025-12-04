from groq import Groq
from app.core.llm.base import BaseLLM
from app.core.config import settings

class GroqLLM(BaseLLM):
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    async def generate_rfp_structure(self, text: str):
        prompt = f"""
        Create STRICT JSON RFP structure:
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

        resp = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message["content"]

    async def extract_vendor_proposal(self, raw_text: str):
        prompt = f"""
        Parse vendor proposal into JSON:
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

        Vendor Email:
        {raw_text}
        """

        resp = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message["content"]
