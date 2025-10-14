<!-- 4b4b6cf3-dddd-4b85-9fca-fcf6e1a8df02 2578fcf9-e142-4cbe-8d1f-be867230d8f7 -->
# Phase 1: Enable Framework Plumbing - Detailed Implementation Plan

## Overview

This plan breaks Phase 1 into 5 small, independently verifiable milestones. Each milestone can be tested and validated before moving to the next, ensuring no existing functionality breaks.

## Milestone 1: Frontend - Register Portuguese Locale Data

**Goal:** Add Portuguese locale data to Angular's locale system

**Changes Required:**

- Modify `tm/tm-front/projects/sqtm-app/src/app/app.module.ts`:
  - Import `registerLocaleData` from `@angular/common`
  - Import `localePt` from `@angular/common/locales/pt`
  - Call `registerLocaleData(localePt)` before `@NgModule` decorator

**Verification:**

- Application builds without errors
- Application loads in browser without console errors
- Existing functionality (login, navigation) works as before
- No visual changes to the UI

**Testing Command:**

```bash
cd tm/tm-front
yarn build
```

---

## Milestone 2: Frontend - Create Translation File Structure

**Goal:** Set up the translation file directory and create initial empty translation files

**Changes Required:**

- Create directory: `tm/tm-front/projects/sqtm-app/src/assets/`
- Create subdirectory: `tm/tm-front/projects/sqtm-app/src/assets/i18n/`
- Create file: `tm/tm-front/projects/sqtm-app/src/assets/i18n/translations_en.json` with minimal structure:
```json
{
  "sqtm-app": {
    "common": {
      "test": "Test"
    }
  }
}
```

- Create file: `tm/tm-front/projects/sqtm-app/src/assets/i18n/translations_pt.json` with minimal structure:
```json
{
  "sqtm-app": {
    "common": {
      "test": "Teste"
    }
  }
}
```


**Verification:**

- Files are created successfully
- Files contain valid JSON
- Directory structure matches expected path
- Build succeeds

---

## Milestone 3: Frontend - Configure Translation Loading

**Goal:** Connect translation files to the Angular application via `SqtmCoreModule`

**Changes Required:**

- Modify `tm/tm-front/projects/sqtm-app/src/app/app.module.ts`:
  - Update `SqtmCoreModule.forRoot()` configuration:
    - Change `ngxTranslateFiles: []` to `ngxTranslateFiles: ['./assets/i18n/translations_']`

**Verification:**

- Application builds without errors
- Application loads without console errors
- Translation files are requested by browser (check Network tab)
- No 404 errors for translation files
- Existing functionality works unchanged

**Testing in Browser:**

- Open DevTools Network tab
- Look for requests to `translations_en.json` and `translations_pt.json`
- Verify files load with HTTP 200 status

---

## Milestone 4: Frontend - Add LOCALE_ID Provider

**Goal:** Set up dynamic locale selection based on user preference

**Changes Required:**

- Modify `tm/tm-front/projects/sqtm-app/src/app/app.module.ts`:
  - Import `LOCALE_ID` from `@angular/core`
  - Add to `providers` array:
```typescript
{
  provide: LOCALE_ID,
  useFactory: () => {
    const stored = localStorage.getItem('sqtm-locale');
    return stored || 'en';
  }
}
```


**Verification:**

- Application builds and runs
- Default locale is 'en'
- No console errors
- Date/number formatting still works (currently defaults to English)
- Can manually test by:
  - Opening DevTools Console
  - Running: `localStorage.setItem('sqtm-locale', 'pt')`
  - Refreshing page
  - Verifying Portuguese locale is active (check browser console for TranslateService current language)

---

## Milestone 5: Frontend - Create Language Switcher Component

**Goal:** Build a visible UI component to switch between languages

**Changes Required:**

1. Create component directory: `tm/tm-front/projects/sqtm-app/src/app/components/language-switcher/`

2. Create file: `language-switcher.component.ts`
```typescript
import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'sqtm-app-language-switcher',
  template: `
    <nz-select 
      [ngModel]="currentLang" 
      (ngModelChange)="changeLanguage($event)"
      nzPlaceHolder="Language"
      style="width: 150px;">
      <nz-option nzValue="en" nzLabel="English"></nz-option>
      <nz-option nzValue="pt" nzLabel="Português"></nz-option>
    </nz-select>
  `,
  standalone: false
})
export class LanguageSwitcherComponent {
  currentLang = 'en';

  constructor(private translate: TranslateService) {
    this.currentLang = this.translate.currentLang || 'en';
  }

  changeLanguage(lang: string) {
    this.translate.use(lang);
    localStorage.setItem('sqtm-locale', lang);
    window.location.reload();
  }
}
```

3. Create module file: `language-switcher.module.ts`
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { LanguageSwitcherComponent } from './language-switcher.component';

@NgModule({
  declarations: [LanguageSwitcherComponent],
  imports: [CommonModule, FormsModule, NzSelectModule],
  exports: [LanguageSwitcherComponent]
})
export class LanguageSwitcherModule {}
```

4. Modify `tm/tm-front/projects/sqtm-app/src/app/app.component.ts`:

   - Add language switcher to template (temporary placement for testing):
```typescript
template: `
  <sqtm-core-generic-error-display></sqtm-core-generic-error-display>
  <div style="position: fixed; top: 10px; right: 10px; z-index: 9999;">
    <sqtm-app-language-switcher></sqtm-app-language-switcher>
  </div>
  <div class="full-height full-width" sqtmCoreDragAndDropDisableSelection>
    <router-outlet></router-outlet>
    <sqtm-core-svg-icon-definition></sqtm-core-svg-icon-definition>
  </div>
`
```


5. Import `LanguageSwitcherModule` in `app.module.ts` imports array

**Verification:**

- Language switcher appears in top-right corner
- Dropdown shows "English" and "Português" options
- Selecting a language:
  - Saves preference to localStorage
  - Reloads the page
  - Loads the selected language on reload
- Check browser console for no errors
- Test switching back and forth between languages

**Manual Testing Steps:**

1. Open application
2. Click language switcher
3. Select "Português"
4. Verify page reloads
5. Open DevTools Console
6. Run: `localStorage.getItem('sqtm-locale')` - should return `"pt"`
7. Check Network tab for `translations_pt.json` request
8. Switch back to English and verify same behavior

---

## Important Notes

- **No Backend Changes Yet:** This phase focuses on frontend infrastructure only. Backend integration comes in later milestones.
- **No Breaking Changes:** All changes are additive. Existing functionality must continue to work.
- **Feature Flag Ready:** The implementation is compatible with the feature flag system already in place (`environment.sqtmExperimentalFeatureFlags`).
- **Translation Keys:** We're only creating minimal test translations. Actual string externalization happens in Phase 2.

## Success Criteria for Phase 1 Completion

- [ ] Portuguese locale registered in Angular
- [ ] Translation file structure created
- [ ] Translation files loading successfully
- [ ] Locale can be dynamically switched
- [ ] Language switcher component functional
- [ ] No console errors or warnings
- [ ] All existing tests pass
- [ ] Application builds successfully
- [ ] No regression in existing features

### To-dos

- [ ] Register Portuguese locale data in app.module.ts
- [ ] Create translation file structure with initial en/pt JSON files
- [ ] Configure SqtmCoreModule to load translation files
- [ ] Add LOCALE_ID provider for dynamic locale selection
- [ ] Create and integrate language switcher component