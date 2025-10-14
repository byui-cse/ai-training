## **Context (repo facts)**

* **Project:** SquashTM — web-based Test Management System.

* **Stacks:**

  * **Frontend:** Angular **20+** SPA at `tm/tm-front/` (with `projects/sqtm-app` and shared lib `projects/sqtm-core/`; `angular.json`, `package.json`, `bs-config.js`).

  * **Backend:** Spring Boot **3.5.4** (Java 17+) across Maven modules: `core/`, `tm/` (`tm.domain`, `tm.service`, `tm.web`), plus plugins.

  * **Database:** H2 / MariaDB / PostgreSQL managed by **Liquibase** (`database/` changelogs).

  * **Scripts mentioned:** `database/gen-db.sh` for dev DB setup.

* **Invariants:** Keep REST contracts, ACL/permissions, plugin extension points intact.

## **What to produce (deliverables)**

Create a **single Markdown document** titled **“Running SquashTM Locally (Dev Guide)”** that contains:

1. **Quick Start (TL;DR)**

   * One-page, copy-paste sequence for the **fastest path** to a running system (backend \+ DB \+ frontend), assuming macOS/Linux, and a second sequence for Windows (PowerShell).

   * Include **exact commands** (auto-detected from repo): installing tool versions, starting DB, starting backend, starting frontend, verifying health.

2. **Prerequisites & Versions**

   * Confirm **Java (17+)**, **Node (18+)**, **npm**, **Angular CLI**, **Maven**, **Docker** (optional) with minimal install commands per OS.

   * Provide an **env matrix** table with required tools and verified versions.

3. **Environment Variables & Profiles**

   * List **all required env vars** and their meanings (read from code/properties).

   * Provide a ready-to-use **`.env.example`** (for both backend and frontend) and explain how it is loaded (Spring profiles, Angular environment files, or dotenv if applicable).

   * Explain **Spring profiles** to use for dev (e.g., `local`, `dev`) and how they toggle DBs (H2 vs MariaDB/Postgres).

4. **Database Setup (two options)**

   * **Option A (fastest): H2 dev profile** — how to start backend against H2 with Liquibase auto-apply.

   * **Option B: MariaDB/PostgreSQL** — provide a **`docker-compose.yml`** snippet (ports, volumes, users/passwords) and usage commands.

   * Include how to use `database/gen-db.sh` and what it does (create db, user, apply Liquibase).

   * Show how to **recreate schema** safely and how to **apply/rollback** Liquibase changeSets in dev.

5. **Backend: Build & Run**

   * Commands to **build** and **run** the Spring Boot app from the correct module(s) (e.g., `mvn -q -pl tm/web spring-boot:run` or repo-specific start module you detect).

   * Port(s) and base URL; add **health checks** (e.g., `/actuator/health`, `/api/version`) and **sanity curl** examples.

   * Notes on hot reload (DevTools, if present) and logging config.

6. **Frontend: Build & Run**

   * From `tm/tm-front/`: `npm ci`, `npm start` (or the actual script name) and how the dev server proxies to backend (include proxy config if present).

   * Dev server port (auto-detect), **first-run gotchas** (Angular CLI cache, node-gyp, etc.).

   * How to enable Browser-Sync (if used via `bs-config.js`) or equivalent.

7. **End-to-End Bring-Up**

   * Step-by-step order: DB → backend → frontend.

   * URLs to open, expected successful responses, and **login defaults** (if applicable).

   * A **10-point verification checklist** (e.g., create a test case, list requirements, run minimal flow).

8. **Plugins & Integrations (Jenkins, reports, automation)**

   * How to enable/disable dev plugins, where to place them, and any env vars needed.

   * Mention timeouts, API keys, and safe dev defaults.

9. **Testing Hooks (optional but useful)**

   * How to run **unit**, **integration**, and **E2E** tests for both backend and frontend (commands you detect).

   * Note **Testcontainers** usage if present and any service dependencies (db ports, env).

10. **Troubleshooting & FAQ**

* Common issues & fixes: wrong Java/Node version, port conflicts, Liquibase failures, CORS/proxy errors, missing env vars, ACL blocks.

* Where to see logs and how to increase verbosity.

* Clean rebuild commands and DB reset tips.

11. **Appendices (copy-paste artifacts)**

* `docker-compose.yml` (DB only).

* `.env.example` for backend & frontend.

* `proxy.conf.json` (if needed by Angular).

* A minimal **Makefile**/**package.json** scripts section (e.g., `make dev`, `npm run dev:all`) if none exist, wiring all steps.

## **Method & accuracy rules**

* **Auto-detect everything** from the repository: ports, module names, Spring profiles, health endpoints, npm scripts, Liquibase changelog path, and the presence/usage of `database/gen-db.sh`.

* If something is ambiguous, **search the codebase** (package names, `@SpringBootApplication`, `application-*.yml`, `angular.json`, `package.json`, `bs-config.js`, Liquibase changelogs) and **state the exact file/line** used to derive the value.

* Prefer **behavior-verified commands** (build then run) and include **copy-paste blocks** for macOS/Linux and PowerShell.

* Keep steps **idempotent** and safe; no destructive DB operations unless clearly labeled.

* Use concise language, headings, and bullet lists; avoid hand-wavy instructions.

## **Final output format**

Return **only** the Markdown guide with this outline:

1. Title \+ Short intro

2. Quick Start (macOS/Linux, Windows)

3. Prerequisites & Versions

4. Environment Variables & Profiles (+ `.env.example`)

5. Database Setup (H2 & Docker Compose)

6. Backend: Build & Run (+ health checks)

7. Frontend: Build & Run (+ proxy)

8. End-to-End Bring-Up & Verification Checklist

9. Plugins & Integrations

10. Testing Hooks

11. Troubleshooting & FAQ

12. Appendices (docker-compose, proxy config, Makefile/package scripts)

Ensure all commands are **exact** and **validated against the repo structure** you detect.

