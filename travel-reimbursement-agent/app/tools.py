# from app.utils import load_json
# from app.rag import PolicyRetriever

# # Initialize the RAG retriever
# retriever = None

# # ==========================================================
# # Tool 1: Policy Lookup (RAG)
# # ==========================================================

# def policy_lookup(query: str):

#     global retriever

#     if retriever is None:

#         print("Loading embedding model...")

#         retriever = PolicyRetriever()

#     docs = retriever.retrieve(query)

#     context = "\n\n".join(
#         [doc.page_content for doc in docs]
#     )

#     return context

# # ==========================================================
# # Tool 2: Load Expense Limits
# # ==========================================================

# def load_limits():
#     """
#     Load expense limits from limits.json
#     """

#     return load_json("data/limits.json")


# # ==========================================================
# # Tool 3: Load Approval Matrix
# # ==========================================================

# def load_approval_matrix():
#     """
#     Load approval hierarchy.
#     """

#     return load_json("data/approval_matrix.json")


# # ==========================================================
# # Tool 4: Load Receipt Database
# # ==========================================================

# def load_receipts():
#     """
#     Load receipt database.
#     """

#     return load_json("data/receipts_db.json")


# # ==========================================================
# # Tool 5: Expense Limit Checker
# # ==========================================================

# def check_expense_limits(claim: dict):
#     """
#     Compare claimed expenses with company reimbursement limits.
#     """

#     limits = load_limits()

#     result = {
#         "hotel": {},
#         "meal": {},
#         "taxi": {},
#         "flight": {}
#     }

#     # -----------------------------
#     # Hotel
#     # -----------------------------
#     hotel_amount = claim.get("hotel", 0)
#     hotel_limit = limits["hotel_per_night"]

#     result["hotel"] = {
#         "claimed": hotel_amount,
#         "limit": hotel_limit,
#         "approved": min(hotel_amount, hotel_limit),
#         "exceeded": hotel_amount > hotel_limit,
#         "excess_amount": max(0, hotel_amount - hotel_limit)
#     }

#     # -----------------------------
#     # Meal
#     # -----------------------------
#     meal_amount = claim.get("meal", 0)
#     meal_limit = limits["meal_per_day"]

#     result["meal"] = {
#         "claimed": meal_amount,
#         "limit": meal_limit,
#         "approved": min(meal_amount, meal_limit),
#         "exceeded": meal_amount > meal_limit,
#         "excess_amount": max(0, meal_amount - meal_limit)
#     }

#     # -----------------------------
#     # Taxi
#     # -----------------------------
#     taxi_amount = claim.get("taxi", 0)
#     taxi_limit = limits["taxi_limit"]

#     result["taxi"] = {
#         "claimed": taxi_amount,
#         "limit": taxi_limit,
#         "approved": min(taxi_amount, taxi_limit),
#         "exceeded": taxi_amount > taxi_limit,
#         "excess_amount": max(0, taxi_amount - taxi_limit)
#     }

#     # -----------------------------
#     # Flight
#     # -----------------------------
#     claimed_flight = claim.get("flight", "")

#     result["flight"] = {
#         "claimed": claimed_flight,
#         "allowed": limits["flight_class"],
#         "approved": claimed_flight == limits["flight_class"]
#     }

#     return result

# # ==========================================================
# # Tool 6: Receipt Validator
# # ==========================================================

# def check_receipts(claim: dict):
#     """
#     Validate all receipts referenced in the claim.
#     """

#     receipt_db = load_receipts()

#     receipt_ids = claim.get("receipts", [])

#     result = {
#         "valid": True,
#         "missing_receipts": [],
#         "missing_attachments": [],
#         "found_receipts": []
#     }

#     for receipt_id in receipt_ids:

#         receipt = receipt_db.get(receipt_id)

#         # Receipt ID not found
#         if receipt is None:
#             result["valid"] = False
#             result["missing_receipts"].append(receipt_id)
#             continue

#         result["found_receipts"].append(receipt_id)

#         # Attachment missing
#         if not receipt.get("attachment", False):
#             result["valid"] = False
#             result["missing_attachments"].append(receipt_id)

#     return result

# # ==========================================================
# # Tool 7: Duplicate Receipt Checker
# # ==========================================================

# def check_duplicate_receipts(claim: dict):
#     """
#     Detect duplicate receipt IDs in a reimbursement claim.
#     """

#     receipt_ids = claim.get("receipts", [])

#     duplicates = []
#     seen = set()

#     for receipt_id in receipt_ids:

#         if receipt_id in seen:
#             duplicates.append(receipt_id)

#         seen.add(receipt_id)

#     return {
#         "duplicate_found": len(duplicates) > 0,
#         "duplicates": duplicates
#     }


# # ==========================================================
# # Tool 8: Approval Authority
# # ==========================================================

# def get_required_approver(total_amount: float):
#     """
#     Determine who should approve the claim.
#     """

#     matrix = load_approval_matrix()

#     for approver, rule in matrix.items():

#         if total_amount <= rule["max_amount"]:

#             return {
#                 "approver": approver,
#                 "max_amount": rule["max_amount"]
#             }

#     return {
#         "approver": "director"
#     }














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

        "flight_class": limits["flight_class"]

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