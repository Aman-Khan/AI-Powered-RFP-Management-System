from openai import OpenAI
from app.core.llm.base import BaseLLM
from app.core.config import settings

class OpenAILLM(BaseLLM):
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def generate_rfp_structure(self, text: str):
        prompt = f"""
        Convert this procurement request into STRICT JSON:
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

        Request: {text}
        """

        resp = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return resp.choices[0].message["content"]

    async def extract_vendor_proposal(self, raw_text: str):
        prompt = f"""
        Extract vendor proposal into JSON:
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

        Vendor email:
        {raw_text}
        """

        resp = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return resp.choices[0].message["content"]
