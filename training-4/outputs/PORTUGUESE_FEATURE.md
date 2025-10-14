# Portuguese Translation Feature Implementation Plan

## 1. Executive Summary

**Chosen Approach:** Runtime internationalization using `@ngx-translate/core` for the Angular frontend and Spring Boot's `MessageSource` for the backend, targeting **pt-BR** (Brazilian Portuguese) as the primary locale with fallback support for pt-PT.

**Effort Estimate:** 6-8 weeks for complete implementation across all phases.

**Key Risks:**
- **Out-of-sync translation keys** between frontend and backend
- **Missing fallbacks** causing broken UI elements
- **Performance impact** from loading translation bundles
- **Database collation issues** with Portuguese characters
- **Plugin compatibility** with new i18n system

**Mitigation Strategy:** Incremental rollout with feature flags, comprehensive testing, and automated validation.

## 2. Current i18n Status Analysis

### Frontend (Angular 20+)
- ✅ **Already configured:** `@ngx-translate/core` v16 installed and configured
- ✅ **Locale detection:** `getSupportedBrowserLang()` function from sqtm-core
- ✅ **Translation infrastructure:** `TranslateService` injected in components
- ❌ **Missing:** Portuguese locale data registration
- ❌ **Missing:** Translation files (currently `ngxTranslateFiles: []`)
- ❌ **Missing:** Language switcher UI component

### Backend (Spring Boot 3.5.4)
- ❌ **No i18n configuration:** No `MessageSource` or `LocaleResolver` found
- ❌ **No message bundles:** No `messages.properties` files
- ❌ **No validation messages:** No `ValidationMessages.properties`
- ✅ **UTF-8 support:** Database uses UTF-8 encoding

### Database
- ✅ **UTF-8 encoding:** Supports Portuguese characters
- ✅ **Full-text search:** Configured for MariaDB/PostgreSQL
- ⚠️ **Collation:** May need Portuguese-specific collation for proper sorting

## 3. Phased Implementation Plan

### Phase 1 — Enable Framework Plumbing (Week 1-2)
**Goals:** Set up basic i18n infrastructure without breaking existing functionality

**Frontend Tasks:**
- Register Portuguese locale data (`registerLocaleData(localePt)`)
- Configure translation file loading in `SqtmCoreModule`
- Create language switcher component
- Add Portuguese translation file structure

**Backend Tasks:**
- Configure `MessageSource` and `LocaleResolver`
- Set up `Accept-Language` header handling
- Create message bundle structure

**Files to Modify:**
- `tm/tm-front/projects/sqtm-app/src/app/app.module.ts`
- `tm/tm-front/projects/sqtm-app/src/app/app.component.ts`
- `tm/tm-front/projects/sqtm-app/src/assets/i18n/` (new directory)
- Backend configuration classes (new)

**Acceptance Criteria:**
- Language switcher appears in UI
- Portuguese locale data loads without errors
- Backend accepts `Accept-Language: pt-BR` headers
- No existing functionality breaks

### Phase 2 — String Externalization (Week 2-3)
**Goals:** Extract and externalize user-visible strings

**Frontend Tasks:**
- Extract hard-coded strings from top-traffic components
- Create `en.json` and `pt.json` translation files
- Replace string literals with translation keys
- Implement ICU message format for pluralization

**Backend Tasks:**
- Replace hard-coded error messages with message codes
- Create validation message bundles
- Update exception handlers to use localized messages

**Priority Components:**
- Login/authentication pages
- Main navigation and menus
- Error messages and notifications
- Form labels and buttons

**Acceptance Criteria:**
- 80% of user-facing strings externalized
- Translation keys follow naming convention
- ICU messages work correctly
- Error messages are localized

### Phase 3 — Formatting & UX Polish (Week 3-4)
**Goals:** Implement proper date, number, and currency formatting

**Tasks:**
- Configure date/number/currency pipes for Portuguese locale
- Implement pluralization rules
- Add accessibility announcements
- Test right-to-left readiness (not required for Portuguese)

**Files to Modify:**
- Date formatting services
- Number formatting utilities
- Chart and report components

**Acceptance Criteria:**
- Dates display in Portuguese format (dd/MM/yyyy)
- Numbers use Portuguese decimal separator (comma)
- Currency displays in Brazilian Real (R$)
- Pluralization works correctly

### Phase 4 — Data & Search Nuances (Week 4-5)
**Goals:** Ensure database and search work correctly with Portuguese

**Tasks:**
- Verify database collation supports Portuguese characters
- Test search functionality with accented characters
- Update full-text search indexes if needed
- Document search behavior with diacritics

**Database Changes:**
- Add Portuguese collation if needed
- Update search indexes for better Portuguese support
- Test case-insensitive search with accents

**Acceptance Criteria:**
- Search works with accented characters (ã, ç, é, etc.)
- Sorting respects Portuguese alphabetical order
- Database queries handle UTF-8 correctly

### Phase 5 — Tests & CI (Week 5-6)
**Goals:** Comprehensive testing for both locales

**Frontend Tests:**
- Unit tests for translation service
- Component tests with different locales
- E2E tests for language switching
- Snapshot tests for translated components

**Backend Tests:**
- Integration tests for localized messages
- API tests with different `Accept-Language` headers
- Validation message tests

**CI Pipeline:**
- Build matrix for both locales
- Translation file validation
- Missing key detection

**Acceptance Criteria:**
- 90% test coverage for i18n functionality
- CI passes for both English and Portuguese
- Automated detection of missing translations

### Phase 6 — Docs & Rollout (Week 6-8)
**Goals:** Documentation and gradual rollout

**Tasks:**
- Update README with i18n information
- Create translator handoff guide
- Implement feature flag for gradual rollout
- Performance monitoring setup

**Documentation:**
- Developer guide for adding new translations
- Translator workflow documentation
- Troubleshooting guide

**Rollout Strategy:**
- Feature flag to enable Portuguese for specific users
- Gradual rollout to 10%, 50%, 100% of users
- Monitoring for performance and error rates

**Acceptance Criteria:**
- Complete documentation available
- Feature flag controls Portuguese availability
- Rollout can be reverted if issues occur

## 4. Concrete Implementation Changes

### Frontend Changes

**1. App Module Configuration**
```typescript
// tm/tm-front/projects/sqtm-app/src/app/app.module.ts
import { registerLocaleData } from '@angular/common';
import localePt from '@angular/common/locales/pt';
import { LOCALE_ID } from '@angular/core';

registerLocaleData(localePt);

@NgModule({
  imports: [
    SqtmCoreModule.forRoot({
      pluginIdentifier: SQTM_MAIN_APP_IDENTIFIER,
      ngxTranslateFiles: ['./assets/i18n/translations_'],
    }),
    // ... other imports
  ],
  providers: [
    {
      provide: LOCALE_ID,
      useFactory: () => {
        const stored = localStorage.getItem('sqtm-locale');
        return stored || 'en';
      }
    },
    // ... other providers
  ],
})
export class AppModule {}
```

**2. Language Switcher Component**
```typescript
// tm/tm-front/projects/sqtm-app/src/app/components/language-switcher/language-switcher.component.ts
@Component({
  selector: 'sqtm-app-language-switcher',
  template: `
    <nz-select 
      [ngModel]="currentLang" 
      (ngModelChange)="changeLanguage($event)"
      nzPlaceHolder="Language">
      <nz-option nzValue="en" nzLabel="English"></nz-option>
      <nz-option nzValue="pt" nzLabel="Português"></nz-option>
    </nz-select>
  `
})
export class LanguageSwitcherComponent {
  currentLang = 'en';

  constructor(private translate: TranslateService) {
    this.currentLang = this.translate.currentLang || 'en';
  }

  changeLanguage(lang: string) {
    this.translate.use(lang);
    localStorage.setItem('sqtm-locale', lang);
    window.location.reload(); // Simple approach for now
  }
}
```

**3. Translation Files Structure**
```json
// tm/tm-front/projects/sqtm-app/src/assets/i18n/translations_en.json
{
  "sqtm-app": {
    "common": {
      "save": "Save",
      "cancel": "Cancel",
      "delete": "Delete",
      "edit": "Edit"
    },
    "navigation": {
      "dashboard": "Dashboard",
      "test-cases": "Test Cases",
      "requirements": "Requirements"
    }
  }
}
```

```json
// tm/tm-front/projects/sqtm-app/src/assets/i18n/translations_pt.json
{
  "sqtm-app": {
    "common": {
      "save": "Salvar",
      "cancel": "Cancelar", 
      "delete": "Excluir",
      "edit": "Editar"
    },
    "navigation": {
      "dashboard": "Painel",
      "test-cases": "Casos de Teste",
      "requirements": "Requisitos"
    }
  }
}
```

### Backend Changes

**1. Message Source Configuration**
```java
// tm/tm.web/src/main/java/org/squashtest/tm/web/config/WebConfig.java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Bean
    public MessageSource messageSource() {
        ResourceBundleMessageSource messageSource = new ResourceBundleMessageSource();
        messageSource.setBasenames("messages", "ValidationMessages");
        messageSource.setDefaultEncoding("UTF-8");
        messageSource.setFallbackToSystemLocale(false);
        messageSource.setCacheSeconds(3600);
        return messageSource;
    }

    @Bean
    public LocaleResolver localeResolver() {
        AcceptHeaderLocaleResolver resolver = new AcceptHeaderLocaleResolver();
        resolver.setDefaultLocale(Locale.ENGLISH);
        resolver.setSupportedLocales(Arrays.asList(Locale.ENGLISH, new Locale("pt", "BR")));
        return resolver;
    }

    @Bean
    public LocaleChangeInterceptor localeChangeInterceptor() {
        LocaleChangeInterceptor interceptor = new LocaleChangeInterceptor();
        interceptor.setParamName("lang");
        return interceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(localeChangeInterceptor());
    }
}
```

**2. Message Bundles**
```properties
# tm/tm.web/src/main/resources/messages.properties
error.validation.required=This field is required
error.validation.invalid.email=Invalid email address
success.save=Data saved successfully
```

```properties
# tm/tm.web/src/main/resources/messages_pt_BR.properties
error.validation.required=Este campo é obrigatório
error.validation.invalid.email=Endereço de email inválido
success.save=Dados salvos com sucesso
```

**3. Controller Example**
```java
@RestController
@RequestMapping("/backend/api")
public class TestCaseController {

    @Autowired
    private MessageSource messageSource;

    @PostMapping("/test-cases")
    public ResponseEntity<?> createTestCase(@Valid @RequestBody TestCaseDto dto, 
                                          Locale locale) {
        try {
            // Business logic
            return ResponseEntity.ok(messageSource.getMessage(
                "success.save", null, locale));
        } catch (ValidationException e) {
            return ResponseEntity.badRequest().body(messageSource.getMessage(
                "error.validation.required", null, locale));
        }
    }
}
```

## 5. String Inventory & Ownership

| Key Path | Owner | Status | Priority |
|----------|-------|--------|----------|
| `sqtm-app.common.buttons` | Frontend Team | Pending | High |
| `sqtm-app.navigation.menu` | Frontend Team | Pending | High |
| `sqtm-app.forms.validation` | Frontend Team | Pending | High |
| `sqtm-app.errors.generic` | Frontend Team | Pending | High |
| `backend.api.validation` | Backend Team | Pending | High |
| `backend.api.errors` | Backend Team | Pending | High |
| `backend.reports.templates` | Backend Team | Pending | Medium |
| `plugins.jenkins.messages` | Plugin Team | Pending | Low |

**Naming Convention:** `{module}.{feature}.{element}` (e.g., `sqtm-app.test-cases.list.title`)

## 6. Testing Strategy

### Frontend Testing
```typescript
// Unit test example
describe('LanguageSwitcherComponent', () => {
  it('should switch language and persist choice', () => {
    const component = new LanguageSwitcherComponent(mockTranslateService);
    component.changeLanguage('pt');
    expect(mockTranslateService.use).toHaveBeenCalledWith('pt');
    expect(localStorage.getItem('sqtm-locale')).toBe('pt');
  });
});

// E2E test example
describe('Language Switching', () => {
  it('should display Portuguese text after switching', () => {
    cy.visit('/');
    cy.get('[data-test="language-switcher"]').select('pt');
    cy.get('[data-test="save-button"]').should('contain', 'Salvar');
  });
});
```

### Backend Testing
```java
@Test
public void testLocalizedValidationMessage() {
    // Given
    Locale ptLocale = new Locale("pt", "BR");
    
    // When
    String message = messageSource.getMessage(
        "error.validation.required", null, ptLocale);
    
    // Then
    assertEquals("Este campo é obrigatório", message);
}
```

### Performance Testing
- Measure bundle size impact (target: <50KB per language)
- Test translation loading time (target: <100ms)
- Monitor memory usage with multiple locales

## 7. Rollout & Documentation Notes

### Feature Flag Implementation
```typescript
// Environment configuration
export const environment = {
  sqtmExperimentalFeatureFlags: {
    'portuguese-translation': {
      enabled: true,
      rolloutPercentage: 10 // Start with 10% of users
    }
  }
};
```

### Monitoring & Metrics
- Translation key coverage percentage
- Missing translation errors
- Language switcher usage statistics
- Performance impact metrics

### Rollback Plan
- Feature flag can disable Portuguese instantly
- Database changes are backward compatible
- Translation files can be removed without breaking functionality

### Translator Workflow
1. **Extraction:** Automated extraction of new translation keys
2. **Translation:** Professional translator works with JSON files
3. **Review:** Native speaker reviews translations
4. **Testing:** QA tests with Portuguese locale
5. **Deployment:** Gradual rollout with monitoring

## 8. Database Considerations

### Current Database Setup
- **Encoding:** UTF-8 (supports Portuguese characters)
- **Full-text search:** Configured for MariaDB/PostgreSQL
- **Collation:** May need Portuguese-specific collation

### Required Changes
```sql
-- For MariaDB/PostgreSQL - Add Portuguese collation if needed
ALTER DATABASE squashtm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Update full-text search indexes for better Portuguese support
-- (Already configured in existing changelogs)
```

### Search Behavior
- **Case-insensitive:** Search should work with/without accents
- **Diacritic handling:** "café" should match "cafe"
- **Sorting:** Respect Portuguese alphabetical order

## 9. Plugin Compatibility

### Existing Plugin System
- Plugins use `ngxTranslateFiles` configuration
- Translation files located at `./assets/i18n/translations_`
- Plugin development documentation available

### Required Updates
- Update plugin development guide with Portuguese examples
- Ensure plugin translation keys don't conflict
- Test plugin compatibility with new locale system

## 10. Performance Considerations

### Bundle Size Impact
- **Target:** <50KB additional per language
- **Strategy:** Lazy load translation files
- **Monitoring:** Track bundle size in CI

### Runtime Performance
- **Translation loading:** <100ms target
- **Memory usage:** Monitor with multiple locales
- **Caching:** Implement translation caching strategy

### Optimization Strategies
- Split translation files by feature
- Implement lazy loading for non-critical translations
- Use tree-shaking to remove unused translations

This comprehensive plan provides a safe, incremental approach to adding Portuguese language support to SquashTM while maintaining system stability and performance.
