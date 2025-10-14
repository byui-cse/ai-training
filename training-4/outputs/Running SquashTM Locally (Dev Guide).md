# Running SquashTM Locally (Dev Guide)

This guide provides step-by-step instructions for setting up and running SquashTM locally for development purposes.

## Quick Start (TL;DR)

### macOS/Linux
```bash
# 1. Install prerequisites
brew install openjdk@21 node@20 maven docker

# 2. Clone and navigate to project
git clone <repository-url>
cd squashtest-tm-staging

# 3. Start database (H2 - fastest option)
cd database
./gen-db.sh h2

# 4. Start backend
cd ../tm
mvn spring-boot:run -Dspring-boot.run.profiles=h2

# 5. Start frontend (in new terminal)
cd tm-front
yarn install --frozen-lockfile
yarn start

# 6. Access application
open http://localhost:4200/squash
```

### Windows (PowerShell)
```powershell
# 1. Install prerequisites (using Chocolatey)
choco install openjdk21 nodejs maven docker-desktop

# 2. Clone and navigate to project
git clone <repository-url>
cd squashtest-tm-staging

# 3. Start database (H2 - fastest option)
cd database
./gen-db.bat h2

# 4. Start backend
cd ../tm
mvn spring-boot:run -Dspring-boot.run.profiles=h2

# 5. Start frontend (in new PowerShell window)
cd tm-front
yarn install --frozen-lockfile
yarn start

# 6. Access application
start http://localhost:4200/squash
```

## Prerequisites & Versions

| Tool | Required Version | Install Command |
|------|------------------|-----------------|
| **Java** | 21+ | `brew install openjdk@21` (macOS) / `choco install openjdk21` (Windows) |
| **Node.js** | 20+ | `brew install node@20` (macOS) / `choco install nodejs` (Windows) |
| **npm/yarn** | Latest | Included with Node.js |
| **Angular CLI** | 20.1.5+ | `npm install -g @angular/cli@20.1.5` |
| **Maven** | 3.9.9+ | `brew install maven` (macOS) / `choco install maven` (Windows) |
| **Docker** | Latest | `brew install docker` (macOS) / `choco install docker-desktop` (Windows) |

### Verification Commands
```bash
java -version          # Should show Java 21+
node --version         # Should show v20+
npm --version          # Should show 10+
ng version             # Should show Angular CLI 20.1.5+
mvn --version          # Should show Maven 3.9.9+
docker --version       # Should show Docker 24+
```

## Environment Variables & Profiles

### Spring Profiles
SquashTM uses Spring profiles to configure different environments:

- **`h2`** (default): Uses H2 in-memory database - fastest for development
- **`mariadb`**: Uses MariaDB database - production-like setup
- **`postgresql`**: Uses PostgreSQL database - production-like setup
- **`local`**: Local development profile
- **`dev`**: Development profile

### Environment Variables

#### Backend (.env.example)
```bash
# Database Configuration
SPRING_PROFILES_ACTIVE=h2
SPRING_DATASOURCE_URL=jdbc:h2:file:./data/squash-tm;NON_KEYWORDS=ROW,VALUE
SPRING_DATASOURCE_USERNAME=sa
SPRING_DATASOURCE_PASSWORD=

# Server Configuration
SERVER_PORT=8080
SERVER_SERVLET_CONTEXT_PATH=/squash

# Liquibase Configuration
LIQUIBASE_CHANGELOG_FILE=src/main/liquibase/sample/sample-db.changelog.xml
LIQUIBASE_DROP_FIRST=true

# Development Settings
SPRING_DEVTOOLS_RESTART_ENABLED=true
SPRING_DEVTOOLS_LIVERELOAD_ENABLED=true
```

#### Frontend (.env.example)
```bash
# API Configuration
API_BASE_URL=http://localhost:8080/squash/backend
APP_BASE_URL=http://localhost:4200/squash

# Development Settings
NODE_ENV=development
NG_CLI_ANALYTICS=false
```

### Loading Environment Variables
- **Backend**: Spring Boot automatically loads `application.properties` and `application-{profile}.properties`
- **Frontend**: Angular uses environment files (`environment.ts`, `environment.prod.ts`, etc.)
- **Database**: Liquibase properties are configured in Maven settings.xml

## Database Setup

### Option A: H2 Database (Fastest for Development)

H2 is the default database for development and requires no external setup.

```bash
# Navigate to database directory
cd database

# Generate H2 database with sample data
./gen-db.sh h2

# Or generate empty database
./gen-db.sh h2 -empty
```

**What this does:**
- Creates H2 database file at `../tm/data/squash-tm`
- Applies Liquibase changelogs
- Populates with sample data (unless `-empty` flag is used)

### Option B: MariaDB/PostgreSQL (Production-like Setup)

#### Using Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  mariadb:
    image: mariadb:10.11
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: squashtm_dev
      MYSQL_USER: squashtm
      MYSQL_PASSWORD: squashtm
    ports:
      - "3306:3306"
    volumes:
      - mariadb_data:/var/lib/mysql
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

  postgresql:
    image: postgres:15
    environment:
      POSTGRES_DB: squashtm_dev
      POSTGRES_USER: squashtm
      POSTGRES_PASSWORD: squashtm
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  mariadb_data:
  postgres_data:
```

#### Setup Commands
```bash
# Start databases
docker-compose up -d

# Generate MariaDB database
cd database
./gen-db.sh mariadb

# Generate PostgreSQL database
./gen-db.sh postgresql
```

#### Maven Settings Configuration

Add to `~/.m2/settings.xml`:
```xml
<profiles>
  <profile>
    <id>mariadb</id>
    <properties>
      <dev.liquibase.url>jdbc:mariadb://localhost:3306/squashtm_dev</dev.liquibase.url>
      <dev.liquibase.username>squashtm</dev.liquibase.username>
      <dev.liquibase.password>squashtm</dev.liquibase.password>
    </properties>
  </profile>
  <profile>
    <id>postgresql</id>
    <properties>
      <dev.liquibase.url>jdbc:postgresql://localhost:5432/squashtm_dev</dev.liquibase.url>
      <dev.liquibase.username>squashtm</dev.liquibase.username>
      <dev.liquibase.password>squashtm</dev.liquibase.password>
    </properties>
  </profile>
</profiles>
```

### Database Management

#### Recreate Schema
```bash
# Drop and recreate H2 database
cd database
./gen-db.sh h2

# Drop and recreate MariaDB database
./gen-db.sh mariadb

# Drop and recreate PostgreSQL database
./gen-db.sh postgresql
```

#### Apply/Rollback Liquibase Changesets
```bash
# Apply pending changesets
mvn liquibase:update -P<profile>

# Rollback last changeset
mvn liquibase:rollback -P<profile>

# Rollback to specific changeset
mvn liquibase:rollback -Dliquibase.rollbackCount=1 -P<profile>
```

## Backend: Build & Run

### Build Commands
```bash
# Build entire project
mvn clean install

# Build specific modules
mvn clean install -pl tm -am

# Skip tests for faster build
mvn clean install -DskipTests
```

### Run Commands
```bash
# Run with H2 database (default)
cd tm
mvn spring-boot:run

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=mariadb

# Run with custom properties
mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=8080 --spring.profiles.active=h2"
```

### Server Configuration
- **Port**: 8080 (default)
- **Context Path**: `/squash`
- **Base URL**: `http://localhost:8080/squash`

### Health Checks
```bash
# Application health
curl http://localhost:8080/squash/actuator/health

# Application info
curl http://localhost:8080/squash/actuator/info

# Database status
curl http://localhost:8080/squash/backend/api/version
```

### Hot Reload
Spring Boot DevTools is configured for hot reload:
- **Restart**: Automatically restarts application on classpath changes
- **LiveReload**: Automatically refreshes browser on static resource changes
- **Logging**: Enhanced logging for development

## Frontend: Build & Run

### Build Commands
```bash
# Navigate to frontend directory
cd tm/tm-front

# Install dependencies
yarn install --frozen-lockfile

# Build for production
yarn build

# Build for tests
yarn build-tests
```

### Development Server
```bash
# Start development server
yarn start

# Start with test configuration
yarn start-tests

# Start production build locally
yarn start-prod
```

### Server Configuration
- **Port**: 4200 (default Angular dev server)
- **Base URL**: `http://localhost:4200/squash`
- **Proxy**: Routes `/backend/*` requests to `http://localhost:8080`

### Proxy Configuration
The frontend uses `proxy-conf.js` to route API calls to the backend:
```javascript
const apiProxy = createProxyMiddleware('/backend', {
  target: 'http://localhost:8080',
  changeOrigin: true,
});
```

### First-Run Gotchas
- **Angular CLI Cache**: Clear with `ng cache clean`
- **Node Modules**: Use `yarn install --frozen-lockfile` for consistent versions
- **Port Conflicts**: Ensure ports 4200 and 8080 are available
- **CORS Issues**: Proxy configuration handles CORS automatically

### Browser-Sync
Browser-Sync is configured via `bs-config.js` for:
- **Live Reload**: Automatic browser refresh on file changes
- **Proxy**: Routes backend requests to Spring Boot server
- **File Watching**: Monitors file changes for hot reload

## End-to-End Bring-Up

### Step-by-Step Order

1. **Start Database**
   ```bash
   cd database
   ./gen-db.sh h2
   ```

2. **Start Backend**
   ```bash
   cd ../tm
   mvn spring-boot:run -Dspring-boot.run.profiles=h2
   ```

3. **Start Frontend** (in new terminal)
   ```bash
   cd tm/tm-front
   yarn install --frozen-lockfile
   yarn start
   ```

4. **Access Application**
   - Frontend: `http://localhost:4200/squash`
   - Backend API: `http://localhost:8080/squash/backend`

### Expected Responses

#### Backend Health Check
```bash
curl http://localhost:8080/squash/actuator/health
# Expected: {"status":"UP"}
```

#### Frontend Access
```bash
curl http://localhost:4200/squash
# Expected: HTML page with Angular app
```

### Login Defaults
- **Default Admin User**: `admin` / `admin`
- **Sample Users**: Various test users with different roles
- **Login URL**: `http://localhost:4200/squash/login`

### 10-Point Verification Checklist

1. ✅ Backend starts without errors on port 8080
2. ✅ Frontend starts without errors on port 4200
3. ✅ Database connection established (check logs)
4. ✅ Health endpoint responds: `http://localhost:8080/squash/actuator/health`
5. ✅ Frontend loads: `http://localhost:4200/squash`
6. ✅ Login page accessible: `http://localhost:4200/squash/login`
7. ✅ Can login with admin/admin credentials
8. ✅ Dashboard loads after login
9. ✅ Can create a test project
10. ✅ Can create a test case

## Plugins & Integrations

### Available Plugins
- **Report Plugins**: PDF and editable document generation
- **Test Automation**: Jenkins integration
- **Bug Trackers**: Jira, Bugzilla, GitLab, Azure DevOps

### Plugin Development
```bash
# Enable plugin development mode
mvn spring-boot:run -Dspring-boot.run.profiles=h2,dev

# Plugin configuration
# Plugins are loaded from: <project-root>/plugins/
# Plugin JARs should be placed in: <project-root>/tm/plugins/
```

### Environment Variables for Plugins
```bash
# Jenkins Integration
JENKINS_URL=http://localhost:8080
JENKINS_USERNAME=admin
JENKINS_PASSWORD=admin

# Jira Integration
JIRA_URL=https://your-jira-instance.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_PASSWORD=your-api-token
```

### Safe Dev Defaults
- **Timeouts**: 30 seconds for external API calls
- **API Keys**: Use development/test keys only
- **Rate Limiting**: Disabled in development mode

## Testing Hooks

### Backend Tests
```bash
# Unit tests
mvn test

# Integration tests
mvn verify -Pintegration

# Specific test class
mvn test -Dtest=TestClassName

# Skip tests
mvn install -DskipTests
```

### Frontend Tests
```bash
# Unit tests for core library
yarn test-core

# Unit tests for main app
yarn test-app

# Integration tests (Cypress)
yarn integration-tests-cypress-dev

# End-to-end tests
yarn e2e-cypress-postgres
yarn e2e-cypress-mariadb
```

### Testcontainers Usage
SquashTM uses Testcontainers for integration tests:
- **Database**: H2, MariaDB, PostgreSQL containers
- **Dependencies**: Automatic container lifecycle management
- **Ports**: Dynamic port allocation to avoid conflicts

### Service Dependencies
- **Database Ports**: 3306 (MariaDB), 5432 (PostgreSQL)
- **Environment**: Test-specific profiles (`test`, `integration`)
- **Data**: Test data automatically seeded

## Troubleshooting & FAQ

### Common Issues & Fixes

#### Wrong Java/Node Version
```bash
# Check versions
java -version
node --version

# Fix Java version
export JAVA_HOME=/path/to/java21
# or
sdk use java 21.0.0

# Fix Node version
nvm use 20
# or
nvm install 20 && nvm use 20
```

#### Port Conflicts
```bash
# Check port usage
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Kill process using port
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

#### Liquibase Failures
```bash
# Check database connection
mvn liquibase:status -P<profile>

# Reset database
./gen-db.sh <profile>

# Check changelog syntax
mvn liquibase:validate -P<profile>
```

#### CORS/Proxy Errors
```bash
# Check proxy configuration
cat tm/tm-front/proxy-conf.js

# Verify backend is running
curl http://localhost:8080/squash/actuator/health

# Check frontend proxy logs
# Look for proxy errors in browser console
```

#### Missing Environment Variables
```bash
# Check Spring profiles
echo $SPRING_PROFILES_ACTIVE

# Check Maven settings
cat ~/.m2/settings.xml

# Verify database properties
mvn help:effective-settings
```

#### ACL/Permission Blocks
```bash
# Check user permissions
# Login as admin and verify user roles

# Reset admin password
# Use database script or admin interface

# Check Spring Security logs
# Look for authentication/authorization errors
```

### Logging Configuration

#### Backend Logs
```bash
# Increase verbosity
mvn spring-boot:run -Dspring-boot.run.arguments="--logging.level.org.squashtest=DEBUG"

# Log to file
mvn spring-boot:run -Dspring-boot.run.arguments="--logging.file.name=logs/squashtm.log"
```

#### Frontend Logs
```bash
# Browser console logs
# Open Developer Tools (F12) and check Console tab

# Angular CLI logs
yarn start --verbose

# Proxy logs
# Check terminal where frontend is running
```

### Clean Rebuild Commands
```bash
# Clean everything
mvn clean
cd tm/tm-front
yarn clean-dist
rm -rf node_modules
yarn install --frozen-lockfile

# Rebuild from scratch
mvn clean install
cd tm/tm-front
yarn build
```

### Database Reset Tips
```bash
# H2: Delete database file
rm -f tm/data/squash-tm.*

# MariaDB/PostgreSQL: Drop and recreate
docker-compose down -v
docker-compose up -d
./gen-db.sh <profile>
```

## Appendices

### Docker Compose (Database Only)
```yaml
version: '3.8'
services:
  mariadb:
    image: mariadb:10.11
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: squashtm_dev
      MYSQL_USER: squashtm
      MYSQL_PASSWORD: squashtm
    ports:
      - "3306:3306"
    volumes:
      - mariadb_data:/var/lib/mysql
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

  postgresql:
    image: postgres:15
    environment:
      POSTGRES_DB: squashtm_dev
      POSTGRES_USER: squashtm
      POSTGRES_PASSWORD: squashtm
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  mariadb_data:
  postgres_data:
```

### Proxy Configuration
```javascript
// tm/tm-front/proxy-conf.js
const { createProxyMiddleware } = require('http-proxy-middleware');

const apiProxy = createProxyMiddleware('/backend', {
  target: 'http://localhost:8080',
  changeOrigin: true,
});

module.exports = {
  server: {
    middleware: {
      10: apiProxy,
    },
    baseDir: "./dist/sqtm-app"
  },
  open: false,
  watchOptions: { ignored: '**/*.*' },
};
```

### Makefile/package.json Scripts
```json
{
  "scripts": {
    "dev:all": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "cd ../tm && mvn spring-boot:run -Dspring-boot.run.profiles=h2",
    "dev:frontend": "yarn start",
    "dev:db": "cd ../database && ./gen-db.sh h2",
    "dev:reset": "npm run dev:db && npm run dev:all"
  }
}
```

### Environment Files
```typescript
// tm/tm-front/projects/sqtm-app/src/environments/environment.ts
export const environment = {
  production: false,
  apiBaseUrl: 'http://localhost:8080/squash/backend',
  appBaseUrl: 'http://localhost:4200/squash',
  sqtmExperimentalFeatureFlags: {}
};
```

---

**Note**: This guide is based on SquashTM version 12.0.0-SNAPSHOT with Spring Boot 3.5.4 and Angular 20.1.7. Always refer to the latest documentation for version-specific changes.
