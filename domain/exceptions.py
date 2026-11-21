class ServiceDeskError(Exception):
    """Base exception for Smart Service Desk domain and application errors."""


class DuplicateRequestError(ServiceDeskError):
    """Raised when attempting to create a service request with an existing ID."""


class RequestNotFoundError(ServiceDeskError):
    """Raised when a service request ID cannot be found."""


class InvalidPriorityError(ServiceDeskError):
    """Raised when an unsupported priority value is provided."""


class RequestAlreadyResolvedError(ServiceDeskError):
    """Raised when attempting to resolve a request that is already RESOLVED."""
