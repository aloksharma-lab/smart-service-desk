# Smart Service Desk Management System

## Problem Statement
Employees report IT issues (such as laptop, software, network, password, account, and access problems) that are currently tracked manually. This CLI application allows support staff to create, view, search, and resolve service requests with persistent JSON storage.

## Implemented Features
- Create a new service request (`OPEN` by default) with duplicate Request ID and priority validation
- View all saved service requests
- Search for a service request by Request ID
- Resolve an `OPEN` service request (`OPEN` -> `RESOLVED`) and persist updates
- Safe loading and saving using `data/requests.json` (handles missing or empty files)

## Concepts Used
- **OOP**: Encapsulated `ServiceRequest` entity with `resolve()` state transition and validation
- **Exception Handling**: Custom domain exceptions (`DuplicateRequestError`, `RequestNotFoundError`, `InvalidPriorityError`, `RequestAlreadyResolvedError`) and explicit input validation
- **File Handling**: JSON serialization/deserialization in `FileRepository`
- **SOLID (SRP & DIP)**: Separate classes for domain state, use cases, JSON persistence, and CLI I/O; `RequestService` depends on a repository abstraction (`RequestRepository`)
- **Basic DDD**: Organized into `domain/`, `application/`, `infrastructure/`, and presentation (`main.py`)
- **Git**: Feature work on `development` with multiple commits merged into `main`

## Project Folder Structure
```text
smart-service-desk/
├── domain/
│   ├── __init__.py
│   ├── exceptions.py
│   └── service_request.py
├── application/
│   ├── __init__.py
│   └── request_service.py
├── infrastructure/
│   ├── __init__.py
│   └── file_repository.py
├── data/
│   └── requests.json
├── main.py
├── README.md
└── .gitignore
