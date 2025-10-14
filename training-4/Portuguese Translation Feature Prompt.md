**Role:** You are an **Internationalization (i18n) Architect \+ Implementer**. Analyze the repository and produce a **safe, incremental plan** to add **Portuguese** language support across frontend and backend, including runtime switching, formatting, tests, CI, and rollout.

## **Context (repo facts)**

* **Project:** SquashTM — web-based Test Management System with plugin architecture.

* **Frontend:** **Angular 20+** at `tm/tm-front/` (`projects/sqtm-app`, shared lib `projects/sqtm-core/`).

* **Backend:** **Spring Boot 3.5.4** (Java 17+): `tm.domain`, `tm.service`, `tm.web`, plus `core/`.

* **Database:** Liquibase migrations under `database/` targeting H2/MariaDB/PostgreSQL.

* **Constraints:** Preserve REST contracts, ACL/permissions, and plugin extension points. Avoid destructive DB changes.

* **Target locale:** `<choose one: pt-BR or pt-PT>` (explain choice and where it matters; support future second variant via fallback).

## **What to analyze (auto-detect; cite paths/files)**

1. **Current i18n status**

   * Frontend: any existing i18n libs (`@ngx-translate`, Angular built-in i18n, ICU message usage), pipes, locale data registration, date/number/currency formatting.

   * Backend: existing `MessageSource`, `LocaleResolver`, validation message bundles, Accept-Language handling, email/report templates.

   * Plugins & reports: strings in plugins, export formats (CSV/PDF), scheduled emails.

2. **User-visible strings & patterns**

   * Hard-coded English strings in Angular components/templates/services.

   * Server-side error/validation messages, log/event messages that surface to UI.

   * Format-sensitive outputs (dates, numbers, currency, percentages, time zones).

3. **Routing, SEO, and runtime switching**

   * Whether locale is URL-based, header-based, or user preference in profile.

   * Where to place a **language switcher** and how to persist choice.

4. **DB & search implications**

   * Collations/encodings (utf8mb4) for MariaDB/Postgres; case/diacritic-insensitive search behavior; ORDER BY locale.

   * Any seeded reference data or enumerations shown to users that need translations.

## **Approach (decide \+ justify)**

* **Frontend i18n mode (pick one after scanning):**

  * **Runtime (recommended for dev UX):** `@ngx-translate/core` (JSON translation files, instant switching).

  * **Build-time (Angular i18n):** XLIFF extraction, per-locale builds.

  * If runtime chosen, show how to keep ICU pluralization and interpolation correct.

* **Backend i18n:**

  * `ResourceBundleMessageSource` (`messages.properties`, `messages_pt.properties` or `messages_pt_BR.properties`).

  * **AcceptHeaderLocaleResolver** (or equivalent) \+ propagation from UI to API.

  * Validation bundles: `ValidationMessages*.properties`.

  * Ensure logs remain English, but user-facing errors are localized.

## **Deliverables (produce all)**

1. **Architecture Overview (Markdown)** — one page: chosen strategy, data flow (locale selection → UI → API → persistence), fallback rules, and where keys live.

2. **Work Plan (Phased, Incremental)**

   * **Phase 1 — Enable framework plumbing:**

     * Frontend: add i18n library/config, register `pt` locale data, bootstrap translation loader, add language switcher.

     * Backend: configure `MessageSource`, `LocaleResolver`, `LocaleChangeInterceptor` (if used), wire validation bundles.

   * **Phase 2 — String externalization:**

     * Extract top-traffic UI surfaces; create `en.json` / `pt.json`; replace hard-coded strings with keys (ICU where needed).

     * Server errors/validation: replace literals with message codes & args.

   * **Phase 3 — Formatting & UX polish:**

     * Date/number/currency pipes; pluralization; accessibility announcements; right-to-left readiness (note: not required for pt).

   * **Phase 4 — Data & search nuances:**

     * Verify DB collation/charset; document search behavior with accents; propose tests.

   * **Phase 5 — Tests & CI:**

     * Unit and E2E tests for both locales; snapshot tolerances; coverage targets; CI matrix.

   * **Phase 6 — Docs & Rollout:**

     * README/runbook updates; translator handoff guide; feature flag & gradual rollout plan.

3. **Concrete Changes (unified diffs)**

   * **Frontend:**

     * `app.module.ts`/bootstrap: `registerLocaleData(pt)`; inject `LOCALE_ID` via user setting; install & wire `@ngx-translate/core`.

     * Example component/template diff: replace hard-coded text with `{{ 'key.path' | translate }}`; add ICU samples.

     * Add `src/assets/i18n/en.json` and `src/assets/i18n/pt.json` skeletons.

   * **Backend:**

     * `@Configuration` for `MessageSource` and `LocaleResolver` using `Accept-Language`; example controller/service using `MessageSource`.

     * Replace validation messages with `{code}` lookups; add `ValidationMessages_pt.properties`.

   * **CI:**

     * Job steps to verify both locales (frontend unit, backend tests), artifact checks for translation files.

4. **String Inventory & Owners**

   * Table (CSV/Markdown) of key paths → owners → status (extracted/translated/reviewed).

   * Naming convention (e.g., `feature.view.action.label`) and lint rule suggestions.

5. **Testing Strategy**

   * **Frontend:** unit tests asserting translated DOM, ICU plurals, error banners; E2E toggling locale & verifying persisted choice.

   * **Backend:** unit/integration tests asserting localized validation errors and controller messages based on `Accept-Language`.

   * **Non-functional:** performance impact of translation loading; memory footprint of bundles.

6. **Risk Register & Mitigations**

   * Out-of-sync keys, missing fallbacks, inconsistent date formats, plugin strings not externalized; propose automated checks.

## **Output format (return exactly in this order)**

1. **Executive Summary** (why chosen approach, effort estimate, risks)

2. **Phased Plan** (with goals, tasks, file paths, PR sizing, acceptance criteria)

3. **Concrete Diffs** (frontend, backend, CI snippets)

4. **String Inventory (Table)**

5. **Testing Plan** (unit/E2E examples)

6. **Rollout & Documentation Notes**

## **Examples (style/templates)**

**Angular — enable runtime translations & register locale**

\+ npm i @ngx-translate/core @ngx-translate/http-loader  
\--- a/tm/tm-front/projects/sqtm-app/src/app/app.module.ts  
\+++ b/tm/tm-front/projects/sqtm-app/src/app/app.module.ts  
\+ import { HttpClient } from '@angular/common/http';  
\+ import { TranslateLoader, TranslateModule } from '@ngx-translate/core';  
\+ import { TranslateHttpLoader } from '@ngx-translate/http-loader';  
\+ import { registerLocaleData } from '@angular/common';  
\+ import localePt from '@angular/common/locales/pt';  
\+ registerLocaleData(localePt);

\+ export function HttpLoaderFactory(http: HttpClient) {  
\+   return new TranslateHttpLoader(http, '/assets/i18n/', '.json');  
\+ }

  @NgModule({  
    ...  
\+   providers: \[{ provide: LOCALE\_ID, useFactory: localeFactory }\], // describe localeFactory  
\+   imports: \[  
\+     ...  
\+     TranslateModule.forRoot({ loader: { provide: TranslateLoader, useFactory: HttpLoaderFactory, deps: \[HttpClient\] }})  
\+   \]  
  })  
 export class AppModule {}

**Spring Boot — message source & locale from Accept-Language**

\--- a/tm.web/src/main/java/.../WebConfig.java  
\+++ b/tm.web/src/main/java/.../WebConfig.java  
\+ @Bean  
\+ public MessageSource messageSource() {  
\+   var src \= new ResourceBundleMessageSource();  
\+   src.setBasenames("messages", "ValidationMessages");  
\+   src.setDefaultEncoding("UTF-8");  
\+   src.setFallbackToSystemLocale(false);  
\+   return src;  
\+ }

\+ @Bean  
\+ public LocaleResolver localeResolver() {  
\+   var resolver \= new AcceptHeaderLocaleResolver();  
\+   resolver.setDefaultLocale(Locale.ENGLISH);  
\+   return resolver;  
\+ }

**Validation bundle**

src/main/resources/ValidationMessages.properties  
src/main/resources/ValidationMessages\_pt.properties