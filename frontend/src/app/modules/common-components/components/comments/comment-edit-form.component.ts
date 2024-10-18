import {Component, EventEmitter, Input, Output} from '@angular/core';
import {BaseFormComponent} from '../../../shared/components/base-form.component';

@Component({
  selector: 'app-comment-edit-form',
  template: `
    <mat-card>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field>
            <input matInput placeholder="Comment title" formControlName="title">
          </mat-form-field>
          <app-control-messages
            [form]="form"
            [control]="f.title"
            [submitted]="isSubmitted"
            [errors]="errors">
          </app-control-messages>
          <mat-form-field>
            <textarea matInput placeholder="Comment" formControlName="comment">
            </textarea>
          </mat-form-field>
          <app-control-messages
            [form]="form"
            [control]="f.comment"
            [submitted]="isSubmitted"
            [errors]="errors">
          </app-control-messages>
          <button type="submit" mat-raised-button color="primary">
            <span *ngIf="editCommentMode">Save</span>
            <span *ngIf="!editCommentMode">Add</span>
            comment
            <mat-icon matSuffix>save</mat-icon>
          </button>
          <button type="reset" mat-raised-button color="primary" *ngIf="editCommentMode" (click)="closeForm.emit()">
            Cancel
            <mat-icon matSuffix>cancel</mat-icon>
          </button>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})

export class CommentEditFormComponent extends BaseFormComponent {
  @Input() editCommentMode: boolean;
  @Output() closeForm = new EventEmitter<any>();
}
