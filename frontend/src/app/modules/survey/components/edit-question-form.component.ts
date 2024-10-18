import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BaseFormComponent } from '../../shared/components/base-form.component';


@Component({
  selector: 'app-edit-question-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4 *ngIf="create_mode">Create</h4>
        <h4 *ngIf="!create_mode">Edit</h4>
      </mat-card-title>
      <form [formGroup]="form" (ngSubmit)="submit()" class="container">
        <mat-card-content>
          <div class="question-body">
            <div *ngIf="index" class="question-index">{{index}}.</div>
            <mat-form-field>
              <input matInput placeholder="Write your question(should match to answer Yes or No)"
                     formControlName="body" maxlength="256">
            </mat-form-field>
          </div>
          <app-control-messages [form]="form"
                                [control]="f.body"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <mat-radio-group formControlName="disqualifying_answer">
            <div class="answer-variant" *ngFor="let answer of answerVariants">
              <mat-icon matSuffix>arrow_right_alt</mat-icon>
              {{answer.caption}}
              <mat-radio-button value="{{answer.value}}">Disqualifying answer</mat-radio-button>
            </div>
          </mat-radio-group>
          <mat-checkbox formControlName="is_answer_required">Answer required</mat-checkbox>
          <app-control-messages [form]="form"
                                [control]="f.is_answer_required"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <div *ngIf="showSavedCheckBox">
            <mat-checkbox formControlName="add_to_saved_questions">Add to saved question</mat-checkbox>
            <app-control-messages [form]="form"
                                  [control]="f.add_to_saved_questions"
                                  [submitted]="isSubmitted"
                                  [errors]="errors">
            </app-control-messages>
          </div>
        </mat-card-content>
        <mat-card-actions>
          <button type="submit" mat-raised-button color="primary" [disabled]="form.invalid">
            <span *ngIf="create_mode">Create question</span>
            <span *ngIf="!create_mode">Save question</span>
            <mat-icon matSuffix>save</mat-icon>
          </button>
          <button type="button" mat-raised-button color="primary" *ngIf="!create_mode" (click)="discardChanges()">
            <span>Discard changes</span>
            <mat-icon matSuffix>settings_backup_restore</mat-icon>
          </button>
          <button type="button" mat-raised-button color="primary" *ngIf="create_mode" (click)="closeCreation.emit()">
            <span>Close</span>
            <mat-icon matSuffix>close</mat-icon>
          </button>
        </mat-card-actions>
      </form>
    </mat-card>
  `,
  styles: [`
    .container {
      display: flex;
      flex-direction: column;
    }

    .answer-variant {
      display: flex;
      align-items: center;
    }

    .question-body {
      display: flex;
      flex-direction: row;
    }

    .question-index {
      margin-right: 10px;
    }
  `],
})
export class EditQuestionFormComponent extends BaseFormComponent {
  @Input() create_mode: boolean;
  @Input() edit_mode: boolean;
  @Input() index: number;
  @Input() showSavedCheckBox = true;
  @Output() closeCreation = new EventEmitter<any>();

  answerVariants = [
    {caption: 'Yes', value: 'YES'},
    {caption: 'No', value: 'NO'},
  ];

  form = new FormGroup({
    body: new FormControl('', Validators.required),
    disqualifying_answer: new FormControl(''),
    is_answer_required: new FormControl(false),
    add_to_saved_questions: new FormControl(false),
    id: new FormControl(''),
  });

  discardChanges() {
    this.form.patchValue(this.initialData);
  }
}
