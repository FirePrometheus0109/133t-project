import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CoreActions } from '../../core/actions';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { SurveyEditActions, SurveyListActions } from '../actions';
import { EditMode } from '../models/edit-mode.model';
import { Question } from '../models/question.model';
import { Survey } from '../models/survey.model';
import { SurveyService } from '../services/survey.service';

export const updateSurveyMessage = `You have successfully updated questionnaire.`;


class SurveyEditStateModel {
  status: string;
  errors: object;
  createQuestionMode: boolean;
  editQuestionMode: EditMode;
  viewQuestionMode: boolean;
  questionList: Array<Question>;
  surveyToEdit: Survey;
}


export const SURVEY_EDIT_STATE = {
  status: 'ready',
  errors: null,
  createQuestionMode: false,
  editQuestionMode: {
    id: null,
    value: false
  },
  viewQuestionMode: false,
  questionList: [],
  surveyToEdit: null,
};


@State<SurveyEditStateModel>({
  name: 'SurveyEdit',
  defaults: SURVEY_EDIT_STATE
})
export class SurveyEditState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static questionList(state: SurveyEditStateModel): Array<Question> {
    return state.questionList;
  }

  @Selector()
  static createQuestionMode(state: SurveyEditStateModel): boolean {
    return state.createQuestionMode;
  }

  @Selector()
  static viewQuestionMode(state: SurveyEditStateModel): boolean {
    return state.viewQuestionMode;
  }

  @Selector()
  static editQuestionMode(state: SurveyEditStateModel): EditMode {
    return state.editQuestionMode;
  }

  @Selector()
  static surveyToEdit(state: SurveyEditStateModel): Survey {
    return state.surveyToEdit;
  }

  constructor(private surveyService: SurveyService) {
  }

  @Action(SurveyEditActions.DeleteSurvey)
  deleteSurvey(ctx: StateContext<SurveyEditStateModel>, {surveyId}: SurveyEditActions.DeleteSurvey) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.deleteSurvey(surveyId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully deleted the questions list.',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
        state = ctx.getState();
        ctx.dispatch(new SurveyListActions.SetCurrentSurvey(null));
        ctx.dispatch(new SurveyListActions.UpdateSurveyList());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(SurveyEditActions.CreateNewSurvey)
  createNewSurvey(ctx: StateContext<SurveyEditStateModel>, {newSurvey}: SurveyEditActions.CreateNewSurvey) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.createNewSurvey(newSurvey).pipe(
      tap((savedSurvey: Survey) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully created new questions list.',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
        ctx.dispatch(new SurveyListActions.SetCurrentSurvey(null));
        ctx.dispatch(new SurveyListActions.SetCurrentSurvey(savedSurvey));
        ctx.dispatch(new SurveyListActions.SetViewMode(true));
        return ctx.dispatch(new SurveyListActions.UpdateSurveyList());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(SurveyEditActions.UpdateSurveyTitle)
  updateSurveyTitle(ctx: StateContext<SurveyEditStateModel>, {survey}: SurveyEditActions.UpdateSurveyTitle) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.updateSurveyTitle(survey.id, survey.title).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully updated questions list.',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
        ctx.dispatch(new SurveyListActions.SetViewMode(true));
        ctx.dispatch(new SurveyListActions.UpdateCurrentSurvey(survey.id));
        return ctx.dispatch(new SurveyListActions.UpdateSurveyList());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(SurveyEditActions.DeleteQuestionFromSurvey)
  deleteQuestionFromSurvey(ctx: StateContext<SurveyEditStateModel>, {surveyId, questionId}: SurveyEditActions.DeleteQuestionFromSurvey) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.deleteQuestionFromSurvey(surveyId, questionId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new SurveyListActions.UpdateCurrentSurvey(surveyId));
        ctx.dispatch(new SurveyListActions.UpdateSurveyList());
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully deleted question.',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(SurveyEditActions.UpdateQuestionInSurvey)
  updateQuestionInSurvey(ctx: StateContext<SurveyEditStateModel>, {surveyId, questionData}: SurveyEditActions.UpdateQuestionInSurvey) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.updateQuestionInSurvey(surveyId, questionData.id, questionData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new SurveyEditActions.SetEditQuestionMode({value: null, id: null}));
        ctx.dispatch(new SurveyListActions.UpdateCurrentSurvey(surveyId));
        ctx.dispatch(new SurveyListActions.UpdateSurveyList());
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully updated question.',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(SurveyEditActions.SaveNewlyCreatedQuestions)
  saveNewlyCreatedQuestions(ctx: StateContext<SurveyEditStateModel>,
                            {surveyId, questionList}: SurveyEditActions.SaveNewlyCreatedQuestions) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.addNewlyCreatedQuestionsToSurvey(surveyId, questionList).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new SurveyListActions.UpdateCurrentSurvey(surveyId));
        ctx.dispatch(new SurveyListActions.UpdateSurveyList());
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: updateSurveyMessage,
          delay: 3000,
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(SurveyEditActions.SaveQuestionsFromSelected)
  saveQuestionsFromSelected(ctx: StateContext<SurveyEditStateModel>,
                            {surveyId, questionList}: SurveyEditActions.SaveQuestionsFromSelected) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.addQuestionsFromSelectedToSurvey(surveyId, questionList).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new SurveyListActions.UpdateCurrentSurvey(surveyId));
        ctx.dispatch(new SurveyListActions.UpdateSurveyList());
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: updateSurveyMessage,
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(SurveyEditActions.SetCreateQuestionMode)
  setCreateQuestionMode(ctx: StateContext<SurveyEditStateModel>, {value}: SurveyEditActions.SetCreateQuestionMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      createQuestionMode: value,
    });
  }

  @Action(SurveyEditActions.SetViewQuestionMode)
  setViewQuestionMode(ctx: StateContext<SurveyEditStateModel>, {value}: SurveyEditActions.SetViewQuestionMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      viewQuestionMode: value,
    });
  }

  @Action(SurveyEditActions.SetEditQuestionMode)
  setEditQuestionMode(ctx: StateContext<SurveyEditStateModel>, {value}: SurveyEditActions.SetEditQuestionMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      editQuestionMode: value,
    });
  }

  @Action(SurveyEditActions.SetSurveyToEdit)
  setSurveyToEdit(ctx: StateContext<SurveyEditStateModel>, {survey}: SurveyEditActions.SetSurveyToEdit) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      surveyToEdit: survey,
    });
  }
}
