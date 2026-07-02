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