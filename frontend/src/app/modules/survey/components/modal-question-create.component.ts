import { Component, EventEmitter, Input, Output } from '@angular/core';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { Question, QuestionDefault } from '../models/question.model';


@Component({
  selector: 'app-modal-question-create',
  template: `
    <mat-card>
      <form [formGroup]="form" class="container">
        <mat-card-content>
          <div class="question-body">
            <div class="question-index">{{index + 1}}.</div>
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
          <mat-checkbox formControlName="add_to_saved_questions">Add to saved question</mat-checkbox>
          <app-control-messages [form]="form"
                                [control]="f.add_to_saved_questions"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
        </mat-card-content>
        <mat-card-actions>
          <button type="button" mat-raised-button color="primary" (click)="discardChanges()">
            <span>Discard changes</span>
            <mat-icon matSuffix>settings_backup_restore</mat-icon>
          </button>
          <button type="button" mat-raised-button color="primary" (click)="deleteQuestion.emit(index)">
            <span>Close</span>
            <mat-icon matSuffix>delete</mat-icon>
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

    mat-form-field {
      width: 100%;
    }
  `],
})
export class ModalQuestionCreateComponent extends BaseFormComponent {
  @Input() index: number;
  @Input() defaultQuestionValue: Question;
  @Output() deleteQuestion = new EventEmitter<any>();

  answerVariants = [
    {caption: 'Yes', value: 'YES'},
    {caption: 'No', value: 'NO'},
  ];

  discardChanges() {
    this.form.patchValue(QuestionDefault);
  }
}
