import {Component} from '@angular/core';
import {BaseFormComponent} from '../base-form.component';

@Component({
  selector: 'app-cover-letter-select-form',
  template: `
    <form [formGroup]="form">
      <mat-form-field>
        <mat-select
          placeholder="Select cover letter"
          formControlName="cover_letter"
          required>
          <mat-option *ngFor="let coverLetter of initialData" [value]="coverLetter.id">
            {{coverLetter.title}}<span *ngIf="coverLetter.is_default">(default)</span>
          </mat-option>
        </mat-select>
      </mat-form-field>
      <app-control-messages
        [form]="form"
        [control]="f.cover_letter"
        [submitted]="isSubmitted"
        [errors]="errors">
      </app-control-messages>
    </form>
  `,
  styles: [],
})
export class CoverLetterSelectFormComponent extends BaseFormComponent {
}
