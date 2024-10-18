import { Component, EventEmitter, Inject, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { JSPPageState } from '../../job-seeker/states/jsp-page.state';
import { AnswersActions } from '../../survey/actions/index';
import { CoverLetterItem } from '../models/cover-letter.model';


@Component({
  selector: 'app-manage-apply-requirements-dialog',
  template: `
    <mat-card *ngIf="!modalData.is_questionnaire_answered">
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
        <button type="button" mat-raised-button color="primary" (click)="prepareAnswerData()">
          <span>Send answers</span>
          <mat-icon matSuffix>forward</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
    <mat-card *ngIf="modalData.is_cover_letter_required">
      <mat-card-title>
        <h4>Applying confirmation</h4>
      </mat-card-title>
      <mat-dialog-content>
        <mat-card-content>
          <span>Cover letter is required to apply for this job.</span>
          <span *ngIf="!(defaultCoverLetter$ | async)">
            You do not have default cover letter yet. Do you want to create a Cover letter?
          </span>
          <span *ngIf="defaultCoverLetter$ | async">Which cover letter do you want to use?</span>
          <app-cover-letter-select-form *ngIf="(coverLetter$ | async) && (coverLetter$ | async).length > 0"
                                        [initialData]="coverLetter$ | async"
                                        [form]="coverLetterSelectForm">
          </app-cover-letter-select-form>
        </mat-card-content>
      </mat-dialog-content>
      <mat-card-actions>
        <button type="button" mat-raised-button color="primary" (click)="manageCoverLetters.emit()">
          <span>Manage Cover Letters</span>
        </button>
        <button type="button" mat-raised-button color="primary"
                [disabled]="!modalData.is_questionnaire_answered || coverLetterSelectForm.invalid"
                (click)="prepareApplyData()">
          <span>Apply</span>
          <mat-icon matSuffix>forward</mat-icon>
        </button>
        <button type="button" mat-raised-button matDialogClose color="primary">
          <span>Cancel</span>
          <mat-icon matSuffix>close</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [],
})
export class ManageApplyRequirementsDialogComponent implements OnInit {
  @Select(JSPPageState.coverLetter) coverLetter$: Observable<Array<CoverLetterItem>>;
  @Select(JSPPageState.defaultCoverLetter) defaultCoverLetter$: Observable<Array<CoverLetterItem>>;

  @Output() submittedResult = new EventEmitter<any>();
  @Output() manageCoverLetters = new EventEmitter<any>();
  @Output() applyResult = new EventEmitter<any>();

  public coverLetterSelectForm = new FormGroup({
    cover_letter: new FormControl('', Validators.required),
  });

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>,
              private store: Store) {
  }

  ngOnInit() {
    this.dialogRef.afterClosed().subscribe(() => {
      this.resetAnswerList();
    });
    if (this.store.selectSnapshot(JSPPageState.defaultCoverLetter)) {
      this.coverLetterSelectForm.controls.cover_letter.setValue(this.store.selectSnapshot(JSPPageState.defaultCoverLetter).id);
    }
  }

  answerChanged(answerData) {
    this.store.dispatch(new AnswersActions.SetAnswerToAnswersList(answerData));
  }

  resetAnswerList() {
    this.store.dispatch(new AnswersActions.ResetAnswerList());
  }

  prepareAnswerData() {
    this.store.dispatch(new AnswersActions.SendAnswersList(this.modalData.jobData.id)).subscribe((result) => {
      this.modalData.is_questionnaire_answered = true;
      this.submittedResult.emit(result.AnswersState.status);
    });
  }

  prepareApplyData() {
    this.applyResult.emit(this.coverLetterSelectForm.value);
  }
}
