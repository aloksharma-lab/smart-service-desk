from domain.exceptions import InvalidPriorityError, RequestAlreadyResolvedError

ALLOWED_PRIORITIES = ("LOW", "MEDIUM", "HIGH")
STATUS_OPEN = "OPEN"
STATUS_RESOLVED = "RESOLVED"


class ServiceRequest:
    def __init__(
        self,
        request_id: str,
        employee_name: str,
        issue: str,
        priority: str,
        status: str = STATUS_OPEN,
    ) -> None:
        cleaned_id = request_id.strip().upper()
        cleaned_employee = employee_name.strip()
        cleaned_issue = issue.strip()
        normalized_priority = self._validate_priority(priority)

        if not cleaned_id:
            raise ValueError("Request ID cannot be empty.")
        if not cleaned_employee:
            raise ValueError("Employee name cannot be empty.")
        if not cleaned_issue:
            raise ValueError("Issue description cannot be empty.")
        if status not in (STATUS_OPEN, STATUS_RESOLVED):
            raise ValueError(f"Invalid status '{status}'.")

        self.request_id = cleaned_id
        self.employee_name = cleaned_employee
        self.issue = cleaned_issue
        self.priority = normalized_priority
        self.status = status

    @staticmethod
    def _validate_priority(priority: str) -> str:
        normalized = priority.strip().upper()
        if normalized not in ALLOWED_PRIORITIES:
            raise InvalidPriorityError("Priority must be LOW, MEDIUM or HIGH")
        return normalized

    def resolve(self) -> None:
        """Transition request status from OPEN to RESOLVED."""
        if self.status == STATUS_RESOLVED:
            raise RequestAlreadyResolvedError(
                f"Request {self.request_id} is already RESOLVED."
            )
        self.status = STATUS_RESOLVED

    def to_dict(self) -> dict[str, str]:
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "ServiceRequest":
        return cls(
            request_id=data["request_id"],
            employee_name=data["employee_name"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", STATUS_OPEN),
        )
