# Staff Engineer Thinking Process

Step-by-step technical planning and architecture:

1. Technology Stack Decision:
   - Backend: Python (FastAPI for REST API, as it's modern and fast)
   - Database: PostgreSQL for relational data, Redis for caching/session management
   - Frontend: React.js for modern SPA
   - Authentication: JWT tokens
   - Real-time: WebSockets for bidding updates

2. Architecture Planning:
   - Follow clean architecture principles
   - Separate concerns: models, schemas, services, endpoints
   - Use dependency injection
   - Include proper error handling and logging

3. Database Design:
   - Users table (id, email, password_hash, created_at, etc.)
   - Items table (id, title, description, starting_price, current_price, auction_end, seller_id, etc.)
   - Bids table (id, item_id, user_id, amount, timestamp)
   - Categories table for item categorization

4. API Design:
   - RESTful endpoints for CRUD operations
   - WebSocket endpoints for real-time bidding
   - Proper validation using Pydantic schemas
   - Rate limiting for bidding endpoints

5. Security Considerations:
   - Password hashing
   - JWT authentication
   - Input validation and sanitization
   - CORS configuration
   - SQL injection prevention

6. Testing Strategy:
   - Unit tests for all business logic
   - Integration tests for API endpoints
   - 95% code coverage requirement
   - Use pytest framework

7. Deployment Considerations:
   - Docker containers for easy deployment
   - Environment-based configuration
   - Database migrations
   - Logging and monitoring

8. Code Quality:
   - Follow PEP 8 standards
   - Type hints throughout
   - Comprehensive documentation
   - SOLID principles application
