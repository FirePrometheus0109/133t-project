import {Component, EventEmitter, Inject, OnInit, Output} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {Store} from '@ngxs/store';
import {AnswersActions} from '../../actions';

@Component({
  selector: 'app-answer-questions',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Questionnaire</h4>
        <mat-card-subtitle>
          Please answer following question to apply for this job
        </mat-card-subtitle>
      </mat-card-title>
      <mat-dialog-content>
        <mat-card-content *ngFor="let questionItem of modalData.questions">
          <app-yes-no-answer-form [questionItem]="questionItem"
                                  (change)="answerChanged($event)"></app-yes-no-answer-form>
        </mat-card-content>
      </mat-dialog-content>
      <mat-card-actions>
        <button type="button" mat-raised-button matDialogClose color="primary" (click)="resetAnswerList()">
          <span>Close</span>
          <mat-icon matSuffix>close</mat-icon>
        </button>
        <button type="button" mat-raised-button color="primary" (click)="prepareData()">
          <span>Send answers and apply</span>
          <mat-icon matSuffix>forward</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [],
})
export class AnswerQuestionsComponent implements OnInit {
  @Output() submittedResult = new EventEmitter<any>();

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>,
              private store: Store) {
  }

  ngOnInit() {
    this.dialogRef.afterClosed().subscribe(() => {
      this.resetAnswerList();
    });
  }

  answerChanged(answerData) {
    this.store.dispatch(new AnswersActions.SetAnswerToAnswersList(answerData));
  }

  resetAnswerList() {
    this.store.dispatch(new AnswersActions.ResetAnswerList());
  }

  prepareData() {
    this.store.dispatch(new AnswersActions.SendAnswersList(this.modalData.jobData.id)).subscribe((result) => {
      this.submittedResult.emit(result.AnswersState.status);
    });
  }
}
