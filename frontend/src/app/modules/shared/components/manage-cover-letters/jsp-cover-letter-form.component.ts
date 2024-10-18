import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ConfirmationDialogService } from '../../services/confirmation-dialog.service';
import { BaseFormComponent } from '../base-form.component';


// TODO: mistake in app-control-messages errors
@Component({
  selector: 'app-jsp-cover-letter-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Cover letter</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field>
            <input type="text" matInput placeholder="Cover letter name" formControlName="title">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.title"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <mat-form-field>
            <textarea matInput placeholder="Cover letter body" formControlName="body">
            </textarea>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.body"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <mat-checkbox formControlName="is_default" (change)="changeIsDefault()">
            Set as default Cover letter
          </mat-checkbox>
          <app-control-messages [form]="form"
                                [control]="f.is_default"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <mat-action-row>
            <button type="reset" mat-raised-button color="primary" (click)="closeForm.emit()">
              Cancel
              <mat-icon matSuffix>cancel</mat-icon>
            </button>
            <button type="submit" mat-raised-button color="primary" [disabled]='!form.valid'>
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
export class JspCoverLetterFormComponent extends BaseFormComponent {
  @Input() defaultCoverLetter: any;
  @Output() closeForm = new EventEmitter<any>();

  constructor(private confirmationDialogService: ConfirmationDialogService) {
    super();
  }

  public changeIsDefault() {
    if (this.defaultCoverLetter) {
      this.confirmationDialogService.openConfirmationDialog({
        message: `You already have default cover letter. Are you sure you want to set this cover letter as default?`,
        confirmationText: `Yes`,
        negativeText: `No`,
        dismissible: true,
        callback: this.changeCheckbox.bind(this),
        callbackNegative: this.changeCheckbox.bind(this)
      });
    }
  }

  private changeCheckbox(value) {
    this.form.controls.is_default.setValue(value);
  }
}
