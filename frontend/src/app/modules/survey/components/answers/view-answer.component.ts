import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {AnswerVariants} from '../../../shared/enums/answer-variants';

@Component({
  selector: 'app-answer-view',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Questionnaire</h4>
      </mat-card-title>
      <mat-card-content *ngFor="let answerItem of modalData.answers">
        <div class="answer">
          <div>{{answerItem.question.body}}</div>
          <div>
            <mat-radio-group>
              <mat-radio-button checked="true"></mat-radio-button>
              {{AnswerVariants[answerItem.answer]}}
            </mat-radio-group>
          </div>
        </div>
      </mat-card-content>
      <mat-card-actions>
        <button type="button" mat-raised-button matDialogClose color="primary">
          <span>Close</span>
          <mat-icon matSuffix>close</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [],
})
export class ViewAnswerComponent {
  public AnswerVariants = AnswerVariants;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>) {
  }
}
