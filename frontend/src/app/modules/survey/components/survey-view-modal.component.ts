import {Component, Input} from '@angular/core';
import {Survey} from '../models/survey.model';

@Component({
  selector: 'app-survey-view-modal',
  template: `
    <mat-card>
      <mat-card-title>
        <app-survey-title-preview [surveyItem]="surveyItem"
                                  [modalMode]="true">
        </app-survey-title-preview>
      </mat-card-title>
      <mat-card-content>
        <div>Questions:</div>
        <div *ngFor="let questionItem of surveyItem.questions; index as i">
          <app-question-preview [questionItem]="questionItem"
                                [index]="i + 1"
                                [modalMode]="true"
          ></app-question-preview>
        </div>
        <p *ngIf="surveyItem.questions.length === 0">No questions</p>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class SurveyViewModalComponent {
  @Input() surveyItem: Survey;
  @Input() index: number;
}
