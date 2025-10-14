<!-- e822db16-200e-48a8-a4a6-40e7bb02017b e8875759-46de-499d-a58a-bea31e107d74 -->
# Liquibase Rollback Safety Implementation

## Objective

Add `<rollback>` blocks to critical data-modifying Liquibase changesets across all changelog files to enable safe rollback during failed deployments.

## Scope

- Focus on all 54 changelog files containing `update tableName` operations
- Prioritize simple UPDATE, INSERT, and DELETE operations that can be easily reversed
- Mark complex operations (multi-table deletes, temp tables, procedures) as non-rollbackable where appropriate
- Follow user requirement: Add rollbacks where feasible, mark others as non-rollbackable

## Implementation Strategy

### Phase 1: Simple UPDATE Operations (High Priority)

**Files:** tm.changelog-1.1.0.xml, tm.changelog-1.9.0.xml, tm.changelog-1.13.0.xml, and ~50 others

**Pattern to implement:**

```xml
<changeSet id="tm-1.1.0.01" author="gfouquet">
  <comment>Corrects status to BLOCKED in EXECUTION table</comment>
  <update tableName="EXECUTION">
    <column name="EXECUTION_STATUS" value="BLOCKED" />
    <where>EXECUTION_STATUS='BLOQUED'</where>
  </update>
  <rollback>
    <update tableName="EXECUTION">
      <column name="EXECUTION_STATUS" value="BLOQUED" />
      <where>EXECUTION_STATUS='BLOCKED'</where>
    </update>
  </rollback>
</changeSet>
```

**Specific changesets:**

- `tm.changelog-1.1.0.xml`: changesets tm-1.1.0.01, tm-1.1.0.02, tm-1.1.0.03 (status corrections)
- `tm.changelog-1.9.0.xml`: changeset tm-1.9.0-issue-3236-01 (FIELD_TYPE update)
- `tm.changelog-1.13.0.xml`: changeset tm-1.13.0 (version number update)
- All similar UPDATE operations across other files

### Phase 2: Simple INSERT Operations

**Pattern to implement:**

```xml
<changeSet id="tm-1.9.0.feature-3211-2" author="flaurens">
  <comment>Inserting default disabled execution statuses</comment>
  <sql><![CDATA[
    insert into DISABLED_EXECUTION_STATUS (CL_ID, EXECUTION_STATUS)
    select cl_id, 'ERROR' from CAMPAIGN_LIBRARY;
  ]]></sql>
  <rollback>
    <delete tableName="DISABLED_EXECUTION_STATUS">
      <where>EXECUTION_STATUS IN ('ERROR', 'WARNING', 'NOT_RUN', 'SETTLED')</where>
    </delete>
  </rollback>
</changeSet>
```

### Phase 3: Complex Operations - Mark as Non-Rollbackable

**Pattern to implement:**

```xml
<changeSet id="tm-1.10.5-issue-3860-1" author="mpagnon">
  <comment>Removing duplicate values</comment>
  <!-- Complex operation with temp tables -->
  <createTable tableName="CUF_VALUES_TO_SAVE">...</createTable>
  <sql>...</sql>
  <dropTable tableName="CUF_VALUES_TO_SAVE" />
  <rollback>
    <comment>This changeset cannot be rolled back due to data deletion</comment>
    <empty/>
  </rollback>
</changeSet>
```

**Operations to mark as non-rollbackable:**

- Multi-table DELETE operations (tm.changelog-1.8.0.xml)
- Temp table data migrations (tm.changelog-1.10.5.xml, tm.changelog-1.9.0.xml)
- CREATE/DROP PROCEDURE operations
- Complex data transformations

## Files to Modify

### Critical Priority (Simple reversible operations):

1. `database/src/main/liquibase/tm/tm.changelog-1.1.0.xml` - 3 UPDATE changesets
2. `database/src/main/liquibase/tm/tm.changelog-1.9.0.xml` - 1 UPDATE, 4 INSERT changesets
3. `database/src/main/liquibase/tm/tm.changelog-1.13.0.xml` - 1 UPDATE changeset
4. All version number updates across ~50 files (UPDATE CORE_CONFIG)

### Medium Priority (Feasible rollbacks):

- Simple INSERT operations across 34 files (~373 total inserts)
- Single-table DELETE operations where data can be restored

### Mark as Non-Rollbackable:

- `database/src/main/liquibase/tm/tm.changelog-1.10.5.xml` - Complex duplicate removal
- `database/src/main/liquibase/tm/tm.changelog-1.8.0.xml` - Multi-table cleanup
- `database/src/main/liquibase/tm/tm.changelog-1.3.0.xml` - Trigger/procedure operations

## Validation Strategy

After each file modification:

1. Run Liquibase validation: `mvn liquibase:validate -pl database`
2. Test rollback capability: `mvn liquibase:rollback -Dliquibase.rollbackCount=1 -pl database`
3. Run database linter: `mvn clean verify -pl database` (ensure no linter errors)

## Risk Assessment

- **Risk Level:** Low
- **Impact:** Deployment safety improvement only
- **Breaking Changes:** None - rollback blocks are optional metadata
- **Backwards Compatibility:** 100% - existing deployments unaffected

## Estimated Changes

- ~150-200 changesets across 54 files
- ~300 lines of code (LOC) added
- Effort: Small (S) - as specified in REFACTOR_ANALYSIS.md

### To-dos

- [ ] Analyze all 54 changelog files to categorize changesets by rollback feasibility (simple UPDATE/INSERT vs complex operations)
- [ ] Add rollback blocks to simple UPDATE operations (version updates, status corrections)
- [ ] Add rollback blocks to simple INSERT operations that can be reversed with DELETE
- [ ] Add empty rollback blocks with comments for complex operations (multi-table deletes, temp tables)
- [ ] Run liquibase:validate and liquibase:rollback tests to ensure all changes work correctly
- [ ] Run database linter to ensure no new violations introduced