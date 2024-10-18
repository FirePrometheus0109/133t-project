import { Component, EventEmitter, Output } from '@angular/core';
import { MatCheckboxChange } from '@angular/material';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { environment } from '../../../../../environments/environment';
import { CoreState } from '../../../core/states/core.state';
import { BaseFormComponent } from '../../../shared/components/base-form.component';


@Component({
  selector: 'app-jsp-education-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>New education</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field>
            <input matInput placeholder="Institution" formControlName="institution">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.institution"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <mat-select placeholder="Degree" formControlName="degree">
              <mat-option *ngFor="let education of jobSeekerEducationModelEnumDict$ | async | keys" [value]="education.key">
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
            <input matInput placeholder="Field of study" formControlName="field_of_study">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.field_of_study"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input matInput [matDatepicker]="pickerFrom" placeholder="From" formControlName="date_from"
                   [min]="dateMin" [max]="dateMax">
            <mat-datepicker-toggle matSuffix [for]="pickerFrom"></mat-datepicker-toggle>
            <mat-datepicker #pickerFrom></mat-datepicker>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.date_from"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input matInput [matDatepicker]="pickerTo" placeholder="To" formControlName="date_to"
                   [disabled]="f.is_current.value" [min]="dateMin" [max]="dateMax">
            <mat-datepicker-toggle matSuffix [for]="pickerTo"></mat-datepicker-toggle>
            <mat-datepicker #pickerTo></mat-datepicker>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.date_to"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-checkbox formControlName="is_current" [value]="false"
                        (change)="changeIsCurrent($event)">Currently studying
          </mat-checkbox>
          <app-control-messages [form]="form"
                                [control]="f.is_current"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input matInput placeholder="Location" formControlName="location">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.location"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <textarea matInput placeholder="Description" formControlName="description">
            </textarea>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.description"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-action-row>
            <button type="reset" mat-raised-button color="primary" (click)="closeForm.emit()">
              Cancel
              <mat-icon matSuffix>cancel</mat-icon>
            </button>
            <button type="submit" mat-raised-button color="primary">
              Save
              <mat-icon matSuffix>save</mat-icon>
            </button>
          </mat-action-row>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class JspEducationComponent extends BaseFormComponent {
  @Select(CoreState.JobSeekerEducationModelEnumDict) jobSeekerEducationModelEnumDict$: Observable<object[]>;

  @Output() closeForm = new EventEmitter<any>();

  dateMin = environment.dateChoiceMin;
  dateMax = new Date();

  changeIsCurrent(event: MatCheckboxChange) {
    if (event.checked) {
      this.form.controls.date_to.setValue(null);
    }
  }
}
