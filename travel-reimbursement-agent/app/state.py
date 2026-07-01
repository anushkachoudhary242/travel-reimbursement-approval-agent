# from typing import TypedDict


# class TravelState(TypedDict):

#     claim: dict

#     policy: str

#     limits: dict

#     receipts: dict

#     duplicates: dict

#     approver: dict

#     financials: dict

#     business_decision: dict

#     result: dict












from typing import TypedDict, Optional


class TravelState(TypedDict):

    # Original Claim
    claim: dict

    # Retrieved Policy (RAG)
    policy: Optional[str]

    # Policy Limits
    limits: Optional[dict]

    # Receipt Validation
    receipts: Optional[dict]

    # Duplicate Validation
    duplicates: Optional[dict]

    # Required Approver
    approver: Optional[str]

    # Business Decision Engine Output
    business_decision: Optional[dict]

    # Final API Response
    result: Optional[dict]