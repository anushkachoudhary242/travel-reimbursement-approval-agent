from app.tools import check_receipts
from app.utils import load_json


print("="*70)
print("APPROVED CLAIM")
print("="*70)

claim = load_json("data/claims/approved.json")

print(
    check_receipts(claim)
)


print("\n")


print("="*70)
print("MANUAL REVIEW CLAIM")
print("="*70)

claim = load_json("data/claims/manual_review.json")

print(
    check_receipts(claim)
)