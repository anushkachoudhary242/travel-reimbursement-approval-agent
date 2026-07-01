from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.logger import logger


class PolicyNotFoundException(Exception):
    pass


class ReceiptValidationException(Exception):
    pass


class DecisionEngineException(Exception):
    pass


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    logger.error(f"Validation Error : {exc}")

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid Request",
            "details": exc.errors()
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc)
        }
    )