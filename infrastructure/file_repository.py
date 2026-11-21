import json
from pathlib import Path
from typing import Protocol

from domain.service_request import ServiceRequest


class RequestRepository(Protocol):
    def load_all(self) -> list[ServiceRequest]: ...
    def save_all(self, requests: list[ServiceRequest]) -> None: ...


class FileRepository:
    def __init__(self, file_path: str | Path = Path("data/requests.json")) -> None:
        self.file_path = Path(file_path)

    def load_all(self) -> list[ServiceRequest]:
        if not self.file_path.exists():
            return []

        content = self.file_path.read_text(encoding="utf-8").strip()
        if not content:
            return []

        try:
            raw_items = json.loads(content)
        except json.JSONDecodeError:
            return []

        if not isinstance(raw_items, list):
            return []

        requests: list[ServiceRequest] = []
        for item in raw_items:
            if isinstance(item, dict):
                requests.append(ServiceRequest.from_dict(item))
        return requests

    def save_all(self, requests: list[ServiceRequest]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [req.to_dict() for req in requests]
        self.file_path.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )
