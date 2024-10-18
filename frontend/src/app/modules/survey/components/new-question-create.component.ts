import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { UtilsService } from '../../shared/services/utils.service';
import { Question } from '../models/question.model';
import { SurveyService } from '../services/survey.service';


@Component({
  selector: 'app-new-question-create',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Create new question</h4>
      </mat-card-title>
      <mat-dialog-content>
        <mat-card-content>
          <form [formGroup]="questionsListForm">
            <div formArrayName="questions"
                 *ngFor="let question of questionsData.controls; let i = index;">
              <div [formGroupName]="i">
                <app-modal-question-create [initialData]="question.value"
                                           [form]="question"
                                           [index]="i"
                                           (deleteQuestion)="deleteQuestion($event)"></app-modal-question-create>
              </div>
            </div>
          </form>
        </mat-card-content>
      </mat-dialog-content>
      <mat-card-actions>
        <button type="button" mat-raised-button color="primary" [disabled]="!isQuestionsCountAcceptable()"
                (click)="createNewQuestion()">
          <span>Create new question</span>
          <mat-icon matSuffix>add_circle</mat-icon>
        </button>
        <button type="button" mat-raised-button color="primary" (click)="addToList()"
                [disabled]="!questionsListForm.valid">
          <span>Add questions to list</span>
          <mat-icon matSuffix>playlist_add</mat-icon>
        </button>
        <button type="button" mat-raised-button matDialogClose color="primary">
          <span>Close</span>
          <mat-icon matSuffix>close</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [],
})
export class NewQuestionCreateComponent {
  @Output() submittedResult = new EventEmitter<Array<Question>>();

  questions: FormArray;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>,
              private surveyService: SurveyService) {
  }

  questionsListForm: FormGroup = new FormGroup({
    questions: new FormArray([], Validators.maxLength(this.modalData.maxQuestionsLength - this.modalData.questionsCount)),
  });

  private static createQuestion(): FormGroup {
    return new FormGroup({
      body: new FormControl('', Validators.required),
      disqualifying_answer: new FormControl(''),
      is_answer_required: new FormControl(false),
      add_to_saved_questions: new FormControl(false),
      // add unique id for newly created question to manage editing and deleting
      id: new FormControl(UtilsService.generateUniqueId()),
    });
  }

  createNewQuestion() {
    this.questions = this.questionsData;
    this.questions.push(NewQuestionCreateComponent.createQuestion());
  }

  deleteQuestion(indexToRemove) {
    this.questions = this.questionsData;
    this.questions.removeAt(indexToRemove);
  }

  addToList() {
    this.submittedResult.emit(this.questionsListForm.value.questions);
  }

  get questionsData() {
    return <FormArray>this.questionsListForm.get('questions');
  }

  isQuestionsCountAcceptable() {
    return this.surveyService.isQuestionsCountAcceptable(this.modalData.questionsCount, this.questionsData.length);
  }
}
