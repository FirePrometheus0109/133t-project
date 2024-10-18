import { ChangeDetectorRef, Component, Input, OnInit, ViewChild } from '@angular/core';
import { Store } from '@ngxs/store';
import { environment } from '../../../../environments/environment';
import { CoreActions } from '../../core/actions';
import { CoreState } from '../../core/states/core.state';
import { SkillItem } from '../models/skill.model';
import { ValidationService } from '../services/validation.service';
import { BaseFormComponent } from './base-form.component';
import { SearchFieldComponent } from './search-field/search-field.component';


@Component({
  selector: 'app-skills-select-component',
  template: `
    <mat-card>
      <mat-card-title>
        <ng-content select="title"></ng-content>
      </mat-card-title>
      <mat-card-content>
        <div class="skills-container">
          <div class="skills-search-section">
            <div class="skill-search-form-class">
              <app-search-field [autocompleteProp]="auto"
                                [isMatAutocompleteDisabled]="false"
                                [placeholder]="'Search'"
                                [isDisabled]="isSkillsReachedMaxCount"
                                [initialValue]="defaultSearchText"
                                (focused)="filterAlreadySelected()"
                                (searchChanged)="loadSkills($event)">
              </app-search-field>
              <app-control-messages [form]="form"
                                    [control]="searchFieldComponent.formCtrl"
                                    [submitted]="isSubmitted"
                                    [errors]="errors">
              </app-control-messages>
              <mat-autocomplete #auto="matAutocomplete"
                                (optionSelected)="addSkill($event.option.value)"
                                [disableRipple]="true">
                <mat-option *ngIf="noResults" value="false" disabled>No results</mat-option>
                <mat-option *ngFor="let filteredSkill of allFilteredSkills" [value]="filteredSkill">
                  {{filteredSkill.name}}
                </mat-option>
              </mat-autocomplete>
            </div>
          </div>

          <div class="skills-selected-section">
            <form [formGroup]="form" (ngSubmit)="submit()">
              <div class="selected-skills-list">
                <mat-chip-list #chipList>
                  <mat-chip *ngFor="let selectedSkill of form.value[skillPropertyName]"
                            [selectable]="!pending"
                            [removable]="!pending"
                            (removed)="removeSkill(selectedSkill)"
                            [attr.disabled]="pending">
                    {{selectedSkill.name}}
                    <mat-icon matChipRemove>cancel</mat-icon>
                  </mat-chip>
                </mat-chip-list>
              </div>

              <div class="skills-actions">
                <ng-content select="body"></ng-content>
              </div>
            </form>
          </div>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .skill-search-form-class {
      width: 400px;
    }

    .skills-container {
      display: flex;
      flex-direction: column;
    }

    .skills-search-section {
      margin-bottom: 15px;
    }

    .selected-skills-list {
      margin-bottom: 30px;
    }
  `],
})
export class SkillsSelectComponent extends BaseFormComponent implements OnInit {
  @Input() skillPropertyName = 'skills';
  @Input() excludedSkills: Array<any> = [];

  @ViewChild(SearchFieldComponent) searchFieldComponent: SearchFieldComponent;

  private searchResultsLimit = 100;
  private selectedSkills: SkillItem[] = [];
  public allFilteredSkills: SkillItem[] = [];
  public defaultSearchText = '';

  constructor(
    private changeDetectorRef: ChangeDetectorRef,
    public store: Store
  ) {
    super();
  }

  ngOnInit() {
    this.handleSetInitialData.subscribe((initialData) => {
      if (initialData && initialData[this.skillPropertyName]) {
        this.selectedSkills = initialData[this.skillPropertyName].slice();
      }
      this.loadSkills(this.defaultSearchText);
    });
    this.searchFieldComponent.formCtrl.setValidators(ValidationService.selectListObjectValidator);
    super.ngOnInit();
  }

  get isSkillsReachedMaxCount(): boolean {
    return this.selectedSkills.length >= environment.maxSkillsCount;
  }

  get noResults(): boolean {
    return !this.allFilteredSkills.length;
  }

  addSkill(skill: SkillItem): void {
    const isNewSkill = !this.selectedSkills.some(item => item.id === skill.id);
    if (isNewSkill) {
      this.selectedSkills = [
        ...this.selectedSkills,
        skill,
      ];
      this.updateOriginalControl();
    }
    this.searchFieldComponent.formCtrl.setValue('');
    this.searchFieldComponent.formCtrl.markAsUntouched();
  }

  removeSkill(skill: SkillItem): void {
    this.selectedSkills = this.selectedSkills.filter(item => item.id !== skill.id);
    this.updateOriginalControl();
  }

  filterAlreadySelected() {
    this.allFilteredSkills = this.getFilteredSkills(this.store.selectSnapshot(CoreState.skillsFiltered));
  }

  loadSkills(value: string) {
    const offset = 0;
    const orderField = 'name';
    this.store.dispatch(
      new CoreActions.LoadSkillsPart(value, offset, this.searchResultsLimit, orderField)
    ).subscribe(() => {
      this.filterAlreadySelected();
      this.changeDetectorRef.markForCheck();
    });
  }

  private updateOriginalControl(): void {
    this.handleFormPatch.emit({ [this.skillPropertyName]: this.selectedSkills });
  }

  private getFilteredSkills(results: SkillItem[]): SkillItem[] {
    const excludedSkills = [
      ...this.form.value[this.skillPropertyName],
      ...this.excludedSkills,
    ];
    return results.filter(skill => {
      return !excludedSkills.some(excludedSkill => excludedSkill.id === skill.id);
    });
  }
}
