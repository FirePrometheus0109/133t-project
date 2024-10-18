import { Component } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { SavedQuestionsActions } from '../actions';
import { Question } from '../models/question.model';
import { SavedQuestionsState } from '../states/saved-questions.state';


@Component({
  selector: 'app-saved-questions',
  template: `
    <div>
      <mat-card>
        <mat-card-header>
          <mat-card-title>
            <h3>Saved questions</h3>
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <button type="submit" mat-raised-button color="primary" (click)="createNewQuestionInSaved()">
            <mat-icon matSuffix>add</mat-icon>
            Create new question
          </button>
        </mat-card-content>
        <mat-card-content>
          <app-edit-question-form *ngIf="(createMode$ | async)"
                                  [create_mode]="(createMode$ | async)"
                                  [showSavedCheckBox]="false"
                                  (closeCreation)="closeCreation()"
                                  (submitted)="editFormSubmitted($event)">
          </app-edit-question-form>
          <mat-paginator [length]="count$ | async"
                         [pageSize]="pageSize$ | async"
                         [pageSizeOptions]="pageSizeOptions$ | async"
                         (page)="onPageChanged($event)"></mat-paginator>
          <div *ngFor="let savedQuestion of (savedQuestionList$ | async); index as i">
            <app-question-preview *ngIf="!(editMode$ | async).value || (editMode$ | async).id !== savedQuestion.id"
                                  [index]="(pageSize$ | async) * (pageIndex$ | async) + i + 1"
                                  [questionItem]="savedQuestion"
                                  (editQuestion)="editQuestion($event)"
                                  (deleteQuestion)="deleteQuestion($event)">
            </app-question-preview>
            <app-edit-question-form *ngIf="(editMode$ | async).value && (editMode$ | async).id === savedQuestion.id"
                                    [index]="(pageSize$ | async) * (pageIndex$ | async) + i + 1"
                                    [initialData]="savedQuestion"
                                    [showSavedCheckBox]="false"
                                    (submitted)="editFormSubmitted($event)">
            </app-edit-question-form>
          </div>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [],
})
export class SavedQuestionsComponent {
  @Select(SavedQuestionsState.savedQuestionList) savedQuestionList$: Observable<Array<Question>>;
  @Select(SavedQuestionsState.createMode) createMode$: Observable<boolean>;
  @Select(SavedQuestionsState.editMode) editMode$: Observable<boolean>;
  @Select(SavedQuestionsState.count) count$: Observable<number>;
  @Select(SavedQuestionsState.pageSize) pageSize$: Observable<number>;
  @Select(SavedQuestionsState.pageIndex) pageIndex$: Observable<number>;
  @Select(SavedQuestionsState.pageSizeOptions) pageSizeOptions$: Observable<number>;

  constructor(private store: Store) {
  }

  createNewQuestionInSaved() {
    this.store.dispatch(new SavedQuestionsActions.SetCreationMode(true));
  }

  editFormSubmitted(formData: Question) {
    if ((this.store.selectSnapshot(SavedQuestionsState.editMode)).value) {
      this.store.dispatch(new SavedQuestionsActions.UpdateSavedQuestion(formData));
    } else {
      this.store.dispatch(new SavedQuestionsActions.CreateNewQuestion(formData));
    }
  }

  editQuestion(questionData: Question) {
    const editMode = {
      id: questionData.id,
      value: true
    };
    this.store.dispatch(new SavedQuestionsActions.SetEditMode(editMode));
  }

  deleteQuestion(questionId: number) {
    this.store.dispatch(new SavedQuestionsActions.DeleteSavedQuestion(questionId));
  }

  closeCreation() {
    this.store.dispatch(new SavedQuestionsActions.SetCreationMode(false));
  }

  onPageChanged(event: PageEvent) {
    this.store.dispatch(new SavedQuestionsActions.ChangePagination(event));
  }
}
