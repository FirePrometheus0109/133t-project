import { Component } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { SurveyListActions } from '../actions';
import { Survey } from '../models/survey.model';
import { SurveyState } from '../states/survey.state';


@Component({
  selector: 'app-survey-list',
  template: `
    <div>
      <mat-card>
        <mat-card-header>
          <mat-card-title>
            <h3>Questions lists</h3>
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div class="container">
            <div class="question-list-container">
              <div class="question-list">
                <mat-form-field>
                  <mat-icon matPrefix>search</mat-icon>
                  <input matInput placeholder="Question list name" type="search" (change)="searchSurvey($event)">
                </mat-form-field>
                <mat-paginator [length]="count$ | async"
                               [pageSize]="pageSize$ | async"
                               [pageSizeOptions]="pageSizeOptions$ | async"
                               (page)="onPageChanged($event)">
                </mat-paginator>
                <div *ngFor="let surveyItem of (surveyList$ | async); index as i">
                  <p (click)="showSurveyItem(surveyItem)" class="survey-item">
                    {{(pageSize$ | async) * (pageIndex$ | async) + i + 1}}.&nbsp;{{surveyItem.title}}
                  </p>
                </div>
                <p *ngIf="(surveyList$ | async).length === 0">no results</p>
                <button *ngIf="!(modalMode$ | async)"
                        type="button" mat-raised-button color="primary"
                        (click)="createNewQuestionList()">
                  <mat-icon matSuffix>add</mat-icon>
                  Create new questions list
                </button>
              </div>
            </div>
            <div class="survey-container">
              <app-survey-edit-container></app-survey-edit-container>
              <app-survey-view-modal *ngIf="(modalMode$ | async) && (currentSurvey$ | async)"
                                     [surveyItem]="(currentSurvey$ | async)">
              </app-survey-view-modal>
            </div>
          </div>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [`
    .container {
      display: flex;
      justify-content: space-around;
    }

    .question-list {
      display: flex;
      flex-direction: column;
    }

    .survey-item {
      cursor: pointer;
    }
  `],
})
export class SurveyListComponent {
  @Select(SurveyState.surveyList) surveyList$: Observable<Array<Survey>>;
  @Select(SurveyState.currentSurvey) currentSurvey$: Observable<Array<Survey>>;
  @Select(SurveyState.count) count$: Observable<number>;
  @Select(SurveyState.pageSize) pageSize$: Observable<number>;
  @Select(SurveyState.pageIndex) pageIndex$: Observable<number>;
  @Select(SurveyState.pageSizeOptions) pageSizeOptions$: Observable<number>;
  @Select(SurveyState.modalMode) modalMode$: Observable<boolean>;

  constructor(private store: Store) {
  }

  createNewQuestionList() {
    this.store.dispatch(new SurveyListActions.SetCreationMode(true));
  }

  onPageChanged(event: PageEvent) {
    this.store.dispatch(new SurveyListActions.ChangePagination(event));
  }

  showSurveyItem(survey: Survey) {
    this.store.dispatch(new SurveyListActions.SetViewMode(true));
    this.store.dispatch(new SurveyListActions.SetCurrentSurvey(survey));
  }

  searchSurvey(searchField) {
    this.store.dispatch(new SurveyListActions.SearchSurvey(searchField.target.value));
  }
}
