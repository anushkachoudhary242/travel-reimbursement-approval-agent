# import json

# from langgraph.graph import StateGraph, END
# from app.logger import logger
# from app.state import TravelState
# from app.agent import TravelApprovalAgent
# from app.decision_engine import make_business_decision

# from app.tools import (
#     policy_lookup,
#     check_expense_limits,
#     check_receipts,
#     check_duplicate_receipts,
#     get_required_approver
# )

# # ==========================================================
# # Initialize Agent
# # ==========================================================

# agent = TravelApprovalAgent()


# # ==========================================================
# # Node 1 : Retrieve Relevant Policy (RAG)
# # ==========================================================

# def retrieve_policy(state: TravelState):
#     logger.info("Running Policy Retrieval")

#     claim = state["claim"]

#     query = f"""
#     Travel reimbursement policy.

#     Hotel claim:
#     ₹{claim.get("hotel",0)}

#     Meal claim:
#     ₹{claim.get("meal",0)}

#     Taxi claim:
#     ₹{claim.get("taxi",0)}

#     Flight:
#     {claim.get("flight","")}

#     Return the relevant reimbursement rules.
#     """

#     state["policy"] = policy_lookup(query)

#     return state


# # ==========================================================
# # Node 2 : Expense Limit Validation
# # ==========================================================

# def validate_limits(state: TravelState):
#     logger.info("Checking expense limits")

#     state["limits"] = check_expense_limits(
#         state["claim"]
#     )

#     return state


# # ==========================================================
# # Node 3 : Receipt Validation
# # ==========================================================

# def validate_receipts(state: TravelState):
#     logger.info("Checking receipts")

#     state["receipts"] = check_receipts(
#         state["claim"]
#     )

#     return state


# # ==========================================================
# # Node 4 : Duplicate Detection
# # ==========================================================

# def duplicate_checker(state: TravelState):
#     logger.info("Checking duplicate receipts")

#     state["duplicates"] = check_duplicate_receipts(
#         state["claim"]
#     )

#     return state


# # ==========================================================
# # Node 5 : Approval Authority
# # ==========================================================

# def approval_checker(state: TravelState):
#     logger.info("Finding approver")

#     claim = state["claim"]

#     total = (

#         claim.get("hotel",0)

#         + claim.get("meal",0)

#         + claim.get("taxi",0)

#     )

#     state["approver"] = get_required_approver(total)

#     return state


# # ==========================================================
# # Node 6 : Calculate Financial Summary
# # ==========================================================

# def calculate_financials(state: TravelState):
#     logger.info("Calculating approved amount")

#     limits = state["limits"]

#     approved_amount = (

#         limits["hotel"]["approved"]

#         + limits["meal"]["approved"]

#         + limits["taxi"]["approved"]

#     )

#     rejected_amount = (

#         limits["hotel"]["excess_amount"]

#         + limits["meal"]["excess_amount"]

#         + limits["taxi"]["excess_amount"]

#     )

#     state["financials"] = {

#         "approved_amount": approved_amount,

#         "rejected_amount": rejected_amount

#     }

#     return state


# # ==========================================================
# # Node 7 : Business Decision Engine
# # ==========================================================

# def business_decision(state: TravelState):
#     logger.info("Running business decision engine")

#     state["business_decision"] = make_business_decision(

#         claim=state["claim"],

#         limits=state["limits"],

#         receipts=state["receipts"],

#         duplicates=state["duplicates"],

#         financials=state["financials"]

#     )

#     return state


# def make_decision(state: TravelState):

#     state["result"] = agent.evaluate(

#         claim=state["claim"],

#         policy=state["policy"],

#         limits=state["limits"],

#         receipts=state["receipts"],

#         duplicates=state["duplicates"],

#         approver=state["approver"],

#         financials=state["financials"],

#         business_decision=state["business_decision"]

#     )

#     return state


# # ==========================================================
# # Build Graph
# # ==========================================================

# builder = StateGraph(TravelState)


# builder.add_node(
#     "retrieve_policy",
#     retrieve_policy
# )

# builder.add_node(
#     "validate_limits",
#     validate_limits
# )

# builder.add_node(
#     "validate_receipts",
#     validate_receipts
# )

# builder.add_node(
#     "duplicate_checker",
#     duplicate_checker
# )

# builder.add_node(
#     "approval_checker",
#     approval_checker
# )

# builder.add_node(
#     "calculate_financials",
#     calculate_financials
# )

# builder.add_node(
#     "business_decision",
#     business_decision
# )

# builder.add_node(
#     "make_decision",
#     make_decision
# )

# # Entry Point

# builder.set_entry_point(
#     "retrieve_policy"
# )


# # Flow

# builder.add_edge(
#     "retrieve_policy",
#     "validate_limits"
# )

# builder.add_edge(
#     "validate_limits",
#     "validate_receipts"
# )

# builder.add_edge(
#     "validate_receipts",
#     "duplicate_checker"
# )

# builder.add_edge(
#     "duplicate_checker",
#     "approval_checker"
# )

# builder.add_edge(
#     "approval_checker",
#     "calculate_financials"
# )

# builder.add_edge(
#     "calculate_financials",
#     "business_decision"
# )

# builder.add_edge(
#     "business_decision",
#     "make_decision"
# )

# graph = builder.compile()
















import json

from langgraph.graph import StateGraph, END

from app.state import TravelState
from app.agent import TravelApprovalAgent
from app.decision_engine import DecisionEngine

from app.tools import (
    policy_lookup,
    check_expense_limits,
    check_receipts,
    check_duplicate_receipts,
    get_required_approver
)


agent = TravelApprovalAgent()


# ==========================================================
# Policy Retrieval (RAG)
# ==========================================================

def retrieve_policy(state: TravelState):

    claim = state["claim"]

    query = f"""
    Hotel: {claim.get("hotel",0)}
    Meal: {claim.get("meal",0)}
    Taxi: {claim.get("taxi",0)}
    Flight: {claim.get("flight","")}
    Shopping: {claim.get("shopping",0)}
    """

    state["policy"] = policy_lookup(query)

    return state


# ==========================================================
# Expense Limit Validation
# ==========================================================

def validate_limits(state: TravelState):

    state["limits"] = check_expense_limits(
        state["claim"]
    )

    return state


# ==========================================================
# Receipt Validation
# ==========================================================

def validate_receipts(state: TravelState):

    state["receipts"] = check_receipts(
        state["claim"]
    )

    return state


# ==========================================================
# Duplicate Receipt Validation
# ==========================================================

def duplicate_checker(state: TravelState):

    state["duplicates"] = check_duplicate_receipts(
        state["claim"]
    )

    return state


# ==========================================================
# Determine Required Approver
# ==========================================================

def approval_checker(state: TravelState):

    claim = state["claim"]

    total_claim = (
        claim.get("hotel", 0)
        + claim.get("meal", 0)
        + claim.get("taxi", 0)
        + claim.get("flight_amount", 0)
    )

    state["approver"] = get_required_approver(
        total_claim
    )

    return state


# ==========================================================
# Business Decision Engine
# ==========================================================

def business_decision(state: TravelState):

    decision = DecisionEngine.evaluate(

        claim=state["claim"],

        limits=state["limits"],

        receipts=state["receipts"],

        duplicates=state["duplicates"],

        approver=state["approver"]

    )

    state["business_decision"] = decision

    return state


# ==========================================================
# Gemini Explanation
# ==========================================================

def generate_explanation(state: TravelState):

    response = agent.evaluate(

        claim=state["claim"],

        policy=state["policy"],

        business_decision=state["business_decision"]

    )

    try:

        explanation = json.loads(response)

    except Exception:

        explanation = {

            "confidence": 0.85,

            "policy_references": [],

            "explanation": response

        }

    result = state["business_decision"]

    result["confidence"] = explanation.get(

        "confidence",

        0.85

    )

    result["policy_references"] = explanation.get(

        "policy_references",

        result["policy_references"]

    )

    result["explanation"] = explanation.get(

        "explanation",

        ""

    )

    state["result"] = result

    return state


# ==========================================================
# Build Graph
# ==========================================================

builder = StateGraph(TravelState)

builder.add_node(
    "retrieve_policy",
    retrieve_policy
)

builder.add_node(
    "validate_limits",
    validate_limits
)

builder.add_node(
    "validate_receipts",
    validate_receipts
)

builder.add_node(
    "duplicate_checker",
    duplicate_checker
)

builder.add_node(
    "approval_checker",
    approval_checker
)

builder.add_node(
    "business_decision",
    business_decision
)

builder.add_node(
    "generate_explanation",
    generate_explanation
)

builder.set_entry_point(
    "retrieve_policy"
)

builder.add_edge(
    "retrieve_policy",
    "validate_limits"
)

builder.add_edge(
    "validate_limits",
    "validate_receipts"
)

builder.add_edge(
    "validate_receipts",
    "duplicate_checker"
)

builder.add_edge(
    "duplicate_checker",
    "approval_checker"
)

builder.add_edge(
    "approval_checker",
    "business_decision"
)

builder.add_edge(
    "business_decision",
    "generate_explanation"
)

builder.add_edge(
    "generate_explanation",
    END
)

graph = builder.compile()