import { Component, EventEmitter, Input, Output } from '@angular/core';
import { EditMode } from '../models/edit-mode.model';
import { Question } from '../models/question.model';
import { Survey } from '../models/survey.model';


@Component({
  selector: 'app-survey-preview',
  template: `
    <mat-card>
      <mat-card-title *ngIf="!job_edit_mode">
        <app-survey-title-preview *ngIf="view_mode"
                                  [surveyItem]="surveyItem"
                                  (editSurvey)="editSurvey.emit($event)"
                                  (deleteSurvey)="deleteSurvey.emit($event)">
        </app-survey-title-preview>
        <app-survey-title-edit-form *ngIf="edit_mode"
                                    [initialData]="surveyItem"
                                    (submitted)="surveyTitleSubmitted.emit($event)">
        </app-survey-title-edit-form>
      </mat-card-title>
      <mat-card-actions>
        <button *ngIf="job_edit_mode"
                type="button" mat-raised-button color="primary"
                (click)="selectSurveyFromList.emit()">
          <span>Select questions list</span>
          <mat-icon matSuffix>list_alt</mat-icon>
        </button>
        <button type="button" mat-raised-button color="primary"
                [disabled]="validationLength"
                (click)="createQuestionsFromSelected.emit()">
          <span>Select question</span>
          <mat-icon matSuffix>playlist_add</mat-icon>
        </button>
        <button type="button" mat-raised-button color="primary"
                [disabled]="validationLength"
                (click)="createNewQuestion.emit()">
          <span>Create new question</span>
          <mat-icon matSuffix>add_circle</mat-icon>
        </button>
      </mat-card-actions>
      <mat-card-content>
        <div>Questions:</div>
        <div *ngFor="let questionItem of surveyItem.questions; index as i">
          <app-question-preview *ngIf="!edit_question_mode.value || edit_question_mode.id !== questionItem.id"
                                [questionItem]="questionItem"
                                [index]="i + 1"
                                (editQuestion)="editQuestion.emit($event)"
                                (deleteQuestion)="deleteQuestionFromSurvey.emit($event)">
          </app-question-preview>
          <app-edit-question-form *ngIf="edit_question_mode.value && edit_question_mode.id === questionItem.id"
                                  [index]="i + 1"
                                  [initialData]="questionItem"
                                  [showSavedCheckBox]="false"
                                  (submitted)="editQuestionFormSubmitted.emit($event)">
          </app-edit-question-form>
        </div>
        <p *ngIf="surveyItem.questions.length === 0">No questions</p>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class SurveyPreviewComponent {
  @Input() surveyItem: Survey;
  @Input() view_mode: boolean;
  @Input() edit_mode: boolean;
  @Input() edit_question_mode: EditMode;
  @Input() create_mode: boolean;
  @Input() job_edit_mode: boolean;
  @Input() index: number;
  @Input() validationLength: boolean;
  @Output() editSurvey = new EventEmitter<Survey>();
  @Output() editQuestion = new EventEmitter<Question>();
  @Output() deleteSurvey = new EventEmitter<number>();
  @Output() surveyTitleSubmitted = new EventEmitter<Survey>();
  @Output() editQuestionFormSubmitted = new EventEmitter<Question>();
  @Output() deleteQuestionFromSurvey = new EventEmitter<number>();
  @Output() createNewQuestion = new EventEmitter<any>();
  @Output() createQuestionsFromSelected = new EventEmitter<any>();
  @Output() selectSurveyFromList = new EventEmitter<any>();
}
