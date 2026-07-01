# from pydantic import BaseModel, Field
# from typing import List, Optional

# class ClaimRequest(BaseModel):

#     employee_id: str

#     employee_name: str

#     trip_location: str

#     hotel: float = 0

#     meal: float = 0

#     taxi: float = 0

#     flight: str

#     shopping: Optional[float] = 0

#     receipts: List[str]


# class DecisionResponse(BaseModel):

#     decision: str = Field(
#         description="Approve, Partially Approved, Reject or Manual Review"
#     )

#     approved_amount: float

#     rejected_amount: float
 
#     confidence: float = Field(
#     ge=0,
#     le=1,
#     description="Confidence score between 0 and 1"
#     )

#     missing_documents: List[str]

#     policy_references: List[str]

#     explanation: str






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

    # NEW
    flight_class: str = Field(
        "Economy",
        example="Economy"
    )

    # NEW
    flight_amount: float = Field(
        0,
        ge=0,
        example=12000
    )

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