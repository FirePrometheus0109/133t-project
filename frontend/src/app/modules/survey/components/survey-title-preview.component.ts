import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Survey} from '../models/survey.model';

@Component({
  selector: 'app-survey-title-preview',
  template: `
    <div>
      <h4>{{surveyItem.title}}</h4>
      <div *ngIf="!modalMode">
        <button type="button" mat-raised-button color="primary" (click)="editSurvey.emit(surveyItem)">
          <mat-icon matSuffix>edit</mat-icon>
        </button>
        <button type="button" mat-raised-button color="primary" (click)="deleteSurvey.emit(surveyItem.id)">
          <mat-icon matSuffix>delete</mat-icon>
        </button>
      </div>
    </div>
  `,
  styles: [],
})
export class SurveyTitlePreviewComponent {
  @Input() surveyItem: Survey;
  @Input() modalMode: boolean;
  @Output() editSurvey = new EventEmitter<Survey>();
  @Output() deleteSurvey = new EventEmitter<number>();
}
