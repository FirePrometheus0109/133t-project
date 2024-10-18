import { Component, EventEmitter, Inject, OnInit, Output } from '@angular/core';
import { FormArray, FormControl, FormGroup } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { Question } from '../models/question.model';


@Component({
  selector: 'app-new-question-create',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Select question</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="questionsListForm">
          <mat-tab-group>
            <mat-tab label="Default questions">
              <ng-template matTabContent>
                <div formArrayName="default_questions"
                     *ngFor="let item of questionsListForm.controls['default_questions'].controls; let i = index">
                  <mat-checkbox type="checkbox" [formControlName]="i"></mat-checkbox>
                  {{i + 1}}.{{defaultQuestionsList[i].body}}
                </div>
              </ng-template>
            </mat-tab>
            <mat-tab label="Saved questions">
              <ng-template matTabContent>
                <div formArrayName="saved_questions"
                     *ngFor="let item of questionsListForm.controls['saved_questions'].controls; let j = index">
                  <mat-checkbox type="checkbox" [formControlName]="j"></mat-checkbox>
                  {{j + 1}}.{{savedQuestionsList[j].body}}
                </div>
              </ng-template>
            </mat-tab>
          </mat-tab-group>
        </form>
      </mat-card-content>
      <mat-card-actions>
        <button type="button" mat-raised-button color="primary" [disabled]="!addSelectedConfirmed"
                (click)="addToList()">
          <span>Add selected</span>
          <mat-icon matSuffix>playlist_add</mat-icon>
        </button>
        <span *ngIf="!addSelectedConfirmed" class="error">
          Only {{modalData.maxQuestionsLength - modalData.questionsCount}} questions can be added
        </span>
        <button type="button" mat-raised-button matDialogClose color="primary">
          <span>Close</span>
          <mat-icon matSuffix>close</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [`
    .error {
      color: red;
    }
  `],
})
export class QuestionsFromSelectedComponent implements OnInit {
  @Output() submittedResult = new EventEmitter<Array<Question>>();

  defaultQuestionsList: Array<Question>;
  savedQuestionsList: Array<Question>;
  questionsListForm: FormGroup;
  job_edit_mode: boolean;
  addSelectedConfirmed = true;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>) {
  }

  ngOnInit() {
    this.defaultQuestionsList = this.modalData.default_questions;
    this.savedQuestionsList = this.modalData.saved_questions;
    this.job_edit_mode = this.modalData.job_edit_mode;
    const default_controls = this.defaultQuestionsList.map(() => new FormControl(false));
    const saved_controls = this.savedQuestionsList.map(() => new FormControl(false));
    this.questionsListForm = new FormGroup({
      default_questions: new FormArray(default_controls),
      saved_questions: new FormArray(saved_controls),
    });
    this.questionsListForm.valueChanges.subscribe((value) => {
      const selected_questions_count = this.countTrueValue(value.default_questions) +
        this.countTrueValue(value.saved_questions);
      (selected_questions_count > this.modalData.maxQuestionsLength - this.modalData.questionsCount) ?
        this.addSelectedConfirmed = false : this.addSelectedConfirmed = true;
    });
  }

  addToList() {
    const selectedDefaultQuestionsIds = this.questionsListForm.value.default_questions
      .map((value, index) => value ? this.job_edit_mode ? this.defaultQuestionsList[index] : this.defaultQuestionsList[index].id : null)
      .filter(value => value !== null);
    const selectedSavedQuestionsIds = this.questionsListForm.value.saved_questions
      .map((value, index) => value ? this.job_edit_mode ? this.savedQuestionsList[index] : this.savedQuestionsList[index].id : null)
      .filter(value => value !== null);
    const resultIds = selectedDefaultQuestionsIds.concat(selectedSavedQuestionsIds);
    this.submittedResult.emit(resultIds);
  }

  private countTrueValue(formArray) {
    return formArray.filter((form) => form === true).length;
  }
}
