# FastAPI Clean Architecture Starter

A Python starter project following **Clean Architecture** with FastAPI, Docker, and PostgreSQL.

## Project Structure

```
fastapi-strter/
├── src/
│   ├── main.py                 # FastAPI app entry point
│   ├── domain/                 # Domain layer
│   │   ├── entities/
│   │   ├── repositories/       # Ports (ABC interfaces)
│   │   ├── exceptions/
│   │   └── constants/
│   ├── application/           # Application layer
│   │   ├── use_cases/
│   │   ├── dto/
│   │   ├── interfaces/         # Ports for external services
│   │   └── exceptions/
│   ├── infrastructure/        # Infrastructure layer
│   │   ├── config/
│   │   ├── adapters/outbound/
│   │   ├── database/postgresql/
│   │   └── di/
│   └── api/                   # API layer
│       ├── routes/
│       └── dependencies.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Running the Application

### With Docker

```bash
cp .env.example .env
docker compose up --build
```

The API will be available at `http://localhost:8000`.

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (or use Docker for postgres only)
docker compose up postgres -d

# Copy env and run
cp .env.example .env
uvicorn src.main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/users/{user_id}` | Get user by ID |
| POST | `/api/v1/users` | Create user |
| PATCH | `/api/v1/users/{user_id}` | Update user |
| DELETE | `/api/v1/users/{user_id}` | Delete user |

## Conventions

- **Async/await** for all I/O operations
- **Domain** and **application** layers do not import from infrastructure
- **Interfaces (ports)** live in `application/interfaces`
- **Entities** use `dataclass` with `from_dict` / `to_dict` (no ORM)
- **DTOs** use Pydantic for validation

## Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
