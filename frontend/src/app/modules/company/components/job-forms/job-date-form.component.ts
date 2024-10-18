import { Component } from '@angular/core';
import { BaseFormComponent } from '../../../shared/components/base-form.component';


@Component({
  selector: 'app-job-date-form',
  template: `
    <mat-card>
      <mat-card-content>
        <form [formGroup]="form">
          <mat-form-field *ngxPermissionsOnly="['create_delayed_job']">
            <input matInput
                   [matTooltip]="tooltipText"
                   [matDatepicker]="pickerPublishDate"
                   placeholder="Publish date"
                   formControlName="publish_date">
            <mat-datepicker-toggle matSuffix [for]="pickerPublishDate"></mat-datepicker-toggle>
            <mat-datepicker #pickerPublishDate></mat-datepicker>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.publish_date"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field *ngxPermissionsOnly="['set_job_closing_date']">
            <input matInput
                   [matDatepicker]="pickerClosingDate"
                   placeholder="Closing date"
                   formControlName="closing_date">
            <mat-datepicker-toggle matSuffix [for]="pickerClosingDate"></mat-datepicker-toggle>
            <mat-datepicker #pickerClosingDate></mat-datepicker>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.closing_date"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class JobDateFormComponent extends BaseFormComponent {
  public readonly tooltipText = 'To post job immediately specify today\'s date or leave the field blank.';
}
