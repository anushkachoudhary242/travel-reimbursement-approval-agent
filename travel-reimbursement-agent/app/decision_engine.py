# """
# Deterministic Business Decision Engine

# This module contains the business rules for deciding whether a
# travel reimbursement claim should be:

# 1. Approve
# 2. Partially Approved
# 3. Reject
# 4. Manual Review

# The LLM is NOT responsible for making these decisions.
# It only generates the explanation.
# """


# def make_business_decision(
#     claim: dict,
#     limits: dict,
#     receipts: dict,
#     duplicates: dict,
#     financials: dict,
# ):
#     """
#     Returns:
#     {
#         "decision": "...",
#         "approved_amount": ...,
#         "rejected_amount": ...
#     }
#     """

#     # --------------------------------------------------------
#     # Rule 1 : Duplicate Receipts
#     # --------------------------------------------------------

#     duplicate_found = duplicates.get("duplicate_found", False)

#     if duplicate_found:
#         return {
#             "decision": "Reject",
#             "approved_amount": 0,
#             "rejected_amount": (
#                 financials["approved_amount"]
#                 + financials["rejected_amount"]
#             ),
#             "missing_documents": [],
#             "confidence": 0.95
#         }

#     # --------------------------------------------------------
#     # Rule 2 : Missing Receipts / Attachments
#     # --------------------------------------------------------

#     receipts_valid = receipts.get("valid", True)

#     missing_receipts = receipts.get("missing_receipts", [])

#     missing_attachments = receipts.get("missing_attachments", [])

#     if not receipts_valid:

#         return {

#             "decision": "Manual Review",

#             "approved_amount": financials["approved_amount"],

#             "rejected_amount": financials["rejected_amount"],

#             "missing_documents":
#                 missing_receipts + missing_attachments,
#             "confidence": 0.50

#         }

#     # --------------------------------------------------------
#     # Rule 3 : Business Class Flight
#     # --------------------------------------------------------

#     flight = claim.get("flight", "")

#     if str(flight).lower() == "business":

#         return {
#             "decision": "Reject",
#             "approved_amount": 0,
#             "rejected_amount": (
#                 financials["approved_amount"]
#                 + financials["rejected_amount"]
#             ),
#             "missing_documents": [],
#             "confidence": 0.95
#         }

#     # --------------------------------------------------------
#     # Rule 4 : Shopping is never reimbursable
#     # --------------------------------------------------------

#     shopping = claim.get("shopping", 0)

#     if shopping > 0:

#         return {
#             "decision": "Reject",
#             "approved_amount": 0,
#             "rejected_amount": (
#                 financials["approved_amount"]
#                 + financials["rejected_amount"]
#                 + shopping
#             ),
#             "missing_documents": [],
#             "confidence": 0.95
#         }

#     # --------------------------------------------------------
#     # Rule 5 : Flight Policy
#     # --------------------------------------------------------

#     flight_limit = limits.get("flight", {})

#     if not flight_limit.get("approved", True):

#         return {
#             "decision": "Reject",
#             "approved_amount": 0,
#             "rejected_amount": (
#                 financials["approved_amount"]
#                 + financials["rejected_amount"]),
#             "missing_documents": [],
#             "confidence": 0.95
            
#         }

#     # --------------------------------------------------------
#     # Rule 6 : Any exceeded reimbursement limit
#     # --------------------------------------------------------

#     if financials["rejected_amount"] > 0:

#         return {
#             "decision": "Partially Approved",
#             "approved_amount": financials["approved_amount"],
#             "rejected_amount": financials["rejected_amount"],
#             "missing_documents": [],
#             "confidence": 0.85
#         }

#     # --------------------------------------------------------
#     # Rule 7 : Everything valid
#     # --------------------------------------------------------

#     return {

#         "decision": "Approve",

#         "approved_amount": financials["approved_amount"],

#         "rejected_amount": 0,

#         "missing_documents": [],
#         "confidence": 0.98

#     }
















from typing import Dict


class DecisionEngine:
    """
    Deterministic Business Decision Engine

    This class is responsible ONLY for making reimbursement decisions.

    No LLM is used here.

    Gemini is used only to generate the explanation.
    """

    @staticmethod
    def evaluate(
        claim: Dict,
        limits: Dict,
        receipts: Dict,
        duplicates: Dict,
        approver: str,
    ):

        expenses = []

        approved_total = 0
        rejected_total = 0

        # ==========================================================
        # Duplicate Receipt
        # ==========================================================

        if duplicates.get("duplicate_found", False):

            return {
                "decision": "Reject",
                "approved_amount": 0,
                "rejected_amount": (
                    claim.get("hotel", 0)
                    + claim.get("meal", 0)
                    + claim.get("taxi", 0)
                    + claim.get("shopping", 0)
                    + claim.get("flight_amount", 0)
                ),
                "approver": approver,
                "expenses": [],
                "missing_documents": [],
                "policy_references": [
                    "Duplicate Receipt Policy"
                ],
            }

        # ==========================================================
        # Missing Attachments
        # ==========================================================

        if not receipts["valid"]:

            manual_review = True

        else:

            manual_review = False

        # ==========================================================
        # HOTEL
        # ==========================================================

        claimed = claim.get("hotel", 0)

        limit = limits["hotel_per_night"]

        approved = min(claimed, limit)

        rejected = max(0, claimed - limit)

        approved_total += approved
        rejected_total += rejected

        expenses.append({

            "category": "Hotel",

            "claimed": claimed,

            "approved": approved,

            "rejected": rejected,

            "status": (
                "Approved"
                if rejected == 0
                else "Partially Approved"
            ),

            "remarks": (
                "Within limit"
                if rejected == 0
                else "Exceeded hotel reimbursement limit"
            )

        })

        # ==========================================================
        # MEAL
        # ==========================================================

        claimed = claim.get("meal", 0)

        limit = limits["meal_per_day"]

        approved = min(claimed, limit)

        rejected = max(0, claimed - limit)

        approved_total += approved
        rejected_total += rejected

        expenses.append({

            "category": "Meal",

            "claimed": claimed,

            "approved": approved,

            "rejected": rejected,

            "status": (
                "Approved"
                if rejected == 0
                else "Partially Approved"
            ),

            "remarks": (
                "Within limit"
                if rejected == 0
                else "Exceeded meal reimbursement limit"
            )

        })

        # ==========================================================
        # TAXI
        # ==========================================================

        claimed = claim.get("taxi", 0)

        limit = limits["taxi_limit"]

        approved = min(claimed, limit)

        rejected = max(0, claimed - limit)

        approved_total += approved
        rejected_total += rejected

        expenses.append({

            "category": "Taxi",

            "claimed": claimed,

            "approved": approved,

            "rejected": rejected,

            "status": (
                "Approved"
                if rejected == 0
                else "Partially Approved"
            ),

            "remarks": (
                "Within limit"
                if rejected == 0
                else "Exceeded taxi reimbursement limit"
            )

        })

        # ==========================================================
        # FLIGHT
        # ==========================================================

        flight_class = claim.get("flight", "Economy")

        flight_amount = claim.get("flight_amount", 0)

        if flight_class.lower() == "economy":

            approved = flight_amount

            rejected = 0

            status = "Approved"

            remarks = "Economy fare reimbursable"

        else:

            approved = 0

            rejected = flight_amount

            status = "Rejected"

            remarks = "Business class is not reimbursable"

        approved_total += approved
        rejected_total += rejected

        expenses.append({

            "category": "Flight",

            "claimed": flight_amount,

            "approved": approved,

            "rejected": rejected,

            "status": status,

            "remarks": remarks

        })

        # ==========================================================
        # SHOPPING
        # ==========================================================

        shopping = claim.get("shopping", 0)

        if shopping > 0:

            rejected_total += shopping

            expenses.append({

                "category": "Shopping",

                "claimed": shopping,

                "approved": 0,

                "rejected": shopping,

                "status": "Rejected",

                "remarks": "Personal expenses are not reimbursable"

            })

        # ==========================================================
        # FINAL DECISION
        # ==========================================================

        if manual_review:

            decision = "Manual Review"

        elif approved_total == 0:

            decision = "Reject"

        elif rejected_total == 0:

            decision = "Approve"

        else:

            decision = "Partially Approved"

        return {

            "decision": decision,

            "approved_amount": approved_total,

            "rejected_amount": rejected_total,

            "approver": approver,

            "expenses": expenses,

            "missing_documents": (
                receipts["missing_attachments"]
                + receipts["missing_receipts"]
            ),

            "policy_references": [

                "Hotel Policy",

                "Meal Policy",

                "Taxi Policy",

                "Flight Policy",

                "Shopping Policy"

            ]

        }