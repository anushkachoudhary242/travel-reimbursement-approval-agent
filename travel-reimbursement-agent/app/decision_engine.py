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
                    + claim.get("flight_fare", 0)
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

        flight_type = claim.get("flight_type", "Economy")

        flight_fare = claim.get("flight_fare", 0)

        allowed_class = limits["flight"]["allowed_class"]

        if flight_type.lower() == allowed_class.lower():

            approved = flight_fare

            rejected = 0

            status = "Approved"

            remarks = (
                f"{flight_type} airfare reimbursed."
            )

        else:

            approved = 0

            rejected = flight_fare

            status = "Rejected"

            remarks = (
                f"{flight_type} airfare requires Director approval."
            )

        approved_total += approved

        rejected_total += rejected

        expenses.append({

            "category": "Flight",

            "claimed": flight_fare,

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