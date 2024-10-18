import { Component } from '@angular/core';
import { MatDialog } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { DEFAULT_PAGINATED_OPTIONS } from '../../shared/models/paginated-data.model';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { DefaultQuestionsActions, SavedQuestionsActions, SurveyEditActions, SurveyListActions } from '../actions';
import { NewQuestionCreateComponent } from '../components/new-question-create.component';
import { QuestionsFromSelectedComponent } from '../components/questions-from-selected.component';
import { SelectSurveyDialogComponent } from '../components/select-survey-dialog.component';
import { Question } from '../models/question.model';
import { Survey } from '../models/survey.model';
import { DefaultQuestionsState } from '../states/default-questions.state';
import { SavedQuestionsState } from '../states/saved-questions.state';
import { SurveyEditState } from '../states/survey-edit.state';
import { SurveyState } from '../states/survey.state';


@Component({
  selector: 'app-survey-edit-container',
  template: `
    <div>
      <mat-card>
        <mat-card-content>
          <div class="survey-preview"
               *ngIf="(currentSurvey$ | async) && ((viewMode$ | async) || (editMode$ | async))">
            <app-survey-preview *ngIf="!(modalMode$ | async) && !(jobEditMode$ | async)"
                                [surveyItem]="(currentSurvey$ | async)"
                                [view_mode]="(viewMode$ | async)"
                                [edit_mode]="(editMode$ | async)"
                                [edit_question_mode]="(editQuestionMode$ | async)"
                                [validationLength]="isQuestionLengthLimit()"
                                (editSurvey)="editSurvey($event)"
                                (editQuestion)="editQuestion($event)"
                                (surveyTitleSubmitted)="surveyTitleSubmitted($event)"
                                (editQuestionFormSubmitted)="editQuestionFormSubmitted($event)"
                                (deleteQuestionFromSurvey)="deleteQuestionFromSurvey($event)"
                                (deleteSurvey)="deleteSurvey($event)"
                                (createNewQuestion)="createNewQuestion()"
                                (createQuestionsFromSelected)="createQuestionsFromSelected()">
            </app-survey-preview>
          </div>
          <div class="survey-preview-job-edit" *ngIf="(jobEditMode$ | async) && !(modalMode$ | async)">
            <app-survey-preview [surveyItem]="(surveyForJobEdit$ | async)"
                                [edit_question_mode]="(editQuestionMode$ | async)"
                                [job_edit_mode]="(jobEditMode$ | async)"
                                [validationLength]="isQuestionLengthLimit()"
                                (selectSurveyFromList)="selectSurveyFromList()"
                                (editQuestion)="editQuestion($event)"
                                (editQuestionFormSubmitted)="editQuestionFormSubmitted($event)"
                                (deleteQuestionFromSurvey)="deleteQuestionFromSurvey($event)"
                                (createNewQuestion)="createNewQuestion()"
                                (createQuestionsFromSelected)="createQuestionsFromSelected()">
            </app-survey-preview>
          </div>
          <div class="survey-create" *ngIf="(createMode$ | async)">
            <app-survey-title-edit-form (submitted)="surveyTitleSubmitted($event)"
                                        [create_mode]="(createMode$ | async)">
            </app-survey-title-edit-form>
          </div>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [],
})
export class SurveyEditComponent {
  @Select(SurveyState.currentSurvey) currentSurvey$: Observable<Survey>;
  @Select(SurveyState.surveyForJobEdit) surveyForJobEdit$: Observable<Survey>;
  @Select(SurveyState.createMode) createMode$: Observable<boolean>;
  @Select(SurveyState.editMode) editMode$: Observable<boolean>;
  @Select(SurveyState.viewMode) viewMode$: Observable<boolean>;
  @Select(SurveyState.modalMode) modalMode$: Observable<boolean>;
  @Select(SurveyState.jobEditMode) jobEditMode$: Observable<boolean>;
  @Select(SurveyState.questionsCountInSurvey) questionsCountInSurvey$: Observable<number>;
  @Select(SurveyEditState.createQuestionMode) createQuestionMode$: Observable<boolean>;
  @Select(SurveyEditState.editQuestionMode) editQuestionMode$: Observable<boolean>;
  @Select(SurveyEditState.surveyToEdit) surveyToEdit$: Observable<Survey>;

  private selectSurveyMessage = 'Selecting questions list will delete all questions that you already have in the questionnaire';
  private selectSurveyModalTitle = 'Confirm selection';
  private selectSurveyConfirmButtonText = 'I want to add new questions list';
  private selectSurveyNegativeButtonText = 'No';

  constructor(private store: Store,
              public dialog: MatDialog,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  surveyTitleSubmitted(value) {
    if (this.store.selectSnapshot(SurveyState.createMode)) {
      this.store.dispatch(new SurveyEditActions.CreateNewSurvey(value));
    } else if (this.store.selectSnapshot(SurveyState.editMode)) {
      this.store.dispatch(new SurveyEditActions.UpdateSurveyTitle(value));
    }
  }

  editQuestionFormSubmitted(updatedQuestionData: Question) {
    if (this.jobEditMode) {
      this.store.dispatch(new SurveyEditActions.SetEditQuestionMode({value: null, id: null}));
      this.store.dispatch(new SurveyListActions.UpdateQuestionInSurveyForJobEdit(updatedQuestionData));
    } else {
      const currentSurvey = this.currentSurvey;
      this.store.dispatch(new SurveyEditActions.UpdateQuestionInSurvey(currentSurvey.id, updatedQuestionData));
    }
  }

  deleteQuestionFromSurvey(questionId: number) {
    if (this.jobEditMode) {
      this.store.dispatch(new SurveyListActions.DeleteQuestionFromSurveyForJobEdit(questionId));
    } else {
      const currentSurvey = this.currentSurvey;
      this.store.dispatch(new SurveyEditActions.DeleteQuestionFromSurvey(currentSurvey.id, questionId));
    }
  }

  editSurvey(currentSurvey: Survey) {
    this.store.dispatch(new SurveyListActions.SetEditMode(true));
    this.store.dispatch(new SurveyEditActions.SetSurveyToEdit(currentSurvey));
  }

  editQuestion(questionData: Question) {
    const editMode = {
      value: true,
      id: questionData.id
    };
    this.store.dispatch(new SurveyEditActions.SetEditQuestionMode(editMode));
  }

  deleteSurvey(surveyId: number) {
    this.store.dispatch(new SurveyEditActions.DeleteSurvey(surveyId));
  }

  createNewQuestion() {
    const currentSurvey = this.currentSurvey;
    const dialogRef = this.dialog.open(NewQuestionCreateComponent, {
      width: '80%',
      data: {
        maxQuestionsLength: environment.maxQuestionsLength,
        questionsCount: this.store.selectSnapshot(SurveyState.questionsCountInSurvey)
      }
    });
    dialogRef.componentInstance.submittedResult.subscribe((result) => {
      if (this.jobEditMode) {
        const resultQuestions = this.buildNewQuestionsList(result);
        this.store.dispatch(new SurveyListActions.UpdateSurveyForJobEdit(resultQuestions));
      } else {
        this.store.dispatch(new SurveyEditActions.SaveNewlyCreatedQuestions(currentSurvey.id, result));
      }
      dialogRef.close();
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.componentInstance.submittedResult.unsubscribe();
      dialogRef.close();
    });
  }

  createQuestionsFromSelected() {
    const currentSurvey = this.currentSurvey;
    let defaultQuestions = [];
    let savedQuestions = [];
    this.getDefaultAndSavedQuestions().subscribe(() => {
      defaultQuestions = this.store.selectSnapshot(DefaultQuestionsState.defaultQuestionList);
      savedQuestions = this.store.selectSnapshot(SavedQuestionsState.savedQuestionList);
      const dialogRef = this.dialog.open(QuestionsFromSelectedComponent, {
        width: '80%',
        data: {
          default_questions: defaultQuestions,
          saved_questions: savedQuestions,
          job_edit_mode: this.jobEditMode,
          maxQuestionsLength: environment.maxQuestionsLength,
          questionsCount: this.store.selectSnapshot(SurveyState.questionsCountInSurvey)
        }
      });
      dialogRef.componentInstance.submittedResult.subscribe((result) => {
        if (this.jobEditMode) {
          const resultQuestions = this.buildNewQuestionsList(result);
          this.store.dispatch(new SurveyListActions.UpdateSurveyForJobEdit(resultQuestions));
        } else {
          this.store.dispatch(new SurveyEditActions.SaveQuestionsFromSelected(currentSurvey.id, result));
        }
        dialogRef.close();
      });
      dialogRef.afterClosed().subscribe(() => {
        dialogRef.componentInstance.submittedResult.unsubscribe();
        dialogRef.close();
      });
    });
  }

  public addSurveyFromList() {
    this.store.dispatch(new SurveyListActions.LoadSurveyList(DEFAULT_PAGINATED_OPTIONS.limit, DEFAULT_PAGINATED_OPTIONS.offset))
      .subscribe(() => {
        this.store.dispatch(new SurveyListActions.SetModalMode(true));
        const dialogRef = this.dialog.open(SelectSurveyDialogComponent, {
          width: '60%',
        });
        dialogRef.componentInstance.confirmed.subscribe((result) => {
          this.store.dispatch(new SurveyListActions.UpdateSurveyForJobEdit(result.questions));
          dialogRef.close();
        });
        dialogRef.afterClosed().subscribe(() => {
          this.store.dispatch(new SurveyListActions.SetModalMode(false));
          this.store.dispatch(new SurveyListActions.SetCurrentSurvey(null));
          dialogRef.componentInstance.confirmed.unsubscribe();
          dialogRef.close();
        });
      });
  }

  public selectSurveyFromList() {
    if (this.surveyForJobEdit.questions.length > 0) {
      this.confirmationDialogService.openConfirmationDialog({
        message: `${this.selectSurveyMessage}`,
        callback: this.addSurveyFromList.bind(this),
        arg: null,
        confirmationText: `${this.selectSurveyConfirmButtonText}`,
        negativeText: `${this.selectSurveyNegativeButtonText}`,
        title: `${this.selectSurveyModalTitle}`,
      });
    } else {
      this.addSurveyFromList();
    }
  }

  get currentSurvey() {
    return this.store.selectSnapshot(SurveyState.currentSurvey);
  }

  get jobEditMode() {
    return this.store.selectSnapshot(SurveyState.jobEditMode);
  }

  get surveyForJobEdit() {
    return this.store.selectSnapshot(SurveyState.surveyForJobEdit);
  }

  buildNewQuestionsList(newQuestions: Array<Question>) {
    const existingQuestions = this.surveyForJobEdit.questions;
    return existingQuestions.concat(newQuestions);
  }

  isQuestionLengthLimit() {
    if (this.jobEditMode) {
      return this.surveyForJobEdit.questions.length >= environment.maxQuestionsLength;
    } else {
      return this.currentSurvey.questions.length >= environment.maxQuestionsLength;
    }
  }

  private getDefaultAndSavedQuestions() {
    return forkJoin(
      this.store.dispatch(new DefaultQuestionsActions.LoadDefaultQuestionList()),
      this.store.dispatch(new SavedQuestionsActions
        .LoadSavedQuestionList(DEFAULT_PAGINATED_OPTIONS.limit, DEFAULT_PAGINATED_OPTIONS.offset))
    );
  }
}
