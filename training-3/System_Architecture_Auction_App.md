# System Architecture — Simple Auction App (MVP)

**Version:** 1.0  
**Date:** 2025-10-08  
**Owner:** [Your Team]  
**Status:** Draft

---

## 1. Overview

This document describes the architecture for the **Simple Auction App (MVP)** delivering three capabilities:
1) Existing user login  
2) New user registration  
3) Viewing available auction items

The solution is a **Spring Boot monolith** with a **PostgreSQL** database, a **client-side HTML/CSS/JS frontend using Tailwind**, and is deployed using **Docker containers**. Authentication is **Spring Security form login with server sessions (cookie-based)**. **No external integrations** are included in this version. **In-memory session storage** is used.

---

## 2. High-Level Architecture

```mermaid
flowchart LR
  U[User Browser] -- HTTPS --> LB[Load Balancer/Reverse Proxy]
  LB --> W[Spring Boot Container]
  subgraph Docker Environment
    W --> C[Controllers (Spring MVC)]
    C --> S[Services]
    S --> R[Repositories (JPA)]
    R --> DB[(PostgreSQL Container)]
  end
  U <--> ST[Static Assets (Tailwind, JS)]
```

**Key decisions**
- **Runtime:** Spring Boot monolith for simplicity and fast iteration.  
- **Frontend:** Simple client-rendered HTML + Tailwind CSS delivered by the monolith (static assets served by Spring).  
- **Auth:** Spring Security form login; session cookie maintained by container (in-memory session).  
- **Data:** PostgreSQL for durable storage of users and auction items.  
- **Deployment:** Docker containers with docker-compose for local development and container orchestration for production.  
- **Operations:** Containerized deployment with health checks and proper logging.

---

## 3. Functional Scope (MVP)

- **Registration**: Create account (name, email, password).  
- **Login**: Form-based authentication, server-side session.  
- **Browse Items**: Authenticated users can view active auction items list.

Out of scope (future): bidding, payments, images, categories, admin, notifications, analytics.

---

## 4. Component View

### 4.1 Web Layer (Controllers)
- **AuthController**: `/login`, `/logout`, `/register`  
- **ItemController**: `/items` (list active items)
- Serves static assets: `/static/**` (HTML, CSS, JS, Tailwind build)

### 4.2 Service Layer
- **AuthService**: registration flow (hash password), login helper, profile retrieval.
- **ItemService**: list active items, sorting/pagination.

### 4.3 Data Access Layer
- **UserRepository (JPA)**: CRUD for `User`.
- **ItemRepository (JPA)**: queries for active items.

### 4.4 Security
- **Spring Security** with form login, session cookie, CSRF enabled for state-changing routes.
- Passwords hashed (BCrypt).
- Access rules:
  - `/login`, `/register`, `/static/**` — permit all  
  - `/items/**` — authenticated

---

## 5. Data Model (MVP)

```mermaid
erDiagram
  USER ||--o{ ITEM : "created_by (optional future)"
  USER {
    UUID id PK
    string name
    string email UNIQUE
    string password_hash
    datetime created_at
  }
  ITEM {
    UUID id PK
    string title
    text description
    string image_url  "optional - may be blank"
    decimal current_bid "default 0"
    datetime end_time
    boolean active
    datetime created_at
  }
```

**Notes**
- Email is unique for login.  
- `image_url` is optional placeholder for future media support.  
- `active` filters visible items.

---

## 6. Request Flows

### 6.1 Registration
1. User submits form (name, email, password).  
2. `AuthController` → `AuthService`: validate, check unique email.  
3. Hash password (BCrypt), persist `User`.  
4. Redirect to login page with success message.

### 6.2 Login (Form + Session)
1. User posts credentials to `/login`.  
2. Spring Security `AuthenticationManager` validates credentials via `UserDetailsService`.  
3. On success, container issues session cookie; user redirected to `/items`.  
4. On failure, show error; do not reveal which field failed.

### 6.3 View Items
1. Authenticated GET `/items`.  
2. `ItemController` → `ItemService` → `ItemRepository` query active items.  
3. Render HTML template + client JS/Tailwind; return JSON if needed for dynamic filtering/pagination (optional).

---

## 7. Configuration

### 7.1 Spring Profiles
- `dev`: local developer settings; `spring.jpa.hibernate.ddl-auto=create`, verbose logs.  
- `docker`: containerized environment with PostgreSQL container, optimized logging.
- `prod`: production settings with managed migrations (Flyway), minimal logs.

### 7.2 Application Properties (examples)
```
# Docker environment
spring.datasource.url=jdbc:postgresql://postgres:5432/auction_app
spring.datasource.username=${DB_USER}
spring.datasource.password=${DB_PASSWORD}
spring.jpa.hibernate.ddl-auto=update
spring.flyway.enabled=true
management.endpoints.web.exposure.include=health,info
```

### 7.3 Security
```
server.servlet.session.cookie.secure=true
server.servlet.session.cookie.http-only=true
server.servlet.session.timeout=30m
spring.security.filter.dispatcher-types=REQUEST,ERROR
```

---

## 8. Environments (Docker)

### 8.1 Local Development
- **Profile**: `docker`  
- **DB**: PostgreSQL container via docker-compose  
- **Environment**: `DB_USER`, `DB_PASSWORD`, `DATABASE_URL`  
- **Scaling**: Single instance (in-memory sessions acceptable)

### 8.2 Production
- **Profile**: `prod`  
- **DB**: Managed PostgreSQL or containerized PostgreSQL  
- **Environment**: `DB_USER`, `DB_PASSWORD`, `DATABASE_URL`  
- **TLS**: Reverse proxy/load balancer managed HTTPS  
- **Scaling**: Container orchestration (Docker Swarm, Kubernetes); if scaling horizontally, **migrate sessions** to Redis or JDBC (Spring Session).

---

## 9. Deployment (Docker)

### 9.1 Local Development
- Build: `docker-compose up --build`  
- Start: `docker-compose up`  
- Stop: `docker-compose down`  
- Environment variables set in docker-compose.yml or .env file.

### 9.2 Production Deployment
- Build: `docker build -t auction-app .`  
- Run: `docker run -p 8080:8080 -e SPRING_PROFILES_ACTIVE=prod auction-app`  
- Or use container orchestration (Docker Swarm, Kubernetes) for production scaling.

**Container orchestration** recommended for production environments.

---

## 10. Observability & Ops (Containerized)

- **Logging**: Spring Boot default logging to stdout; container logs via `docker logs` or log aggregation systems.  
- **Health**: Spring Boot Actuator `/actuator/health` with Docker health checks.  
- **Backups**: Container volume backups or managed database backups.  
- **Error Handling**: Global exception handler (ControllerAdvice) returning friendly error pages.
- **Monitoring**: Container metrics via Docker stats or orchestration platform monitoring.

---

## 11. Security Considerations

- BCrypt for passwords; never store plaintext.  
- CSRF protection for state-changing endpoints.  
- Secure, HttpOnly session cookie; set `SameSite=Lax` (default) or `Strict` as needed.  
- Input validation on registration fields.  
- Limit login attempts (optional), generic error messages.  
- HTTPS enforced end-to-end (reverse proxy/load balancer).
- Container security: non-root user, minimal base images, security scanning.

---

## 12. Risks & Future Work

- **In-memory sessions** will cause logouts on restarts and break if horizontally scaling; plan migration to **Redis** or **JDBC Spring Session** when adding more instances.  
- **No external storage** for images; if required later, integrate S3/Cloudinary.  
- Add **bidding** domain, **rate limiting**, **metrics/monitoring**, **CI/CD**, and **migrations** in future iterations.
- **Container orchestration** complexity increases with scale; consider managed Kubernetes services.

---

## 13. Appendix: Minimal Package Structure

```
com.example.auction
├─ config/           # SecurityConfig, WebConfig
├─ controller/       # AuthController, ItemController
├─ domain/           # User, Item (JPA entities)
├─ repository/       # UserRepository, ItemRepository
├─ service/          # AuthService, ItemService
├─ dto/              # request/response DTOs (optional)
└─ static/ & templates/  # HTML, CSS (Tailwind), JS
```

---

© 2025 Your Company — Internal use only.
