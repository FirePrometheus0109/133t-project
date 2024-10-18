import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatCheckboxChange } from '@angular/material';
import { environment } from '../../../../../environments/environment';
import { BaseFormComponent } from '../../../shared/components/base-form.component';
import { Enums } from '../../../shared/models/enums.model';


@Component({
  selector: 'app-jsp-experience-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Experience</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field>
            <input matInput placeholder="Company" formControlName="company">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.company"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input matInput placeholder="Job title" formControlName="job_title">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.job_title"
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

          <mat-checkbox formControlName="is_current" (change)="changeIsCurrent($event)">Currently work here</mat-checkbox>
          <app-control-messages [form]="form"
                                [control]="f.is_current"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <mat-radio-group formControlName="employment" class="employment">
            <mat-radio-button *ngFor="let employment of enums.Employment | keys" [value]="employment.key">
              {{employment.value}}
            </mat-radio-button>
          </mat-radio-group>
          <app-control-messages [form]="form"
                                [control]="f.employment"
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
            <button type="submit" mat-raised-button color="primary" (click)="markEmploymentControl()">
              Save
              <mat-icon matSuffix>save</mat-icon>
            </button>
          </mat-action-row>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .employment {
      display: flex;
      flex-direction: column;
    }
  `],
})
export class JspExperienceFormComponent extends BaseFormComponent {
  @Input() enums: Enums;
  @Output() closeForm = new EventEmitter<any>();

  dateMin = environment.dateChoiceMin;
  dateMax = new Date();

  changeIsCurrent(event: MatCheckboxChange) {
    if (event.checked) {
      this.form.controls.date_to.setValue(null);
    }
  }

  markEmploymentControl() {
    this.form.controls.employment.markAsTouched();
  }
}
