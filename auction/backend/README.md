# Auction Website Backend

FastAPI backend for the auction website with PostgreSQL database.

## Features

- **User Management**: Registration, authentication, JWT tokens
- **Item Management**: Create, list, and browse auction items
- **Bidding System**: Place bids with validation and real-time updates
- **Auction Logic**: Automatic auction timing and winner determination
- **Categories**: Organize items by categories
- **RESTful API**: Well-documented API with OpenAPI/Swagger

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Validation**: Pydantic
- **Testing**: pytest
- **Documentation**: Automatic OpenAPI docs

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL database

### Installation

1. **Clone and navigate to backend directory:**
   ```bash
   cd auction/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database:**
   ```bash
   python init_db.py
   ```

6. **Run the application:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/v1/openapi.json`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Users
- `GET /api/v1/users/` - List users (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user

### Items (TODO)
- `GET /api/v1/items/` - List auction items
- `POST /api/v1/items/` - Create new auction item
- `GET /api/v1/items/{item_id}` - Get item details
- `PUT /api/v1/items/{item_id}` - Update item

### Bids (TODO)
- `POST /api/v1/bids/` - Place a bid
- `GET /api/v1/bids/item/{item_id}` - Get bids for item

### Categories (TODO)
- `GET /api/v1/categories/` - List categories
- `POST /api/v1/categories/` - Create category (admin only)

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

### Type Checking

```bash
mypy .
```

### Database Migrations (Future)

```bash
alembic revision --autogenerate -m "Migration message"
alembic upgrade head
```

## Sample Data

The `init_db.py` script creates sample users, categories, items, and bids for testing:

**Users:**
- admin@example.com / admin (admin user)
- john@example.com / john_doe
- jane@example.com / jane_smith
- bob@example.com / bob_wilson

**Password for all users:** password123

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/     # API route handlers
│   ├── core/              # Configuration and core functionality
│   ├── db/                # Database session and models
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic services
├── tests/                 # Unit and integration tests
├── main.py               # FastAPI application entry point
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── env.example          # Environment configuration example
└── README.md            # This file
```

## Contributing

1. Follow the established code style (Black, isort, mypy)
2. Write tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass before submitting

## License

This project is part of an AI training exercise.
