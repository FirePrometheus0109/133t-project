import {Component, EventEmitter, Output} from '@angular/core';
import {Store} from '@ngxs/store';
import {Survey} from '../models/survey.model';
import {SurveyState} from '../states/survey.state';

@Component({
  selector: 'app-select-survey-dialog',
  template: `
    <h3 mat-dialog-title align="center">Select questions list</h3>
    <mat-dialog-content align="center">
      <app-survey-list></app-survey-list>
    </mat-dialog-content>
    <mat-dialog-actions align="center">
      <button mat-raised-button color="primary" (click)="confirmed.emit(getCurrentSurvey())">
        <mat-icon matSuffix>check</mat-icon>
        Add list to questionnaire
      </button>
      <button mat-raised-button color="accent" [matDialogClose]>
        <mat-icon matSuffix>close</mat-icon>
        Cancel
      </button>
    </mat-dialog-actions>
  `,
  styles: []
})
export class SelectSurveyDialogComponent {
  @Output() confirmed = new EventEmitter<Survey>();

  constructor(private store: Store) {
  }

  getCurrentSurvey() {
    return this.store.selectSnapshot(SurveyState.currentSurvey);
  }
}
