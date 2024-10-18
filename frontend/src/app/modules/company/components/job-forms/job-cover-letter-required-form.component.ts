import {Component} from '@angular/core';
import {BaseFormComponent} from '../../../shared/components/base-form.component';

@Component({
  selector: 'app-job-cover-letter-required-form',
  template: `
    <mat-card *ngxPermissionsOnly="['set_job_is_cover_letter_required']">
      <mat-card-content>
        <form [formGroup]="form">
          <mat-checkbox formControlName="is_cover_letter_required">Cover Letter Required</mat-checkbox>
          <app-control-messages
            [form]="form"
            [control]="f.is_cover_letter_required"
            [submitted]="isSubmitted"
            [errors]="errors">
          </app-control-messages>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class JobCoverLetterRequiredFormComponent extends BaseFormComponent {
}
