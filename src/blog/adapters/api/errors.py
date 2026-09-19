import logging

from starlette.requests import Request
from starlette.responses import JSONResponse

from blog.core.errors import Kind, AppError

logger = logging.getLogger(__name__)

_STATUS = {
    Kind.VALIDATION:      400,
    Kind.UNAUTHENTICATED: 401,
    Kind.FORBIDDEN:       403,
    Kind.NOT_FOUND:       404,
    Kind.CONFLICT:        409,
    Kind.RATE_LIMITED:    429,
    Kind.INTERNAL:        500,
}


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    if exc.kind is Kind.INTERNAL:
        # Внутрішні деталі — у лог, не клієнту (§14.2).
        logger.exception("unhandled", extra={"code": exc.code})
        return JSONResponse({"error": {"code": "internal", "message": "Internal error"}}, 500)

    body: dict[str, object] = {"error": {"code": exc.code, "message": exc.message}}
    if exc.fields:
        body["error"]["fields"] = exc.fields
    return JSONResponse(body, status_code=_STATUS[exc.kind])