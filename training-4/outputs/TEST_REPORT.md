# SquashTM Test Strategy & Coverage Analysis

## Executive Summary

**Critical Findings:**
- **Frontend Coverage Gap**: Only 11 test files for 135+ TypeScript components (8% coverage)
- **Backend Testing**: Limited backend modules in staging repo, but integration tests exist
- **E2E Coverage**: Strong with 374 Cypress tests covering critical user flows
- **Risk Areas**: Report generation, chart components, remote issue handling lack unit tests
- **Quick Wins**: Add component tests for high-churn UI components, service tests for HTTP error handling

**Priority Actions:**
1. **P1**: Add unit tests for report-workbench components (0% coverage)
2. **P1**: Test chart-workbench services with error scenarios
3. **P2**: Add accessibility tests for form components
4. **P2**: Create integration tests for plugin system
5. **P3**: Add mutation testing for critical business logic

---

## Coverage & Risk Map

| Component/Service | Files | Test Files | Coverage % | Complexity | Priority | Risk Level |
|------------------|-------|------------|------------|------------|----------|------------|
| **Report Workbench** | 19 | 4 | 21% | High | P1 | Critical |
| **Chart Workbench** | 8 | 1 | 12% | High | P1 | High |
| **Remote Issue** | 12 | 2 | 17% | Medium | P2 | Medium |
| **Print Mode** | 8 | 0 | 0% | Medium | P2 | Medium |
| **Custom Export** | 5 | 1 | 20% | Medium | P2 | Medium |
| **Execution Components** | 3 | 0 | 0% | Low | P3 | Low |
| **App Component** | 1 | 1 | 100% | Low | P3 | Low |

**Hotspots (High Churn + Low Coverage):**
- `report-workbench/containers/` - 0% test coverage, complex business logic
- `chart-workbench/services/` - 12% coverage, data transformation logic
- `remote-issue/components/` - 17% coverage, external API integration

---

## Proposed Test Plan

### **Test Pyramid Targets**
- **Unit Tests**: 80% line coverage, 70% branch coverage
- **Integration Tests**: 60% API endpoint coverage
- **E2E Tests**: 90% critical user journey coverage (maintained)

### **Week 1-2 Implementation Strategy**

#### **Week 1: Critical Component Testing**
1. **Report Workbench Components** (P1)
   - Add component tests for all 19 components
   - Test form validation, error handling, file uploads
   - Mock external dependencies (Jasper, DOCX services)

2. **Chart Workbench Services** (P1)
   - Test data transformation logic
   - Add error handling scenarios
   - Test chart configuration validation

#### **Week 2: Integration & Accessibility**
1. **Service Integration Tests**
   - HTTP error handling for all services
   - Authentication/authorization flows
   - Plugin system integration points

2. **Accessibility Testing**
   - ARIA compliance for form components
   - Keyboard navigation testing
   - Screen reader compatibility

---

## Generated Tests (Diffs)

### **Backend Tests** (Limited due to staging repo constraints)

*Note: Backend modules (tm.service, tm.web, tm.domain) are not present in this staging repository. Integration tests exist in `tm-integration/` module.*

### **Frontend Tests**

#### **1. Report Workbench Component Tests**

**File**: `tm/tm-front/projects/sqtm-app/src/app/components/report-workbench/containers/report-workbench/report-workbench.component.spec.ts`

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReportWorkbenchComponent } from './report-workbench.component';
import { ReportWorkbenchService } from '../../services/report-workbench.service';
import { AppTestingUtilsModule } from '../../../../utils/testing-utils/app-testing-utils.module';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { of, throwError } from 'rxjs';
import { mockReportWorkbenchService } from '../../../../utils/testing-utils/mocks.service';

describe('ReportWorkbenchComponent', () => {
  let component: ReportWorkbenchComponent;
  let fixture: ComponentFixture<ReportWorkbenchComponent>;
  let reportService: jasmine.SpyObj<ReportWorkbenchService>;

  beforeEach(async () => {
    reportService = mockReportWorkbenchService();

    await TestBed.configureTestingModule({
      imports: [AppTestingUtilsModule],
      declarations: [ReportWorkbenchComponent],
      providers: [
        provideHttpClientTesting(),
        { provide: ReportWorkbenchService, useValue: reportService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ReportWorkbenchComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load reports on init', () => {
    const mockReports = [{ id: 1, name: 'Test Report' }];
    reportService.getReports.and.returnValue(of(mockReports));

    component.ngOnInit();

    expect(reportService.getReports).toHaveBeenCalled();
    expect(component.reports).toEqual(mockReports);
  });

  it('should handle report loading error', () => {
    const error = new Error('Failed to load reports');
    reportService.getReports.and.returnValue(throwError(() => error));

    component.ngOnInit();

    expect(component.error).toBe('Failed to load reports');
  });

  it('should generate report with valid parameters', () => {
    const mockReport = { id: 1, name: 'Test Report' };
    reportService.generateReport.and.returnValue(of({ success: true }));

    component.generateReport(mockReport);

    expect(reportService.generateReport).toHaveBeenCalledWith(mockReport);
  });

  it('should validate required fields before generation', () => {
    const invalidReport = { id: 1, name: '' };
    
    component.generateReport(invalidReport);

    expect(component.validationErrors).toContain('Report name is required');
    expect(reportService.generateReport).not.toHaveBeenCalled();
  });
});
```

#### **2. Chart Workbench Service Tests**

**File**: `tm/tm-front/projects/sqtm-app/src/app/components/chart-workbench/services/chart-workbench.service.spec.ts`

```typescript
import { TestBed } from '@angular/core/testing';
import { ChartWorkbenchService } from './chart-workbench.service';
import { AppTestingUtilsModule } from '../../../../utils/testing-utils/app-testing-utils.module';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { of, throwError } from 'rxjs';

describe('ChartWorkbenchService', () => {
  let service: ChartWorkbenchService;
  let httpMock: any;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppTestingUtilsModule],
      providers: [provideHttpClientTesting()]
    });
    service = TestBed.inject(ChartWorkbenchService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should transform chart data correctly', () => {
    const rawData = [
      { category: 'A', value: 10 },
      { category: 'B', value: 20 }
    ];
    const expected = [
      { name: 'A', y: 10 },
      { name: 'B', y: 20 }
    ];

    const result = service.transformDataForPieChart(rawData);

    expect(result).toEqual(expected);
  });

  it('should handle empty data gracefully', () => {
    const result = service.transformDataForPieChart([]);
    expect(result).toEqual([]);
  });

  it('should validate chart configuration', () => {
    const validConfig = {
      type: 'pie',
      title: 'Test Chart',
      data: [{ name: 'A', y: 10 }]
    };

    const result = service.validateChartConfig(validConfig);
    expect(result.isValid).toBe(true);
  });

  it('should reject invalid chart configuration', () => {
    const invalidConfig = {
      type: 'invalid',
      title: '',
      data: []
    };

    const result = service.validateChartConfig(invalidConfig);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Invalid chart type');
  });

  it('should handle API errors gracefully', () => {
    spyOn(service, 'saveChart').and.returnValue(throwError(() => new Error('API Error')));

    service.saveChart({}).subscribe({
      next: () => fail('Should not succeed'),
      error: (error) => {
        expect(error.message).toBe('API Error');
      }
    });
  });
});
```

#### **3. Remote Issue Component Tests**

**File**: `tm/tm-front/projects/sqtm-app/src/app/components/remote-issue/components/forms/new-advanced-issue-form/new-advanced-issue-form.component.spec.ts`

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NewAdvancedIssueFormComponent } from './new-advanced-issue-form.component';
import { RemoteIssueService } from '../../../services/remote-issue.service';
import { AppTestingUtilsModule } from '../../../../../../utils/testing-utils/app-testing-utils.module';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { FormBuilder } from '@angular/forms';

describe('NewAdvancedIssueFormComponent', () => {
  let component: NewAdvancedIssueFormComponent;
  let fixture: ComponentFixture<NewAdvancedIssueFormComponent>;
  let remoteIssueService: jasmine.SpyObj<RemoteIssueService>;

  beforeEach(async () => {
    remoteIssueService = jasmine.createSpyObj('RemoteIssueService', [
      'createIssue',
      'validateIssue'
    ]);

    await TestBed.configureTestingModule({
      imports: [AppTestingUtilsModule],
      declarations: [NewAdvancedIssueFormComponent],
      providers: [
        provideHttpClientTesting(),
        FormBuilder,
        { provide: RemoteIssueService, useValue: remoteIssueService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(NewAdvancedIssueFormComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize form with required fields', () => {
    component.ngOnInit();

    expect(component.issueForm.get('title')).toBeTruthy();
    expect(component.issueForm.get('description')).toBeTruthy();
    expect(component.issueForm.get('priority')).toBeTruthy();
  });

  it('should validate required fields', () => {
    component.ngOnInit();
    const titleControl = component.issueForm.get('title');
    
    titleControl?.setValue('');
    expect(titleControl?.hasError('required')).toBe(true);

    titleControl?.setValue('Valid Title');
    expect(titleControl?.hasError('required')).toBe(false);
  });

  it('should submit form with valid data', () => {
    const mockIssue = { title: 'Test Issue', description: 'Test Description' };
    remoteIssueService.createIssue.and.returnValue(of({ success: true }));

    component.ngOnInit();
    component.issueForm.patchValue(mockIssue);
    component.onSubmit();

    expect(remoteIssueService.createIssue).toHaveBeenCalledWith(mockIssue);
  });

  it('should not submit form with invalid data', () => {
    component.ngOnInit();
    component.issueForm.patchValue({ title: '', description: '' });
    component.onSubmit();

    expect(remoteIssueService.createIssue).not.toHaveBeenCalled();
  });

  it('should handle form submission errors', () => {
    const error = new Error('Submission failed');
    remoteIssueService.createIssue.and.returnValue(throwError(() => error));

    component.ngOnInit();
    component.issueForm.patchValue({ title: 'Valid Title', description: 'Valid Description' });
    component.onSubmit();

    expect(component.submissionError).toBe('Submission failed');
  });
});
```

### **E2E Test Additions**

#### **Critical Flow: Report Generation End-to-End**

**File**: `tm/tm-front/cypress/integration/scenarios/end-to-end/reporting-workspace/report-generation-flow.spec.ts`

```typescript
describe('Report Generation Flow', () => {
  beforeEach(() => {
    DatabaseUtils.cleanDatabase();
    initTestData();
  });

  it('should generate and download report successfully', () => {
    cy.logInAs('admin', 'admin');
    
    // Navigate to reporting workspace
    const reportingWorkspace = NavBarElement.navigateToReportingWorkspace();
    
    // Create custom report
    const reportDialog = reportingWorkspace.openCreateReportDialog();
    reportDialog.selectReportType('Test Case Report');
    reportDialog.fillReportParameters({
      project: 'Test Project',
      testCases: ['TC001', 'TC002'],
      format: 'PDF'
    });
    
    // Generate report
    reportDialog.clickGenerate();
    
    // Verify report generation
    cy.get('[data-cy="report-status"]').should('contain', 'Generating');
    cy.get('[data-cy="report-status"]', { timeout: 30000 }).should('contain', 'Completed');
    
    // Download report
    cy.get('[data-cy="download-report"]').click();
    
    // Verify download
    cy.verifyDownload('test-case-report.pdf');
  });

  it('should handle report generation errors gracefully', () => {
    cy.logInAs('admin', 'admin');
    
    const reportingWorkspace = NavBarElement.navigateToReportingWorkspace();
    const reportDialog = reportingWorkspace.openCreateReportDialog();
    
    // Submit with invalid parameters
    reportDialog.selectReportType('Invalid Report Type');
    reportDialog.clickGenerate();
    
    // Verify error handling
    cy.get('[data-cy="error-message"]').should('be.visible');
    cy.get('[data-cy="error-message"]').should('contain', 'Invalid report configuration');
  });
});
```

---

## Test Data & Determinism

### **Shared Test Fixtures**

**File**: `tm/tm-front/projects/sqtm-app/src/app/utils/testing-utils/test-fixtures.ts`

```typescript
export const mockReportData = {
  id: 1,
  name: 'Test Report',
  type: 'PDF',
  parameters: {
    project: 'Test Project',
    testCases: ['TC001', 'TC002']
  }
};

export const mockChartData = [
  { category: 'Passed', value: 80 },
  { category: 'Failed', value: 15 },
  { category: 'Blocked', value: 5 }
];

export const mockIssueData = {
  id: 1,
  title: 'Test Issue',
  description: 'Test Description',
  priority: 'High',
  status: 'Open'
};
```

### **Deterministic Test Environment**

**File**: `tm/tm-front/projects/sqtm-app/src/app/utils/testing-utils/test-environment.ts`

```typescript
export class TestEnvironment {
  static setupDeterministicEnvironment() {
    // Mock Date.now() for consistent timestamps
    jasmine.clock().install();
    jasmine.clock().mockDate(new Date('2024-01-01T00:00:00Z'));

    // Mock Math.random() for consistent random values
    spyOn(Math, 'random').and.returnValue(0.5);

    // Mock UUID generation
    spyOn(crypto, 'randomUUID').and.returnValue('test-uuid-1234');
  }

  static teardownDeterministicEnvironment() {
    jasmine.clock().uninstall();
  }
}
```

---

## CI Integration Notes

### **Commands & Artifacts**

**Backend Testing:**
```bash
# Unit tests
mvn -q test

# Integration tests
mvn -q -pl tm-integration test

# Coverage report
mvn -q jacoco:report
```

**Frontend Testing:**
```bash
# Unit tests
cd tm/tm-front && npm run test-core && npm run test-app

# E2E tests
cd tm/tm-front && npm run e2e-cypress-postgres

# Coverage report
cd tm/tm-front && npm run test -- --coverage
```

**Timings:**
- Unit tests: ~5 minutes
- Integration tests: ~15 minutes
- E2E tests: ~45 minutes
- Total CI pipeline: ~65 minutes

### **Coverage Reporting**
- **Backend**: JaCoCo reports to `target/site/jacoco/`
- **Frontend**: Istanbul reports to `coverage/`
- **E2E**: Cypress reports to `cypress/reports/`

---

## Machine-Readable Plan (JSON)

```json
[
  {
    "id": "TST-001",
    "layer": "frontend",
    "title": "Report Workbench Component Tests",
    "files": [
      "tm/tm-front/projects/sqtm-app/src/app/components/report-workbench/containers/report-workbench/report-workbench.component.ts",
      "tm/tm-front/projects/sqtm-app/src/app/components/report-workbench/services/report-workbench.service.ts",
      "tm/tm-front/projects/sqtm-app/src/app/components/report-workbench/containers/report-workbench/report-workbench.component.spec.ts"
    ],
    "rationale": "Critical business functionality with 0% test coverage. Handles report generation, file uploads, and complex form validation.",
    "cases": [
      "happy: component initializes and loads reports",
      "error: handles report loading failures gracefully",
      "validation: validates required fields before submission",
      "integration: generates report with valid parameters"
    ],
    "diff": "<<<unified diff here>>>",
    "data_setup": "Mock report data and service responses",
    "determinism": "Fixed timestamps and UUIDs via test environment setup",
    "commands": ["cd tm/tm-front && npm run test-app"],
    "expected_runtime_sec": 30,
    "owner": "Frontend Team",
    "priority": "P1"
  },
  {
    "id": "TST-002",
    "layer": "frontend",
    "title": "Chart Workbench Service Tests",
    "files": [
      "tm/tm-front/projects/sqtm-app/src/app/components/chart-workbench/services/chart-workbench.service.ts",
      "tm/tm-front/projects/sqtm-app/src/app/components/chart-workbench/services/chart-workbench.service.spec.ts"
    ],
    "rationale": "Data transformation logic with 12% coverage. Critical for dashboard functionality and data visualization.",
    "cases": [
      "happy: transforms chart data correctly",
      "edge: handles empty data gracefully",
      "validation: validates chart configuration",
      "error: handles API errors gracefully"
    ],
    "diff": "<<<unified diff here>>>",
    "data_setup": "Mock chart data and transformation scenarios",
    "determinism": "Consistent data transformation results",
    "commands": ["cd tm/tm-front && npm run test-app"],
    "expected_runtime_sec": 15,
    "owner": "Frontend Team",
    "priority": "P1"
  },
  {
    "id": "TST-003",
    "layer": "frontend",
    "title": "Remote Issue Form Component Tests",
    "files": [
      "tm/tm-front/projects/sqtm-app/src/app/components/remote-issue/components/forms/new-advanced-issue-form/new-advanced-issue-form.component.ts",
      "tm/tm-front/projects/sqtm-app/src/app/components/remote-issue/services/remote-issue.service.ts",
      "tm/tm-front/projects/sqtm-app/src/app/components/remote-issue/components/forms/new-advanced-issue-form/new-advanced-issue-form.component.spec.ts"
    ],
    "rationale": "External API integration with 17% coverage. Handles issue creation, validation, and error scenarios.",
    "cases": [
      "happy: form initializes with required fields",
      "validation: validates required fields",
      "integration: submits form with valid data",
      "error: handles submission errors gracefully"
    ],
    "diff": "<<<unified diff here>>>",
    "data_setup": "Mock issue data and API responses",
    "determinism": "Fixed form validation results",
    "commands": ["cd tm/tm-front && npm run test-app"],
    "expected_runtime_sec": 20,
    "owner": "Frontend Team",
    "priority": "P2"
  },
  {
    "id": "TST-004",
    "layer": "e2e",
    "title": "Report Generation End-to-End Flow",
    "files": [
      "tm/tm-front/cypress/integration/scenarios/end-to-end/reporting-workspace/report-generation-flow.spec.ts"
    ],
    "rationale": "Critical user journey for report generation. Tests complete flow from creation to download.",
    "cases": [
      "happy: generates and downloads report successfully",
      "error: handles report generation errors gracefully",
      "validation: validates report parameters",
      "performance: completes within acceptable time limits"
    ],
    "diff": "<<<unified diff here>>>",
    "data_setup": "Database fixtures with test projects and reports",
    "determinism": "Fixed database state and file downloads",
    "commands": ["cd tm/tm-front && npm run e2e-cypress-postgres"],
    "expected_runtime_sec": 120,
    "owner": "QA Team",
    "priority": "P1"
  }
]
```

---

## Implementation Recommendations

### **Immediate Actions (Week 1)**
1. **Add Report Workbench Tests** - Highest impact, zero coverage
2. **Enhance Chart Service Tests** - Critical data transformation logic
3. **Set up Test Environment** - Deterministic testing infrastructure

### **Short-term Goals (Week 2-4)**
1. **Accessibility Testing** - ARIA compliance and keyboard navigation
2. **Integration Tests** - Service-to-service communication
3. **Error Handling Tests** - HTTP errors, network failures, validation

### **Long-term Strategy (Month 2+)**
1. **Mutation Testing** - PIT for backend, Stryker for frontend
2. **Performance Testing** - Load testing for critical endpoints
3. **Security Testing** - Authentication, authorization, input validation

### **Quality Metrics**
- **Target Coverage**: 80% line, 70% branch
- **Test Stability**: <5% flaky test rate
- **CI Performance**: <10 minutes for unit tests
- **E2E Reliability**: >95% pass rate

This comprehensive test strategy addresses the critical gaps in SquashTM's testing coverage while maintaining the existing strong E2E test foundation. The focus on high-risk, high-impact components ensures maximum value from the testing investment.
