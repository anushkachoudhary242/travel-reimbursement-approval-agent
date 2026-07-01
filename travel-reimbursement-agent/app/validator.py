from app.schemas import ClaimRequest


def validate_claim(claim: dict):

    return ClaimRequest(**claim)