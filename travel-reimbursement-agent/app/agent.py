import json

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import (
    GOOGLE_API_KEY,
    MODEL_NAME
)

from app.prompts import SYSTEM_PROMPT


class TravelApprovalAgent:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(

            model=MODEL_NAME,

            google_api_key=GOOGLE_API_KEY,

            temperature=0

        )

    # ======================================================
    # Prompt Builder
    # ======================================================

    def build_prompt(

        self,

        claim,

        policy,

        business_decision

    ):

        prompt = f"""

{SYSTEM_PROMPT}

================================================

EMPLOYEE CLAIM

{json.dumps(claim, indent=4)}

================================================

# FLIGHT DETAILS

# Flight Type:
# {claim.get("flight_type")}

# Flight Fare:
# ₹{claim.get("flight_fare")}

================================================

RELEVANT POLICY

{policy}

================================================

BUSINESS DECISION (FINAL)

{json.dumps(business_decision, indent=4)}

The above decision has already been finalized by the Business Decision Engine.

Use it exactly as provided.

================================================

IMPORTANT INSTRUCTIONS

The Business Decision Engine has already completed all reimbursement calculations.

The Business Decision Engine has already determined:

• Final Decision
• Approved Amount
• Rejected Amount
• Expense-wise Breakdown
• Required Approver

DO NOT perform any calculations.

DO NOT change:

- decision
- approved_amount
- rejected_amount
- approver
- expenses

Your ONLY responsibilities are:

1. Explain why each expense was approved, partially approved, or rejected.

2. Explain how the company policy was applied.

3. Mention the policy sections used for the decision.

4. Generate a confidence score between 0 and 1.

The explanation should specifically mention:

• Hotel reimbursement
• Meal reimbursement
• Taxi reimbursement
• Flight reimbursement (based on flight type and fare)
• Shopping expenses (if present)
• Missing receipts (if any)
• Duplicate receipts (if any)

If no receipts were uploaded, clearly state that the claim requires Manual Review because supporting documents are mandatory for reimbursement.

Return ONLY valid JSON.

Expected Output:

{{
    "confidence": 0.97,

    "policy_references": [

        "Hotel Expense Policy",

        "Flight Expense Policy"

    ],

    "explanation": "Provide a concise explanation of how the Business Decision Engine applied the reimbursement policy. Do not mention calculations that are not already present in the Business Decision."
}}

"""

        return prompt

    # ======================================================
    # LLM
    # ======================================================

    def evaluate(

        self,

        claim,

        policy,

        business_decision

    ):

        prompt = self.build_prompt(

            claim,

            policy,

            business_decision

        )

        response = self.llm.invoke(prompt)

        text = response.content.strip()

        if text.startswith("```json"):

            text = text.replace("```json", "")

        if text.endswith("```"):

            text = text.replace("```", "")

        text = text.strip()

        try:

            data = json.loads(text)

        except Exception:

            data = {

                "confidence": 0.80,

                "policy_references": [],

                "explanation": text

            }

        return json.dumps(data)