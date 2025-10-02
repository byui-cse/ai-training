# Major Decisions - Auction Website

## Technology Stack
**Decision**: Python backend with HTML/CSS frontend
**Rationale**: Meets requirements, Python is robust for backend logic, HTML/CSS provides modern clean UI without complexity
**Date**: October 2, 2025

## Architecture Approach
**Decision**: Clean Architecture with domain-driven design
**Rationale**: Maintains separation of concerns, testable code, scalable for future enhancements
**Date**: October 2, 2025

## MVP Scope
**Decision**: Core auction features only (users, items, bidding, basic UI)
**Rationale**: Focus on validating core product before adding advanced features like real-time bidding or payments
**Date**: October 2, 2025

## Database Choice
**Decision**: SQLite for development, PostgreSQL for production
**Rationale**: SQLite simple for initial development, PostgreSQL provides production reliability
**Date**: October 2, 2025

## Framework Selection
**Decision**: FastAPI for backend (Python async framework)
**Rationale**: Modern, fast, auto-generates OpenAPI docs, excellent for REST APIs
**Date**: October 2, 2025

## Testing Requirements
**Decision**: 95%+ code coverage with pytest
**Rationale**: Ensures code quality and prevents regressions
**Date**: October 2, 2025

## Security Standards
**Decision**: JWT authentication, bcrypt password hashing, input validation
**Rationale**: Industry standard security practices for user data protection
**Date**: October 2, 2025
