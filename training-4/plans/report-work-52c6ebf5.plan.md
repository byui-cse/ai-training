<!-- 52c6ebf5-d933-4333-877d-f7a2ae23ed93 d407df4a-8248-46fd-a970-76306d90a620 -->
# P1: Add Unit Tests for Report-Workbench Components

## Overview

Implement unit tests for the main report-workbench component (0% coverage currently). This requires first creating the missing test infrastructure referenced in TEST_REPORT.md, then writing comprehensive tests for ReportWorkbenchComponent.

## Implementation Steps

### Phase 1: Create Test Infrastructure (Foundation)

**1. Create AppTestingUtilsModule**

- File: `tm/tm-front/projects/sqtm-app/src/app/utils/testing-utils/app-testing-utils.module.ts`
- Purpose: Centralized testing module that provides common testing utilities
- Exports: Common Angular testing modules (CommonModule, FormsModule, ReactiveFormsModule, TranslateModule)

**2. Create Mock Services**

- File: `tm/tm-front/projects/sqtm-app/src/app/utils/testing-utils/mocks.service.ts`
- Mock functions needed:
  - `mockReferentialDataService()`: Returns jasmine spy with projectDatas$, milestoneModeData$, filteredProjects$, isUltimateLicenseAvailable$
  - `mockRestService()`: Returns jasmine spy with get, post, put, delete methods
  - `mockReportWorkbenchService()`: Returns jasmine spy with state$, initializeInitialData, changeSelectedReport, toggleSelectReportPanel
  - `mockReportDefinitionService()`: Returns jasmine spy with saveNewReportDefinition, updateReportDefinition, getReportDefinitionViewModelByReportDefinitionId
  - `mockDialogService()`: Returns jasmine spy with openDialog, openAlert

**3. Create Mock Data**

- File: `tm/tm-front/projects/sqtm-app/src/app/utils/testing-utils/mocks.data.ts`
- Mock data factories:
  - `mockProjectData()`: Returns ProjectData with customFieldBinding, permissions
  - `mockReportData()`: Returns Report with id, name, inputs, views
  - `mockReportDefinitionModel()`: Returns ReportDefinitionModel with id, name, parameters, pluginNamespace
  - `mockMilestoneModeData()`: Returns MilestoneModeData

### Phase 2: Write ReportWorkbenchComponent Tests

**4. Create ReportWorkbenchComponent Test Spec**

- File: `tm/tm-front/projects/sqtm-app/src/app/components/report-workbench/containers/report-workbench/report-workbench.component.spec.ts`
- Test suites:
  - **Component Creation**: Verify component initializes correctly
  - **Report Loading**: Test report list initialization and filtering
  - **Form Initialization**: Test form group setup for new and existing reports
  - **Criteria Management**: Test dynamic form controls for report inputs
  - **Validation**: Test client-side and server-side validation
  - **Report Saving**: Test save/update operations with success and error scenarios
  - **Report Download**: Test download flow for different report types (Jasper, DOCX, Direct)
  - **Error Handling**: Test HTTP error handling and user feedback

### Test Coverage Goals

- **Line Coverage**: Target 80%+ for ReportWorkbenchComponent
- **Branch Coverage**: Target 70%+ for conditional logic
- **Key Scenarios**:
  - Happy path: Create new report, edit existing report, download report
  - Error paths: Validation failures, HTTP errors, missing data
  - Edge cases: Empty inputs, milestone mode enabled/disabled, composite inputs

## Files to Create

1. `tm/tm-front/projects/sqtm-app/src/app/utils/testing-utils/app-testing-utils.module.ts`
2. `tm/tm-front/projects/sqtm-app/src/app/utils/testing-utils/mocks.service.ts`
3. `tm/tm-front/projects/sqtm-app/src/app/utils/testing-utils/mocks.data.ts`
4. `tm/tm-front/projects/sqtm-app/src/app/components/report-workbench/containers/report-workbench/report-workbench.component.spec.ts`

## Key Dependencies from Existing Code

- Existing patterns from `composite-report-input.component.spec.ts` (shows usage of AppTestingUtilsModule)
- Existing patterns from `chart-workbench.service.spec.ts` (shows mock service creation)
- Component under test: `report-workbench.component.ts` (852 lines, complex form management)
- Services: ReportWorkbenchService, DocxReportService, JasperReportService, DirectDownloadableReportService

## Test Execution

```bash
cd tm/tm-front
npm run test-app
```

Expected runtime: ~30 seconds for the new test suite

### To-dos

- [ ] Create test infrastructure files (AppTestingUtilsModule, mocks.service.ts, mocks.data.ts)
- [ ] Write comprehensive unit tests for ReportWorkbenchComponent
- [ ] Run tests and verify coverage meets targets (80% line, 70% branch)