# Major Decisions

All major architectural and implementation decisions are recorded here.

## Technology Stack Decisions
- Backend Framework: FastAPI (Python) - Modern, fast, automatic API documentation, async support
- Database: PostgreSQL - Robust relational database for auction data with ACID compliance
- ORM: SQLAlchemy - Mature Python ORM with excellent PostgreSQL support
- Authentication: JWT tokens with refresh token rotation for security
- Real-time Features: WebSockets via FastAPI WebSocket support
- Caching: Redis for session management and caching (future enhancement)
- Frontend: React.js with TypeScript - Modern SPA with type safety
- State Management: React Context/Redux Toolkit for complex state
- UI Framework: Material-UI or Tailwind CSS for consistent design
- Testing: pytest for backend, Jest/React Testing Library for frontend

## Architecture Decisions
- Clean Architecture pattern with separated concerns (models, schemas, services, endpoints)
- Dependency injection via FastAPI dependency system for testability
- RESTful API design with proper HTTP status codes and error responses
- Event-driven architecture for real-time bidding updates using WebSockets
- Repository pattern for data access abstraction
- Service layer for business logic encapsulation
- CQRS pattern consideration for complex bidding operations (future)

## Project Structure Decisions
- Backend: app/ directory with api/, core/, db/, models/, schemas/, services/ subdirectories
- Frontend: src/ directory with components/, hooks/, pages/, services/, utils/ subdirectories
- Tests: Separate tests/ directory mirroring application structure
- Docker: Multi-stage builds for optimized production images

## Database Design Decisions
- Normalized relational schema for auction entities
- Foreign key relationships for data integrity
- Indexing strategy for performance (user queries, item searches, bidding operations)

## Security Decisions
- Password hashing using bcrypt
- JWT authentication with refresh tokens
- Input validation using Pydantic
- Rate limiting on bidding endpoints to prevent abuse

## Testing Decisions
- pytest framework for all testing
- 95% minimum code coverage requirement
- Unit tests for business logic, integration tests for API endpoints
- Mock external dependencies for isolated testing
