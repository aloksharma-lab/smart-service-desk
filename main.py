from application.request_service import RequestService
from domain.exceptions import (
    DuplicateRequestError,
    InvalidPriorityError,
    RequestAlreadyResolvedError,
    RequestNotFoundError,
)
from domain.service_request import ServiceRequest
from infrastructure.file_repository import FileRepository


def print_menu() -> None:
    print("\nSMART SERVICE DESK SYSTEM")
    print("1. Create Service Request")
    print("2. View All Requests")
    print("3. Search Request")
    print("4. Resolve Request")
    print("5. Exit")


def format_request_line(req: ServiceRequest) -> str:
    return (
        f"{req.request_id}  {req.employee_name}  "
        f"{req.issue}  {req.priority} | {req.status}"
    )


def print_request_details(req: ServiceRequest) -> None:
    print("\n--- Service Request Details ---")
    print(f"Request ID : {req.request_id}")
    print(f"Employee   : {req.employee_name}")
    print(f"Issue      : {req.issue}")
    print(f"Priority   : {req.priority}")
    print(f"Status     : {req.status}")


def handle_create_request(service: RequestService) -> None:
    request_id = input("Enter Request ID: ").strip()
    employee_name = input("Enter Employee Name: ").strip()
    issue = input("Enter Issue: ").strip()
    priority = input("Enter Priority: ").strip()

    try:
        service.create_request(request_id, employee_name, issue, priority)
        print("Service Request created successfully.")
    except (DuplicateRequestError, InvalidPriorityError, ValueError) as exc:
        print(f"Error: {exc}")


def handle_view_all(service: RequestService) -> None:
    requests = service.view_requests()
    if not requests:
        print("No service requests found.")
        return

    for req in requests:
        print(format_request_line(req))


def handle_search_request(service: RequestService) -> None:
    request_id = input("Enter Request ID to search: ").strip()
    try:
        req = service.search_request(request_id)
        print_request_details(req)
    except RequestNotFoundError:
        print("Request not found.")


def handle_resolve_request(service: RequestService) -> None:
    request_id = input("Enter Request ID to resolve: ").strip()
    try:
        req = service.resolve_request(request_id)
        print(f"Request {req.request_id} marked as {req.status}.")
    except RequestNotFoundError:
        print("Request not found.")
    except RequestAlreadyResolvedError as exc:
        print(f"Notice: {exc}")


def run() -> None:
    repository = FileRepository("data/requests.json")
    service = RequestService(repository=repository)

    # Verify persistence store is accessible on startup
    service.view_requests()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            handle_create_request(service)
        elif choice == "2":
            handle_view_all(service)
        elif choice == "3":
            handle_search_request(service)
        elif choice == "4":
            handle_resolve_request(service)
        elif choice == "5":
            print("Exiting Smart Service Desk System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    run()
