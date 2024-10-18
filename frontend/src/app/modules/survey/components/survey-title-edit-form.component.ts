import { Component, Input } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BaseFormComponent } from '../../shared/components/base-form.component';


@Component({
  selector: 'app-survey-title-edit-form',
  template: `
    <mat-card>
      <form [formGroup]="form" (ngSubmit)="submit()" class="container">
        <mat-card-content>
          <mat-form-field>
            <input matInput placeholder="Questions list title"
                   formControlName="title" maxlength="256">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.title"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <button type="submit" mat-raised-button color="primary" [disabled]="!form.valid">
            <span>Save</span>
            <mat-icon matSuffix>save</mat-icon>
          </button>
          <button type="button" mat-raised-button color="primary" *ngIf="view_mode">
            <span>Delete list</span>
            <mat-icon matSuffix>delete</mat-icon>
          </button>
          <button type="button" mat-raised-button color="primary" *ngIf="!view_mode" (click)="discardChanges()">
            <span>Discard changes</span>
            <mat-icon matSuffix>close</mat-icon>
          </button>
        </mat-card-content>
      </form>
    </mat-card>
  `,
  styles: [`
    .container {
      display: flex;
      flex-direction: column;
    }
  `],
})
export class SurveyTitleEditFormComponent extends BaseFormComponent {
  @Input() create_mode: boolean;
  @Input() view_mode: boolean;
  @Input() edit_mode: boolean;

  form = new FormGroup({
    title: new FormControl('', Validators.required),
    questions: new FormControl([]),
    id: new FormControl(''),
  });

  discardChanges() {
    this.form.patchValue(this.initialData);
  }
}
