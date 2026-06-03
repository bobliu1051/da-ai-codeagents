class AppError(Exception):
    """Base application error."""
    status_code = 500


class ValidationError(AppError):
    status_code = 400


class AuthError(AppError):
    status_code = 401


class PermissionError(AppError):
    status_code = 403


class NotFoundError(AppError):
    status_code = 404


class BusinessRuleError(AppError):
    status_code = 422


class RateLimitError(AppError):
    status_code = 429
