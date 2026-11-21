from domain.exceptions import DuplicateRequestError, RequestNotFoundError
from domain.service_request import ServiceRequest
from infrastructure.file_repository import RequestRepository


class RequestService:
    def __init__(self, repository: RequestRepository) -> None:
        self._repository = repository

    def create_request(
        self,
        request_id: str,
        employee_name: str,
        issue: str,
        priority: str,
    ) -> ServiceRequest:
        requests = self._repository.load_all()
        normalized_id = request_id.strip().upper()

        if any(req.request_id == normalized_id for req in requests):
            raise DuplicateRequestError(
                f"Service request with ID '{normalized_id}' already exists."
            )

        new_request = ServiceRequest(
            request_id=normalized_id,
            employee_name=employee_name,
            issue=issue,
            priority=priority,
        )
        requests.append(new_request)
        self._repository.save_all(requests)
        return new_request

    def view_requests(self) -> list[ServiceRequest]:
        return self._repository.load_all()

    def search_request(self, request_id: str) -> ServiceRequest:
        normalized_id = request_id.strip().upper()
        requests = self._repository.load_all()

        for req in requests:
            if req.request_id == normalized_id:
                return req

        raise RequestNotFoundError(f"Request '{normalized_id}' not found.")

    def resolve_request(self, request_id: str) -> ServiceRequest:
        normalized_id = request_id.strip().upper()
        requests = self._repository.load_all()

        for req in requests:
            if req.request_id == normalized_id:
                req.resolve()
                self._repository.save_all(requests)
                return req

        raise RequestNotFoundError(f"Request '{normalized_id}' not found.")
