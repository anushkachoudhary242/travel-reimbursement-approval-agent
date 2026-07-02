import json

from app.rag import PolicyRetriever
from app.config import (
    LIMITS_FILE,
    APPROVAL_MATRIX_FILE,
    RECEIPTS_DB_FILE
)

retriever = PolicyRetriever()


# ==========================================================
# Utility Functions
# ==========================================================

def load_limits():

    with open(LIMITS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_approval_matrix():

    with open(APPROVAL_MATRIX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_receipts():

    with open(RECEIPTS_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================================
# RAG
# ==========================================================

def policy_lookup(query: str):

    docs = retriever.retrieve(query)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return context


# ==========================================================
# Expense Validation
# ==========================================================

def check_expense_limits(claim: dict):

    limits = load_limits()

    return {

        "hotel_per_night": limits["hotel_per_night"],

        "meal_per_day": limits["meal_per_day"],

        "taxi_limit": limits["taxi_limit"],

        "flight": {
            "allowed_class": limits["flight"]["allowed_class"]
        }
    }


# ==========================================================
# Receipt Validation
# ==========================================================

def check_receipts(claim: dict):

    receipt_db = load_receipts()

    receipt_ids = claim.get(
        "receipts",
        []
    )

    # ==========================================================
    # No receipts uploaded
    # ==========================================================

    total_expense = (
        claim.get("hotel", 0)
        + claim.get("meal", 0)
        + claim.get("taxi", 0)
        + claim.get("flight_fare", 0)
    )

    if total_expense > 0 and len(receipt_ids) == 0:

        return {

            "valid": False,

            "missing_receipts": [

                "No receipts uploaded"

            ],

            "missing_attachments": [],

            "found_receipts": []

        }

    result = {

        "valid": True,

        "missing_receipts": [],

        "missing_attachments": [],

        "found_receipts": []

    }

    for receipt_id in receipt_ids:

        receipt = receipt_db.get(receipt_id)

        if receipt is None:

            result["valid"] = False

            result["missing_receipts"].append(
                receipt_id
            )

            continue

        result["found_receipts"].append(
            receipt_id
        )

        if not receipt.get("attachment", False):

            result["valid"] = False

            result["missing_attachments"].append(
                receipt_id
            )

    return result


# ==========================================================
# Duplicate Receipt Detection
# ==========================================================

def check_duplicate_receipts(claim: dict):

    receipt_ids = claim.get(
        "receipts",
        []
    )

    duplicates = []

    seen = set()

    for receipt in receipt_ids:

        if receipt in seen:

            duplicates.append(
                receipt
            )

        seen.add(
            receipt
        )

    return {

        "duplicate_found": len(
            duplicates
        ) > 0,

        "duplicates": duplicates

    }


# ==========================================================
# Approval Authority
# ==========================================================

def get_required_approver(total_amount: float):

    matrix = load_approval_matrix()

    if total_amount <= matrix["manager"]["max_amount"]:

        return "Manager"

    elif total_amount <= matrix["senior_manager"]["max_amount"]:

        return "Senior Manager"

    return "Director"