import { Component } from '@angular/core';
import { InputLengths } from '../constants/validators/input-length';
import { ProfileDetailsComponent } from './profile-details-form.component';


@Component({
  selector: 'app-profile-details-ext-form',
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <mat-grid-list cols="2" rowHeight="2:1">
        <mat-grid-tile>
          <mat-list role="list">
            <mat-list-item role="listitem">
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
            </mat-list-item>
            <mat-list-item role="listitem">
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
              <mat-checkbox formControlName="education_strict">Strict</mat-checkbox>
              <app-control-messages [form]="form"
                                    [control]="f.education_strict"
                                    [submitted]="isSubmitted"
                                    [errors]="errors">
              </app-control-messages>
            </mat-list-item>
            <mat-list-item role="listitem">
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
            </mat-list-item>
            <mat-list-item role="listitem">
              <mat-form-field>
                <mat-select placeholder="Travel opportunities" formControlName="travel">
                  <mat-option *ngFor="let travel of travelOpportunities$ | async | keys" [value]="travel.key">
                    {{travel.value}}
                  </mat-option>
                </mat-select>
              </mat-form-field>
              <app-control-messages [form]="form"
                                    [control]="f.travel"
                                    [submitted]="isSubmitted"
                                    [errors]="errors">
              </app-control-messages>
            </mat-list-item>
          </mat-list>
        </mat-grid-tile>

        <mat-grid-tile>
          <mat-list role="list">
            <mat-list-item role="listitem">
              <mat-checkbox formControlName="salary_negotiable">Negotiable</mat-checkbox>
              <app-control-messages [form]="form"
                                    [control]="f.salary_negotiable"
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

              <mat-form-field>
                <input type="text" matInput placeholder="Salary max" formControlName="salary_max" maxlength="{{salaryInputLength}}">
              </mat-form-field>
              <app-control-messages [form]="form"
                                    [control]="f.salary_max"
                                    [submitted]="isSubmitted"
                                    [errors]="errors">
              </app-control-messages>
            </mat-list-item>
            <mat-list-item role="listitem">
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
            </mat-list-item>
            <mat-list-item role="listitem">
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
            </mat-list-item>
          </mat-list>
        </mat-grid-tile>
      </mat-grid-list>
      <ng-content select="body"></ng-content>
    </form>
  `,
  styles: [],
})
export class ProfileDetailsExtComponent extends ProfileDetailsComponent {
  public salaryInputLength = InputLengths.salary;
}
