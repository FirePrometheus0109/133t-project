import { Component } from '@angular/core';
import { BaseFormComponent } from '../../../shared/components/base-form.component';


@Component({
  selector: 'app-job-title-form',
  template: `
    <mat-card>
      <mat-card-content>
        <form [formGroup]="form">
          <mat-form-field>
            <input matInput
                   formControlName="title"
                   placeholder="Title"
                   required>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.title"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class JobTitleFormComponent extends BaseFormComponent {
}
