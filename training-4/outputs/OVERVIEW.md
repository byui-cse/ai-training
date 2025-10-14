# SquashTM Codebase Analysis

## 1. High-level Overview

**What does this project do overall?**
- **SquashTM** is a comprehensive **Test Management System** that serves as a repository for test cases, requirements, and helps plan and execute test campaigns
- It's a **web-based application** for managing the entire software testing lifecycle

**What kind of system is it?**
- **Full-stack web application** with:
  - **Frontend**: Angular 20+ SPA (Single Page Application)
  - **Backend**: Spring Boot 3.5.4 Java application
  - **Database**: Multi-database support (H2, MariaDB, PostgreSQL)
  - **Architecture**: Modular Maven-based system with plugin architecture

## 2. Architecture Summary

**Main directories and their roles:**

### Core Modules (`core/`)
- **`core.api`**: Plugin APIs and entry points for external integrations
- **`core.foundation`**: Base utilities and foundational classes
- **`core.bugtracker.api`**: Bug tracking system integrations
- **`core.report.api`**: Reporting system APIs
- **`core.testautomation.api`**: Test automation framework APIs
- **`core.dynamicmanager`**: Dynamic component management
- **`core.aspect`**: Aspect-oriented programming support

### Main Application (`tm/`)
- **`tm-front/`**: Angular frontend application
  - **`projects/sqtm-app/`**: Main Angular application
  - **`projects/sqtm-core/`**: Shared Angular library
- **`tm.domain`**: Business domain models and entities
- **`tm.service`**: Business logic and services layer
- **`tm.web`**: Web controllers and REST endpoints

### Database Layer (`database/`)
- **Liquibase** for database schema management
- **Multi-database support** (H2, MariaDB, PostgreSQL)
- **Migration scripts** and changelog management

### Plugin System (`plugins/`)
- **Report plugins**: PDF and editable document generation
- **Test automation plugins**: Jenkins integration
- **Extensible architecture** for custom functionality

**Key entry points:**
- **Frontend**: `tm/tm-front/projects/sqtm-app/src/app/app.module.ts` (Angular bootstrap)
- **Backend**: Spring Boot application (main class not visible in current structure)
- **Database**: Liquibase changelogs in `database/src/main/liquibase/`

**Dependencies between major components:**
```
Frontend (Angular) ↔ REST API ↔ Service Layer ↔ Domain Layer ↔ Database
     ↓
Plugin System ↔ Core APIs ↔ Foundation Layer
```

## 3. Core Functionality

**Main features and business capabilities:**

### Test Management
- **Test Case Management**: Create, organize, and maintain test cases
- **Test Execution**: Plan and execute test campaigns
- **Test Results Tracking**: Monitor execution results and status

### Requirements Management
- **Requirements Repository**: Store and manage requirements
- **Traceability**: Link requirements to test cases
- **Version Control**: Track requirement changes

### Campaign Management
- **Test Campaigns**: Organize test execution cycles
- **Iterations**: Manage sprint-based testing
- **Milestones**: Track project progress

### Reporting & Analytics
- **Custom Reports**: Generate various report formats (PDF, DOCX)
- **Dashboard**: Visual analytics and metrics
- **Export Capabilities**: Data export in multiple formats

### Integration Capabilities
- **Bug Trackers**: Jira, Bugzilla, GitLab, Azure DevOps, etc.
- **Test Automation**: Jenkins, Selenium integration
- **SCM Integration**: Git-based source control
- **Authentication**: LDAP, SAML, OAuth2 support

### Administration
- **User Management**: Role-based access control
- **Project Management**: Multi-project support
- **System Configuration**: Environment and server management

## 4. Data Flow

**How data flows through the system:**

```
User Interface (Angular) 
    ↓ HTTP/REST
Backend Controllers (Spring Boot)
    ↓ Service Layer
Business Logic & Domain Models
    ↓ JPA/Hibernate
Database (H2/MariaDB/PostgreSQL)
```

**Key APIs and services:**
- **REST API**: `/backend/*` endpoints for frontend communication
- **Plugin APIs**: Extensible plugin system for integrations
- **Authentication**: Spring Security with ACL-based permissions
- **Database**: JPA/Hibernate with Liquibase migrations

## 5. Key Classes/Functions

**Important system components:**

### Frontend (Angular)
- **`AppComponent`**: Main application bootstrap
- **`AppModule`**: Application configuration and routing
- **`SqtmCoreModule`**: Core shared functionality
- **Route modules**: Lazy-loaded feature modules for different workspaces

### Backend (Java)
- **Entity Types**: `PROJECT`, `TEST_CASE`, `REQUIREMENT`, `CAMPAIGN`, `EXECUTION`
- **Plugin System**: `PluginName` enum with various integration types
- **Security**: `Roles` and `Permissions` for access control
- **Database**: Liquibase changelog management

### Core APIs
- **Plugin APIs**: For external system integrations
- **Security APIs**: Authentication and authorization
- **Report APIs**: Custom reporting functionality

## 6. Configuration & Environment

**Configuration files and their purpose:**

### Maven Configuration
- **`pom.xml`**: Main project configuration with multi-module structure
- **`settings.xml`**: Maven repository and server configuration
- **Database profiles**: H2, MariaDB, PostgreSQL support

### Frontend Configuration
- **`package.json`**: Node.js dependencies and build scripts
- **`angular.json`**: Angular CLI configuration
- **`bs-config.js`**: Browser-sync proxy configuration for development

### Database Configuration
- **Liquibase changelogs**: Database schema and migration scripts
- **Database profiles**: Environment-specific database configurations
- **Migration scripts**: Automated database updates

### Build & Deployment
- **Maven profiles**: Different build configurations
- **Docker support**: Containerized deployment options
- **CI/CD**: GitLab pipeline configuration

## 7. Potential Next Steps for Onboarding

**To become productive quickly, explore in this order:**

### 1. **Start with the Frontend** (if working on UI)
- **`tm/tm-front/projects/sqtm-app/src/app/app.module.ts`**: Understand the main application structure
- **Route modules**: Explore different workspace modules (test-case-workspace, campaign-workspace, etc.)
- **Core library**: `tm/tm-front/projects/sqtm-core/` for shared components

### 2. **Understand the Domain Model** (if working on business logic)
- **Entity types**: Study the main business entities in `core/core.api/src/main/java/org/squashtest/tm/api/plugin/EntityType.java`
- **Database schema**: Review Liquibase changelogs in `database/src/main/liquibase/`
- **Permissions system**: Understand the security model in `docs/PERMISSIONS.md`

### 3. **Explore Integration Points** (if working on APIs/plugins)
- **Plugin system**: Review `core/core.api/` for plugin development
- **REST endpoints**: Study the backend service layer
- **Authentication**: Understand Spring Security integration

### 4. **Development Setup**
- **Database setup**: Use `database/gen-db.sh` to create development database
- **Frontend development**: Run `npm start` in `tm/tm-front/`
- **Backend development**: Maven-based Spring Boot application

### 5. **Testing & Quality**
- **Integration tests**: `tm-integration/` module
- **Frontend tests**: Cypress E2E tests in `tm/tm-front/cypress/`
- **Unit tests**: Groovy-based tests in various modules

### 6. **Documentation to Read**
- **`docs/PERMISSIONS.md`**: Security and permissions system
- **`docs/EXPERIMENTAL_FEATURE_FLAGS.md`**: Feature flag system
- **`tm/tm-front/docs/PLUGIN_DEVELOPMENT.md`**: Plugin development guide
- **`database/README.md`**: Database management

This system is a mature, enterprise-grade test management platform with extensive customization and integration capabilities. The modular architecture makes it relatively easy to understand and extend once you grasp the core concepts.
