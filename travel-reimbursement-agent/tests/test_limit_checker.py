from app.tools import check_expense_limits
from app.utils import load_json

claim = load_json("data/claims/partial.json")

result = check_expense_limits(claim)

print(result)