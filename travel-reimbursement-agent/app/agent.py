# from langchain_google_genai import ChatGoogleGenerativeAI

# from app.config import (
#     GOOGLE_API_KEY,
#     MODEL_NAME
# )

# from app.prompts import SYSTEM_PROMPT
# import json
# from app.schemas import DecisionResponse


# class TravelApprovalAgent:

#     def __init__(self):

#         self.llm = ChatGoogleGenerativeAI(

#             model=MODEL_NAME,

#             google_api_key=GOOGLE_API_KEY,

#             temperature=0

#         )

#     def build_prompt(

#             self,

#             claim,

#             policy,

#             limits,

#             receipts,

#             duplicates,

#             approver,

#             financials,

#             business_decision

#     ):

#         prompt = f"""

#     {SYSTEM_PROMPT}

#     ============================

#     CLAIM

#     {claim}

#     ============================

#     POLICY

#     {policy}

#     ============================

#     LIMIT CHECK

#     {limits}

#     ============================

#     RECEIPTS

#     {receipts}

#     ============================

#     DUPLICATES

#     {duplicates}

#     ============================

#     APPROVER

#     {approver}

#     ============================

#     BUSINESS DECISION

#     Decision:
#     {business_decision["decision"]}

#     Approved Amount:
#     {business_decision["approved_amount"]}

#     Rejected Amount:
#     {business_decision["rejected_amount"]}

#     Missing Documents:
#     {business_decision["missing_documents"]}

#     This business decision is FINAL.

#     Do NOT change it.

#     Do NOT calculate monetary values.

#     Your job is ONLY to explain WHY this decision was made.
    
#     ============================

#     IMPORTANT

#     The reimbursement decision has already been determined by the Business Decision Engine.

#     Do NOT change the decision.

#     Do NOT calculate any monetary values.

#     Only:

#     1. Explain the decision.
#     2. Mention the relevant policy.
#     3. Provide a confidence score.
#     4. Return valid JSON.

#     """

#         return prompt

#     def evaluate(
#             self,
#             claim,
#             policy,
#             limits,
#             receipts,
#             duplicates,
#             approver,
#             financials,
#             business_decision
#     ):

#         prompt = self.build_prompt(
#             claim,
#             policy,
#             limits,
#             receipts,
#             duplicates,
#             approver,
#             financials,
#             business_decision
#         )

#         response = self.llm.invoke(prompt)

#         text = response.content.strip()

#         if text.startswith("```json"):
#             text = text.replace("```json", "")

#         if text.endswith("```"):
#             text = text.replace("```", "")

#         text = text.strip()

#         try:

#             data = json.loads(text)

#             decision = DecisionResponse(**data)

#             return decision.model_dump()

#         except Exception as e:

#             return {
#                 "decision": "Manual Review",
#                 "approved_amount": financials["approved_amount"],
#                 "rejected_amount": financials["rejected_amount"],
#                 "confidence": 0.4,
#                 "missing_documents": [],
#                 "policy_references": [],
#                 "explanation": f"Unable to parse Gemini response. {str(e)}"
#             }









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

RELEVANT POLICY

{policy}

================================================

BUSINESS DECISION

{json.dumps(business_decision, indent=4)}

================================================

IMPORTANT INSTRUCTIONS

The Business Decision Engine has ALREADY made the decision.

DO NOT recalculate any amount.

DO NOT modify:

- decision
- approved_amount
- rejected_amount
- approver

Your ONLY job is:

1. Explain WHY the decision was made.

2. Mention relevant policy references.

3. Generate confidence score between 0 and 1.

Return ONLY valid JSON.

Expected Output:

{{
    "confidence": 0.98,
    "policy_references":[
        "...",
        "..."
    ],
    "explanation":"..."
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