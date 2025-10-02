# Auction Website

A modern, clean auction website built with Python FastAPI backend and HTML/CSS/JavaScript frontend.

## Features

- User registration and authentication
- Create and manage auction listings
- Real-time bidding system
- Modern, responsive UI design
- RESTful API backend

## Tech Stack

### Backend
- **Python 3.13**
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing

### Frontend
- **HTML5/CSS3** - Modern semantic markup and styling
- **Vanilla JavaScript** - No frameworks for simplicity
- **Inter Font** - Clean, modern typography
- **Responsive Design** - Works on all devices

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation & Setup

1. **Backend Setup:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python init_db.py  # Initialize database
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   # No setup required - static files
   ```

### Running the Application

1. **Start Backend API:**
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```
   Backend will be available at: http://localhost:8000

2. **Start Frontend:**
   ```bash
   cd frontend
   python3 server.py
   ```
   Frontend will be available at: http://localhost:3000

### API Documentation

When the backend is running, visit:
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

## Project Structure

```
auction/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── db/           # Database setup
│   ├── main.py           # FastAPI app entry point
│   ├── init_db.py        # Database initialization
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── index.html        # Main HTML page
│   ├── static/
│   │   ├── css/style.css # Main stylesheet
│   │   └── js/app.js     # Frontend JavaScript
│   └── server.py         # Simple HTTP server
├── docs/
│   ├── BACKLOG.md        # Product requirements
│   ├── PRODUCT_OWNER.md  # Customer-focused analysis
│   ├── STAFF_ENGINEER.md # Technical planning
│   ├── DECISIONS.md      # Major decisions
│   └── SCRATCHPAD.md     # Running notes
└── README.md
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Users
- `GET /users/me` - Get current user
- `PUT /users/me` - Update current user

### Items (Auctions)
- `GET /items/` - List auctions
- `POST /items/` - Create auction
- `GET /items/{id}` - Get auction details
- `PUT /items/{id}` - Update auction
- `POST /items/{id}/activate` - Activate auction

### Bids
- `GET /bids/item/{item_id}` - Get bids for auction
- `POST /bids/` - Place bid
- `GET /bids/user/me` - Get user's bids

## Development Notes

### Database
- Uses SQLite for development
- Tables auto-created on startup
- Run `python init_db.py` to initialize/reset database

### Testing
- Unit tests: `pytest` (95%+ coverage target)
- API tests: HTTP requests to running server

### Security
- JWT token authentication
- Password hashing with bcrypt
- Input validation with Pydantic
- CORS enabled for frontend integration

## MVP Features

✅ User registration and login
✅ Auction listing creation
✅ Basic bidding functionality
✅ Modern responsive UI
✅ REST API backend

## Future Enhancements

🔄 Real-time bid updates (WebSocket)
🔄 Image upload for listings
🔄 Advanced search and filtering
🔄 Email notifications
🔄 Payment integration
🔄 Admin panel

## Contributing

1. Follow the established patterns in the codebase
2. Write tests for new features
3. Update documentation as needed
4. Ensure code follows PEP 8 standards

## License

This project is part of a development exercise and is not intended for production use without further security and performance optimizations.
