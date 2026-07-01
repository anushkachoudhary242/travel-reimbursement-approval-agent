from app.tools import (
    policy_lookup,
    load_limits,
    load_receipts,
    load_approval_matrix
)

print("="*80)
print("TEST 1 : POLICY LOOKUP")
print("="*80)

print(
    policy_lookup(
        "hotel reimbursement limit"
    )
)

print("\n")


print("="*80)
print("TEST 2 : LIMITS")
print("="*80)

print(
    load_limits()
)

print("\n")


print("="*80)
print("TEST 3 : APPROVAL MATRIX")
print("="*80)

print(
    load_approval_matrix()
)

print("\n")


print("="*80)
print("TEST 4 : RECEIPTS")
print("="*80)

print(
    load_receipts()
)