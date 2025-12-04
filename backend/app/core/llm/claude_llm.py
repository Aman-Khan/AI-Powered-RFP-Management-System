import anthropic
from app.core.llm.base import BaseLLM
from app.core.config import settings

class ClaudeLLM(BaseLLM):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.claude_api_key)

    async def generate_rfp_structure(self, text: str):
        prompt = f"""
        Produce STRICT JSON RFP:
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

        Text: {text}
        """

        resp = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        return resp.content[0].text

    async def extract_vendor_proposal(self, raw_text: str):
        prompt = f"""
        Parse vendor proposal into STRICT JSON:
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

        resp = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.content[0].text
