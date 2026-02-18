import uuid
from http import HTTPStatus
from drf_standardized_errors.formatter import ExceptionFormatter as BaseExceptionFormatter
from drf_standardized_errors.types import ErrorResponse
from utils.base_result import BaseResult
from utils.log_helpers import OperationLogger


class ExceptionFormatter(BaseExceptionFormatter):
    """
    Custom formatter for DRF Standardized Errors.
    - Returns generic safe message for 500+ errors
    - Wraps all responses in BaseResult format
    """

    def format_error_response(self, error_response: ErrorResponse):
        error = error_response.errors[0] if error_response.errors else None
        status_code = getattr(error_response, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR)

        op = OperationLogger("ExceptionFormatter", status_code=status_code)
        op.fail(
            f"API Error [{status_code}]: {getattr(error, 'detail', 'Unknown error')}",
            exc=None
        )

        if status_code >= 500:
            return BaseResult(
                status_code=500,
                message="An unexpected error occurred on the server. Please try again later.",
                request_id=str(uuid.uuid4())
            ).to_dict()

        message = (
            f"{error.attr}: {error.detail}"
            if error and getattr(error, "attr", None)
            else str(getattr(error, "detail", "An unexpected error occurred."))
        )

        return BaseResult(
            status_code=status_code,
            message=message,
            request_id=str(uuid.uuid4())
        ).to_dict()