import {Component} from '@angular/core';
import {BaseFormComponent} from '../../../shared/components/base-form.component';

@Component({
  selector: 'app-job-description-form',
  template: `
    <mat-card>
      <mat-card-content>
        <form [formGroup]="form">
          <mat-form-field>
            <textarea
              rows='10'
              matInput
              formControlName="description"
              placeholder="Description"
              required></textarea>
          </mat-form-field>
          <app-control-messages
            [form]="form"
            [control]="f.description"
            [submitted]="isSubmitted"
            [errors]="errors">
          </app-control-messages>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    mat-form-field {
      width: 100%;
    }
  `],
})
export class JobDescriptionFormComponent extends BaseFormComponent {
}
