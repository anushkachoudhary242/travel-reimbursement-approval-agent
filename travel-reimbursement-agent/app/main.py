# from fastapi import FastAPI, HTTPException

# from app.schemas import (
#     ClaimRequest,
#     DecisionResponse
# )

# from app.graph import graph

# from app.validator import validate_claim

# from app.logger import logger

# from fastapi.exceptions import RequestValidationError

# from app.exceptions import (
#     validation_exception_handler,
#     generic_exception_handler
# )

# app = FastAPI(

#     title="Travel Reimbursement Approval Agent",

#     version="1.0.0",

#     description="AI Agent for evaluating travel reimbursement claims"

# )

# app.add_exception_handler(
#     RequestValidationError,
#     validation_exception_handler
# )

# app.add_exception_handler(
#     Exception,
#     generic_exception_handler
# )

# @app.get("/")
# def home():

#     return {

#         "message": "Travel Reimbursement Approval Agent Running"

#     }

# @app.post(
#     "/evaluate",
#     response_model=DecisionResponse
# )
# def evaluate_claim(
#     claim: ClaimRequest
# ):

#     try:

#         validated_claim = validate_claim(
#             claim.model_dump()
#         )

#         initial_state = {

#             "claim": validated_claim.model_dump(),

#             "policy": "",

#             "limits": {},

#             "receipts": {},

#             "duplicates": {},

#             "approver": {},

#             "financials": {},

#             "business_decision": {},

#             "result": {}

#         }

#         logger.info(
#             f"Received claim from {validated_claim.employee_name}"
#         )

#         result = graph.invoke(initial_state)

#         logger.info(
#             f"Decision: {result['result']['decision']}"
#         )

#         return result["result"]
                

#     except Exception as e:

#         raise HTTPException(

#             status_code=500,

#             detail=str(e)

#         )











from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.schemas import ClaimRequest
from app.graph import graph
from app.logger import logger

from app.exceptions import (
    validation_exception_handler,
    generic_exception_handler
)

# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(

    title="AI Travel Reimbursement Approval Agent",

    description="""
An AI-powered Travel Reimbursement Approval System built using:

• LangGraph
• LangChain
• RAG (ChromaDB)
• Google Gemini
• FastAPI

The Business Decision Engine performs deterministic reimbursement calculations.
Gemini generates only the explanation.
""",

    version="2.0.0"

)

# ==========================================================
# Exception Handlers
# ==========================================================

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "service": "Travel Reimbursement Agent",

        "version": "2.0.0"

    }


# ==========================================================
# Evaluate Claim
# ==========================================================

@app.post("/evaluate")
def evaluate(claim: ClaimRequest):

    logger.info(
        f"Received claim from {claim.employee_name}"
    )

    initial_state = {

        "claim": claim.model_dump(),

        "policy": None,

        "limits": None,

        "receipts": None,

        "duplicates": None,

        "approver": None,

        "business_decision": None,

        "result": None

    }

    final_state = graph.invoke(initial_state)

    logger.info(

        f"Decision : "

        f"{final_state['result']['decision']}"

    )

    return final_state["result"]


# ==========================================================
# Root
# ==========================================================

@app.get("/")
def home():

    return {

        "message": "Travel Reimbursement Approval Agent",

        "swagger": "/docs",

        "health": "/health"

    }