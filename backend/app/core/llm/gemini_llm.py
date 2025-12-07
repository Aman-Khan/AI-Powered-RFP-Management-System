import google.generativeai as genai
from app.core.llm.base import BaseLLM
from app.core.config import settings
from typing import Any, Dict
import re
import json

class GeminiLLM(BaseLLM):
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-flash-latest", generation_config={"response_mime_type": "application/json"})

    async def is_proposal_email(self, text: str) -> bool:
      """
      Uses LLM to classify whether email is a vendor PROPOSAL.
      """

      prompt = f"""
      Determine whether the following email contains a vendor's commercial PROPOSAL or quotation.
      Respond ONLY with "YES" or "NO".

      Email:
      {text}
      """

      response = self.model.generate_content(prompt)

      ans = response.text.strip().upper()

      return ans == "YES"

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

    async def generate_email_template(self, rfp: dict, user_name: str):
        """
        Generate a professional vendor email template with clean formatting,
        structured paragraphs, and editable greeting.
        Output MUST be valid JSON with subject, content, footer.
        """

        prompt = f"""
        You are an expert Procurement Communications Assistant.

        Create a **professionally formatted vendor email** based on this structured RFP:

        RFP_JSON = {rfp}

        The output MUST follow these strict rules:

        ====================================================
        GENERAL RULES
        ====================================================
        1. **Output ONLY clean VALID JSON** — no markdown, no backticks,
        no commentary, no explanations.

        2. The JSON MUST contain exactly:
        {{
            "subject": "",
            "content": "",
            "footer": ""
        }}

        3. The email must be clean, readable, and formatted using:
        - Paragraph breaks (\n\n)
        - Short, clear sentences
        - No overly long blocks of text

        ====================================================
        SUBJECT RULES
        ====================================================
        - Must be short, clear, professional.
        - Must reference the RFP (e.g., “Request for Proposal – Laptops Procurement”).

        ====================================================
        CONTENT RULES
        ====================================================
        The **content** must include the following, in order:

        1. Greeting placeholder:
        "Dear {{vendor_name}},"
        (Do not replace vendor_name; keep placeholder for dynamic use)

        2. A short introduction sentence.

        3. The purpose of the email:
        "We are reaching out to request a formal proposal for the following requirements..."

        4. A readable summary of requirements extracted from RFP_JSON.
        - Convert lists into bullet-like sentences.
        - Convert numbers/durations into natural language.
        - DO NOT add new requirements that do not exist.

        5. A request for quotation with timeline:
        "Please share your quotation and proposal details by the requested timeline."

        6. Instructions:
        - How the vendor should respond
        - Any details needed

        7. A closing clarification line:
        "Feel free to contact us for any clarification regarding this RFP."

        ====================================================
        FOOTER RULES
        ====================================================
        The **footer** MUST be EXACTLY:
        "Thanks & Regards,\\n{user_name}"

        ====================================================
        STRICT CONSTRAINTS
        ====================================================
        - DO NOT hallucinate or invent new requirements.
        - DO NOT output markdown, backticks, or explanations.
        - DO NOT wrap JSON inside ```json or any code fence.
        - Ensure the JSON is clean and parsable.

        """

        response = self.model.generate_content(prompt)
        return response.text


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

    async def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        Sends prompt to Gemini and returns **parsed JSON as dict**.
        Auto-fixes minor formatting issues.
        """

        resp = self.model.generate_content(prompt)

        text = resp.text.strip()

        # 1. Remove code fences if model accidentally adds them
        text = re.sub(r"```json|```", "", text).strip()

        # 2. Try parsing directly
        try:
            return json.loads(text)

        except json.JSONDecodeError:
            # 3. Attempt to extract only the JSON substring
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except Exception:
                    pass

        # 4. Fallback: return text for debugging
        raise ValueError(f"LLM returned invalid JSON:\n{text}")
