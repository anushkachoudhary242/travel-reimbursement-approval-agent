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
    Travel reimbursement claim
    Hotel Expense: {claim.get("hotel",0)}
    Meal Expense: {claim.get("meal",0)}
    Taxi Expense: {claim.get("taxi",0)}
    Flight Type: {claim.get("flight_type", "")}
    Flight Fare: {claim.get("flight_fare", 0)}
    Shopping Expense: {claim.get("shopping",0)}
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
        + claim.get("flight_fare", 0)
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