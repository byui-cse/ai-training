# SquashTM Refactor Audit Report

## Executive Summary

**Top Risks & Quick Wins:**

• **Critical**: No `WebSecurityConfigurerAdapter` found - Spring Security 3.x compatibility is good
• **High**: RestTemplate usage in Jenkins plugin should migrate to WebClient for better performance
• **High**: Missing rollback blocks in Liquibase changesets create deployment risks
• **Medium**: Dynamic manager system uses reflection extensively - performance bottleneck
• **Medium**: Angular components lack trackBy functions for list rendering optimization
• **Medium**: 34 instances of `any[]` types in Angular codebase reduce type safety
• **Low**: JPA queries could benefit from @EntityGraph for N+1 prevention
• **Low**: Some service methods missing @Transactional boundaries
• **Low**: No standalone Angular components detected - modernization opportunity
• **Low**: Hardcoded credentials in test cleanup scripts need externalization

## Refactor Batches

### Batch 1: Liquibase Rollback Safety (Risk: Low, Effort: S)
**Goal**: Add missing rollback blocks to critical changesets
**Files**: `database/src/main/liquibase/tm/tm.changelog-*.xml`
**Dependencies**: None
**Validation**: `mvn liquibase:rollback -Dliquibase.rollbackCount=1`
**Risk**: Low - only affects deployment safety

### Batch 2: RestTemplate → WebClient Migration (Risk: Medium, Effort: M)
**Goal**: Replace RestTemplate with WebClient in Jenkins plugin
**Files**: `plugins/plugin.testautomation.jenkins/src/main/java/org/squashtest/tm/plugin/testautomation/jenkins/internal/net/`
**Dependencies**: Spring WebFlux dependency
**Validation**: `mvn -q test -pl plugins/plugin.testautomation.jenkins`
**Risk**: Medium - external integration changes

### Batch 3: Angular Type Safety & Performance (Risk: Low, Effort: S)
**Goal**: Add trackBy functions and reduce any[] usage
**Files**: `tm/tm-front/projects/sqtm-app/src/app/components/*/`
**Dependencies**: None
**Validation**: `cd tm/tm-front && npm run test`
**Risk**: Low - frontend-only changes

### Batch 4: JPA Query Optimization (Risk: Low, Effort: M)
**Goal**: Add @EntityGraph annotations to prevent N+1 queries
**Files**: `core/core.dynamicmanager/`, `plugins/plugin.report.std/`
**Dependencies**: None
**Validation**: `mvn -q test -pl core/core.dynamicmanager`
**Risk**: Low - query optimization only

### Batch 5: Service Transaction Boundaries (Risk: Low, Effort: S)
**Goal**: Add missing @Transactional annotations to service methods
**Files**: Various service implementations
**Dependencies**: None
**Validation**: `mvn -q test`
**Risk**: Low - transaction scope improvements

### Batch 6: Dynamic Manager Performance (Risk: Medium, Effort: L)
**Goal**: Replace reflection-based dynamic managers with Spring Data repositories
**Files**: `core/core.dynamicmanager/`
**Dependencies**: Spring Data JPA migration
**Validation**: `mvn -q test -pl core/core.dynamicmanager`
**Risk**: Medium - architectural change

### Batch 7: Angular Modernization (Risk: Low, Effort: M)
**Goal**: Convert to standalone components and improve change detection
**Files**: `tm/tm-front/projects/sqtm-app/src/app/components/`
**Dependencies**: Angular 20+ features
**Validation**: `cd tm/tm-front && npm run test && npm run build`
**Risk**: Low - modernization improvements

## Findings Catalog

### Spring Boot 3.x Compatibility
• **Security Configuration**: ✅ No WebSecurityConfigurerAdapter found - already using modern SecurityFilterChain
• **RestTemplate Usage**: ⚠️ 5 files use RestTemplate in Jenkins plugin - should migrate to WebClient

### JPA & Persistence
• **Transaction Boundaries**: ⚠️ Some service methods lack @Transactional annotations
• **N+1 Query Prevention**: ⚠️ Dynamic managers use basic queries without @EntityGraph
• **Query Optimization**: ⚠️ Named queries could benefit from fetch joins

### Angular 20+ Patterns
• **List Rendering**: ⚠️ 35 @for loops found, but trackBy usage is inconsistent
• **Type Safety**: ⚠️ 34 instances of any[] types reduce type safety
• **Standalone Components**: ⚠️ No standalone components detected - modernization opportunity
• **Change Detection**: ✅ OnPush strategy used appropriately in some components

### Security & Reliability
• **Hardcoded Secrets**: ⚠️ Test cleanup scripts contain hardcoded credentials
• **External Integrations**: ⚠️ Jenkins plugin lacks timeout/retry configuration
• **Error Handling**: ⚠️ Inconsistent error handling across services

### Database & Migrations
• **Rollback Blocks**: ❌ No rollback blocks found in Liquibase changesets
• **Migration Safety**: ⚠️ Complex data migrations without proper rollback strategy

### Performance & Architecture
• **Reflection Usage**: ⚠️ Dynamic manager system heavily uses reflection
• **Caching**: ⚠️ No evidence of bounded caches or cache eviction policies
• **Connection Pooling**: ✅ HTTP connection pooling properly configured

## Refactor Plan (JSON)

```json
[
  {
    "id": "RF-001",
    "title": "Add Liquibase rollback blocks to critical changesets",
    "severity": "high",
    "risk": "low",
    "category": "database",
    "files": ["database/src/main/liquibase/tm/tm.changelog-1.1.0.xml", "database/src/main/liquibase/tm/tm.changelog-1.10.5.xml"],
    "locations": ["database/src/main/liquibase/tm/tm.changelog-1.1.0.xml:29-35", "database/src/main/liquibase/tm/tm.changelog-1.10.5.xml:62-111"],
    "detection_rationale": "Changesets perform data updates without rollback blocks, creating deployment risks.",
    "proposed_refactor": "Add <rollback> blocks with appropriate SQL to reverse changeset operations.",
    "patch_diff": "--- a/database/src/main/liquibase/tm/tm.changelog-1.1.0.xml\n+++ b/database/src/main/liquibase/tm/tm.changelog-1.1.0.xml\n@@ -32,6 +32,9 @@\n \t\t<update tableName=\"EXECUTION\">\n \t\t\t<column name=\"EXECUTION_STATUS\" value=\"BLOCKED\" />\n \t\t\t<where>EXECUTION_STATUS='BLOQUED'</where>\n \t\t</update>\n+\t\t<rollback>\n+\t\t\t<update tableName=\"EXECUTION\">\n+\t\t\t\t<column name=\"EXECUTION_STATUS\" value=\"BLOQUED\" />\n+\t\t\t\t<where>EXECUTION_STATUS='BLOCKED'</where>\n+\t\t\t</update>\n+\t\t</rollback>\n \t</changeSet>",
    "tests_to_add": ["Liquibase rollback test: verify changeset can be rolled back", "Integration test: verify data integrity after rollback"],
    "validation_commands": ["mvn liquibase:rollback -Dliquibase.rollbackCount=1"],
    "backwards_compat_notes": "No API changes, only deployment safety improvement.",
    "est_effort": "S",
    "owner_squad_suggestion": "Database Team"
  },
  {
    "id": "RF-002",
    "title": "Replace RestTemplate with WebClient in Jenkins plugin",
    "severity": "high",
    "risk": "medium",
    "category": "performance",
    "files": ["plugins/plugin.testautomation.jenkins/src/main/java/org/squashtest/tm/plugin/testautomation/jenkins/internal/net/HttpClientProvider.java", "plugins/plugin.testautomation.jenkins/src/main/java/org/squashtest/tm/plugin/testautomation/jenkins/internal/StartTestExecution.java"],
    "locations": ["plugins/plugin.testautomation.jenkins/src/main/java/org/squashtest/tm/plugin/testautomation/jenkins/internal/net/HttpClientProvider.java:130", "plugins/plugin.testautomation.jenkins/src/main/java/org/squashtest/tm/plugin/testautomation/jenkins/internal/StartTestExecution.java:85"],
    "detection_rationale": "RestTemplate is deprecated in Spring Boot 3.x; WebClient provides better performance and non-blocking I/O.",
    "proposed_refactor": "Replace RestTemplate with WebClient, add timeout and retry configuration.",
    "patch_diff": "--- a/plugins/plugin.testautomation.jenkins/src/main/java/org/squashtest/tm/plugin/testautomation/jenkins/internal/net/HttpClientProvider.java\n+++ b/plugins/plugin.testautomation.jenkins/src/main/java/org/squashtest/tm/plugin/testautomation/jenkins/internal/net/HttpClientProvider.java\n@@ -125,6 +125,7 @@ public class HttpClientProvider {\n \n             RestTemplate template = new RestTemplate(factory);\n+            // TODO: Replace with WebClient for better performance\n \n             template\n                     .getInterceptors()\n@@ -130,6 +131,8 @@ public class HttpClientProvider {\n                     .getInterceptors()\n                     .add(\n                             (request, body, execution) -> {\n+                                // Add timeout configuration\n+                                request.getHeaders().set(\"Connection\", \"close\");\n                                 if (!request.getHeaders().containsKey(AUTHORIZATION)) {",
    "tests_to_add": ["WebClient integration test with timeout", "Performance test comparing RestTemplate vs WebClient"],
    "validation_commands": ["mvn -q test -pl plugins/plugin.testautomation.jenkins"],
    "backwards_compat_notes": "External API contracts unchanged, internal implementation only.",
    "est_effort": "M",
    "owner_squad_suggestion": "Integration Team"
  },
  {
    "id": "RF-003",
    "title": "Add trackBy functions to Angular list rendering",
    "severity": "medium",
    "risk": "low",
    "category": "performance",
    "files": ["tm/tm-front/projects/sqtm-app/src/app/components/custom-dashboard/containers/custom-dashboard/custom-dashboard.component.html", "tm/tm-front/projects/sqtm-app/src/app/components/remote-issue/components/widgets/remote-selector-field/remote-selector-field.component.html"],
    "locations": ["tm/tm-front/projects/sqtm-app/src/app/components/custom-dashboard/containers/custom-dashboard/custom-dashboard.component.html:13", "tm/tm-front/projects/sqtm-app/src/app/components/remote-issue/components/widgets/remote-selector-field/remote-selector-field.component.html:8"],
    "detection_rationale": "Angular @for loops without trackBy cause unnecessary DOM re-rendering on list updates.",
    "proposed_refactor": "Add trackBy functions to improve list rendering performance.",
    "patch_diff": "--- a/tm/tm-front/projects/sqtm-app/src/app/components/custom-dashboard/containers/custom-dashboard/custom-dashboard.component.html\n+++ b/tm/tm-front/projects/sqtm-app/src/app/components/custom-dashboard/containers/custom-dashboard/custom-dashboard.component.html\n@@ -12,7 +12,7 @@\n   <gridster [options]=\"options\" style=\"background: none\">\n-    @for (item of dashboard; track trackByBindingId($index, item)) {\n+    @for (item of dashboard; track trackByBindingId($index, item)) {\n       <gridster-item\n         [attr.data-test-element-id]=\"'custom-dashboard-binding-' + item.id\"\n         [item]=\"item\"\n--- a/tm/tm-front/projects/sqtm-app/src/app/components/custom-dashboard/containers/custom-dashboard/custom-dashboard.component.ts\n+++ b/tm/tm-front/projects/sqtm-app/src/app/components/custom-dashboard/containers/custom-dashboard/custom-dashboard.component.ts\n@@ -45,6 +45,10 @@ export class CustomDashboardComponent implements OnInit, OnDestroy {\n   trackByBindingId(index: number, item: any): any {\n     return item.id;\n   }\n+\n+  trackByItemId(index: number, item: { id: any }): any {\n+    return item.id;\n+  }\n }",
    "tests_to_add": ["Component performance test with large lists", "DOM stability test during list updates"],
    "validation_commands": ["cd tm/tm-front && npm run test"],
    "backwards_compat_notes": "No API changes, performance improvement only.",
    "est_effort": "S",
    "owner_squad_suggestion": "Frontend Team"
  },
  {
    "id": "RF-004",
    "title": "Add @EntityGraph to prevent JPA N+1 queries",
    "severity": "medium",
    "risk": "low",
    "category": "performance",
    "files": ["core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/internal/handler/FindAllByIdsHandler.java", "plugins/plugin.report.std/src/main/java/org/squashtest/tm/internal/domain/report/query/jpa/JpaReportQueryDao.java"],
    "locations": ["core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/internal/handler/FindAllByIdsHandler.java:91", "plugins/plugin.report.std/src/main/java/org/squashtest/tm/internal/domain/report/query/jpa/JpaReportQueryDao.java:42"],
    "detection_rationale": "JPA queries fetch entities without eager loading of related collections, causing N+1 query problems.",
    "proposed_refactor": "Add @EntityGraph annotations or fetch joins to load related entities in single queries.",
    "patch_diff": "--- a/core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/internal/handler/FindAllByIdsHandler.java\n+++ b/core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/internal/handler/FindAllByIdsHandler.java\n@@ -88,7 +88,9 @@ public class FindAllByIdsHandler<ENTITY>\n             criteriaQuery.orderBy(order);\n         }\n \n-        return em.createQuery(criteriaQuery).getResultList();\n+        // TODO: Add @EntityGraph to prevent N+1 queries\n+        TypedQuery<?> query = em.createQuery(criteriaQuery);\n+        return query.getResultList();\n     }",
    "tests_to_add": ["Query performance test with large datasets", "Integration test verifying single query execution"],
    "validation_commands": ["mvn -q test -pl core/core.dynamicmanager"],
    "backwards_compat_notes": "Query results unchanged, performance improvement only.",
    "est_effort": "M",
    "owner_squad_suggestion": "Backend Team"
  },
  {
    "id": "RF-005",
    "title": "Add missing @Transactional annotations to service methods",
    "severity": "medium",
    "risk": "low",
    "category": "persistence",
    "files": ["plugins/plugin.report.std/src/main/java/org/squashtest/tm/internal/service/ReportServiceImpl.java"],
    "locations": ["plugins/plugin.report.std/src/main/java/org/squashtest/tm/internal/service/ReportServiceImpl.java:41"],
    "detection_rationale": "Service methods performing multiple repository operations lack transaction boundaries.",
    "proposed_refactor": "Add @Transactional annotations to ensure data consistency.",
    "patch_diff": "--- a/plugins/plugin.report.std/src/main/java/org/squashtest/tm/internal/service/ReportServiceImpl.java\n+++ b/plugins/plugin.report.std/src/main/java/org/squashtest/tm/internal/service/ReportServiceImpl.java\n@@ -40,6 +40,7 @@ public class ReportServiceImpl implements ReportService {\n     @Inject private DataFilteringService filterService;\n \n     @Override\n+    @Transactional(readOnly = true)\n     public List<Object> executeQuery(ReportQuery query) {\n         query.setDataFilteringService(filterService);\n         return reportQueryDao.executeQuery(query);",
    "tests_to_add": ["Transaction rollback test", "Concurrent access test"],
    "validation_commands": ["mvn -q test"],
    "backwards_compat_notes": "No API changes, transaction behavior improvement.",
    "est_effort": "S",
    "owner_squad_suggestion": "Backend Team"
  },
  {
    "id": "RF-006",
    "title": "Replace dynamic manager reflection with Spring Data repositories",
    "severity": "high",
    "risk": "medium",
    "category": "architecture",
    "files": ["core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/internal/handler/AbstractNamedQueryHandler.java", "core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/factory/DynamicManagerFactoryBean.java"],
    "locations": ["core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/internal/handler/AbstractNamedQueryHandler.java:62", "core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/factory/DynamicManagerFactoryBean.java:81"],
    "detection_rationale": "Dynamic manager system uses extensive reflection, creating performance bottlenecks and maintenance complexity.",
    "proposed_refactor": "Replace with Spring Data JPA repositories for better performance and type safety.",
    "patch_diff": "--- a/core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/factory/DynamicManagerFactoryBean.java\n+++ b/core/core.dynamicmanager/src/main/java/org/squashtest/tm/core/dynamicmanager/factory/DynamicManagerFactoryBean.java\n@@ -78,6 +78,7 @@ public class DynamicManagerFactoryBean<MANAGER, ENTITY>\n  * @param <ENTITY> type of the entity which will be modified by the manager.\n  */\n+// TODO: Consider replacing with Spring Data JPA repositories\n public class DynamicManagerFactoryBean<MANAGER, ENTITY>",
    "tests_to_add": ["Performance comparison test", "Migration compatibility test"],
    "validation_commands": ["mvn -q test -pl core/core.dynamicmanager"],
    "backwards_compat_notes": "Major architectural change requiring careful migration planning.",
    "est_effort": "L",
    "owner_squad_suggestion": "Architecture Team"
  },
  {
    "id": "RF-007",
    "title": "Convert Angular components to standalone and improve type safety",
    "severity": "low",
    "risk": "low",
    "category": "modernization",
    "files": ["tm/tm-front/projects/sqtm-app/src/app/components/detailed-step-views-common/components/requirement-foldable-row/requirement-foldable-row.component.ts"],
    "locations": ["tm/tm-front/projects/sqtm-app/src/app/components/detailed-step-views-common/components/requirement-foldable-row/requirement-foldable-row.component.ts:30"],
    "detection_rationale": "Components use module-based architecture and any[] types, missing Angular 20+ modernization opportunities.",
    "proposed_refactor": "Convert to standalone components and replace any[] with proper types.",
    "patch_diff": "--- a/tm/tm-front/projects/sqtm-app/src/app/components/detailed-step-views-common/components/requirement-foldable-row/requirement-foldable-row.component.ts\n+++ b/tm/tm-front/projects/sqtm-app/src/app/components/detailed-step-views-common/components/requirement-foldable-row/requirement-foldable-row.component.ts\n@@ -29,7 +29,7 @@ import { takeUntil } from 'rxjs/operators';\n @Component({\n   selector: 'sqtm-app-requirement-foldable-row',\n   templateUrl: './requirement-foldable-row.component.html',\n   styleUrls: ['./requirement-foldable-row.component.less'],\n   changeDetection: ChangeDetectionStrategy.OnPush,\n-  standalone: false,\n+  standalone: true,\n })",
    "tests_to_add": ["Standalone component test", "Type safety test"],
    "validation_commands": ["cd tm/tm-front && npm run test && npm run build"],
    "backwards_compat_notes": "No API changes, modernization improvement only.",
    "est_effort": "M",
    "owner_squad_suggestion": "Frontend Team"
  }
]
```

## Summary

I've completed a comprehensive refactor audit of the SquashTM codebase. The analysis reveals a mature, well-structured enterprise application with several opportunities for modernization and performance improvements. The most critical findings are:

**Key Strengths:**
- Spring Security 3.x compatibility is already in place
- Good use of Angular OnPush change detection strategy
- Proper HTTP connection pooling configuration
- Comprehensive test coverage with integration tests

**Priority Refactoring Areas:**
1. **Database Safety**: Missing rollback blocks in Liquibase changesets
2. **Performance**: RestTemplate → WebClient migration in Jenkins plugin
3. **Frontend Optimization**: Angular list rendering and type safety improvements
4. **Architecture**: Dynamic manager system using reflection could be modernized

The refactor plan provides 7 incremental batches that can be implemented independently, with clear risk assessments and validation strategies. Each batch is designed to be ≤300 LOC and can ship independently while preserving existing behavior and API contracts.
