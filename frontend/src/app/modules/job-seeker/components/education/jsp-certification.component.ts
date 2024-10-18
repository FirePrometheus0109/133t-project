import { Component, EventEmitter, Output } from '@angular/core';
import { MatCheckboxChange } from '@angular/material';
import { environment } from '../../../../../environments/environment';
import { BaseFormComponent } from '../../../shared/components/base-form.component';


@Component({
  selector: 'app-jsp-certification-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>New certification</h4>
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
            <input matInput placeholder="Field of study" formControlName="field_of_study">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.field_of_study"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input matInput [matDatepicker]="picker" placeholder="Graduated" formControlName="graduated"
                   [disabled]="f.is_current.value" [min]="dateMin" [max]="dateMax">
            <mat-datepicker-toggle matSuffix [for]="picker"></mat-datepicker-toggle>
            <mat-datepicker #picker></mat-datepicker>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.graduated"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <mat-checkbox formControlName="is_current" (change)="changeIsCurrent($event)">Currently studying</mat-checkbox>
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
            <input matInput placeholder="Licence number" formControlName="licence_number" [disabled]="f.is_current.value">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.licence_number"
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
export class JspCertificationComponent extends BaseFormComponent {
  @Output() closeForm = new EventEmitter<any>();

  dateMin = environment.dateChoiceMin;
  dateMax = new Date();

  changeIsCurrent(event: MatCheckboxChange) {
    if (event.checked) {
      this.form.controls.graduated.setValue(null);
      this.form.controls.licence_number.setValue('');
      this.form.controls.licence_number.disable();
    } else {
      this.form.controls.licence_number.enable();
    }
  }
}
