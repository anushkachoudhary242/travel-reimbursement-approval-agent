from app.agent import TravelApprovalAgent

from app.tools import *

from app.utils import load_json


claim = load_json(
    "data/claims/partial.json"
)

policy = policy_lookup(
    "hotel reimbursement"
)

limits = check_expense_limits(
    claim
)

receipts = check_receipts(
    claim
)

duplicates = check_duplicate_receipts(
    claim
)

total = (
    claim["hotel"]
    + claim["meal"]
    + claim["taxi"]
)

approver = get_required_approver(
    total
)


agent = TravelApprovalAgent()

financials = {

    "approved_amount": (

        limits["hotel"]["approved"]

        + limits["meal"]["approved"]

        + limits["taxi"]["approved"]

    ),

    "rejected_amount": (

        limits["hotel"]["excess_amount"]

        + limits["meal"]["excess_amount"]

        + limits["taxi"]["excess_amount"]

    )

}

result = agent.evaluate(

    claim,

    policy,

    limits,

    receipts,

    duplicates,

    approver,

    financials

)

print(result)