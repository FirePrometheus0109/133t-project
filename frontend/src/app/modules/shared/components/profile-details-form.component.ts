import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreState } from '../../core/states/core.state';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { InputLengths } from '../constants/validators/input-length';


@Component({
  selector: 'app-profile-details-form',
  template: `
    <mat-card>
      <mat-card-title>
        <ng-content select="title"></ng-content>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field>
            <mat-select placeholder="Position type" formControlName="position_type">
              <mat-option *ngFor="let position of positionTypes$ | async | keys" [value]="position.key">
                {{position.value}}
              </mat-option>
              -
            </mat-select>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.position_type"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <mat-select placeholder="Education" formControlName="education">
              <mat-option *ngFor="let education of educationTypes$ | async | keys" [value]="education.key">
                {{education.value}}
              </mat-option>
            </mat-select>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.education"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <mat-select placeholder="Years of experience" formControlName="experience">
              <mat-option *ngFor="let experience of experienceTypes$ | async | keys" [value]="experience.key">
                {{experience.value}}
              </mat-option>
            </mat-select>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.experience"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <mat-select placeholder="Travel opportunities"
                        formControlName="travel">
              <mat-option *ngFor="let travel of jsTravelOpportunities$ | async | keys" [value]="travel.key">
                {{travel.value}}
              </mat-option>
            </mat-select>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.travel"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input type="text" matInput placeholder="Salary min" formControlName="salary_min" maxlength="{{salaryInputLength}}">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.salary_min"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-slide-toggle color="warn" [checked]="f.salary_negotiable" formControlName="salary_negotiable">
            Make Salary Public
          </mat-slide-toggle>

          <mat-form-field>
            <input type="text" matInput placeholder="Salary max" formControlName="salary_max" maxlength="{{salaryInputLength}}">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.salary_max"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <mat-select placeholder="Clearance" formControlName="clearance">
              <mat-option *ngFor="let clearance of clearanceTypes$ | async | keys" [value]="clearance.key">
                {{clearance.value}}
              </mat-option>
            </mat-select>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.clearance"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <mat-select placeholder="Benefits" formControlName="benefits">
              <mat-option *ngFor="let benefit of benefits$ | async | keys" [value]="benefit.key">
                {{benefit.value}}
              </mat-option>
            </mat-select>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.benefits"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <ng-content select="body"></ng-content>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class ProfileDetailsComponent extends BaseFormComponent {
  @Select(CoreState.EducationTypes) educationTypes$: Observable<object[]>;
  @Select(CoreState.PositionTypes) positionTypes$: Observable<object[]>;
  @Select(CoreState.ExperienceTypes) experienceTypes$: Observable<object[]>;
  @Select(CoreState.TravelOpportunities) travelOpportunities$: Observable<object[]>;
  @Select(CoreState.JSTravelOpportunities) jsTravelOpportunities$: Observable<object[]>;
  @Select(CoreState.ClearanceTypes) clearanceTypes$: Observable<object[]>;
  @Select(CoreState.Benefits) benefits$: Observable<object[]>;

  public salaryInputLength = InputLengths.salary;
}
