from typing import List, Optional

from pydantic import BaseModel, Field


# ==========================================================
# Claim Request
# ==========================================================

class ClaimRequest(BaseModel):

    employee_id: str = Field(..., example="EMP001")

    employee_name: str = Field(..., example="Rahul Sharma")

    trip_location: str = Field(..., example="Mumbai")

    hotel: float = Field(0, ge=0)

    meal: float = Field(0, ge=0)

    taxi: float = Field(0, ge=0)

    flight_type: str
    flight_fare: float

    shopping: float = Field(
        0,
        ge=0
    )

    receipts: List[str]


# ==========================================================
# Expense Wise Response
# ==========================================================

class ExpenseBreakdown(BaseModel):

    category: str

    claimed: float

    approved: float

    rejected: float

    status: str

    remarks: str


# ==========================================================
# Final Response
# ==========================================================

class DecisionResponse(BaseModel):

    decision: str

    approved_amount: float

    rejected_amount: float

    approver: str

    confidence: float

    missing_documents: List[str]

    policy_references: List[str]

    expenses: List[ExpenseBreakdown]

    explanation: str