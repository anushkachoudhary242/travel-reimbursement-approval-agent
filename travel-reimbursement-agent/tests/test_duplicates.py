from app.tools import check_duplicate_receipts

claim = {
    "receipts": [
        "receipt_001",
        "receipt_002",
        "receipt_002",
        "receipt_003"
    ]
}

result = check_duplicate_receipts(claim)

print(result)