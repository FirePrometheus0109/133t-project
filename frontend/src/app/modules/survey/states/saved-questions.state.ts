import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { ViewCompanyListPageActions } from '../../company/actions';
import { CoreActions } from '../../core/actions';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { SavedQuestionsActions } from '../actions';
import { EditMode } from '../models/edit-mode.model';
import { Question } from '../models/question.model';
import { SavedQuestionsService } from '../services/saved-questions.service';


class SavedQuestionsStateModel extends BasePaginatedPageStateModel {
  createMode: boolean;
  editMode: EditMode;
  savedQuestionList: Array<Question>;
}


export const SAVED_QUESTIONS_STATE = {
  ...DEFAULT_PAGINATED_STATE,
  createMode: false,
  editMode: {
    id: null,
    value: false
  },
  savedQuestionList: [],
};


@State<SavedQuestionsStateModel>({
  name: 'SavedQuestions',
  defaults: SAVED_QUESTIONS_STATE
})
export class SavedQuestionsState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static savedQuestionList(state: any) {
    return state.savedQuestionList;
  }

  @Selector()
  static createMode(state: any) {
    return state.createMode;
  }

  @Selector()
  static editMode(state: any) {
    return state.editMode;
  }

  @Selector()
  static count(state: SavedQuestionsStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: SavedQuestionsStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: SavedQuestionsStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static pageIndex(state: SavedQuestionsStateModel): number {
    return state.pageIndex;
  }

  constructor(private savedQuestionsService: SavedQuestionsService) {
  }

  @Action(SavedQuestionsActions.LoadSavedQuestionList)
  loadSavedQuestionList(ctx: StateContext<SavedQuestionsStateModel>, {limit, offset}: SavedQuestionsActions.LoadSavedQuestionList) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.savedQuestionsService.getSavedQuestionsList(limit, offset).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          count: result.count,
          savedQuestionList: result['results'],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          savedQuestionList: [],
        }));
      })
    );
  }

  @Action(SavedQuestionsActions.CreateNewQuestion)
  createNewQuestion(ctx: StateContext<SavedQuestionsStateModel>, {questionData}: SavedQuestionsActions.CreateNewQuestion) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.savedQuestionsService.createNewQuestionInSaved(questionData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully created new question.',
          delay: 3000,
          type: SnackBarMessageType.SUCCESS,
        }));
        state = ctx.getState();
        const limit = state.pageSize;
        const offset = state.pageIndex * state.pageSize;
        ctx.dispatch(new SavedQuestionsActions.LoadSavedQuestionList(limit, offset));
        return ctx.dispatch(new SavedQuestionsActions.SetCreationMode(false));
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

  @Action(SavedQuestionsActions.UpdateSavedQuestion)
  updateSavedQuestion(ctx: StateContext<SavedQuestionsStateModel>, {questionData}: SavedQuestionsActions.UpdateSavedQuestion) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.savedQuestionsService.updateSavedQuestion(questionData.id, questionData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully updated the question.',
          delay: 3000,
          type: SnackBarMessageType.SUCCESS,
        }));
        ctx.dispatch(new SavedQuestionsActions.SetEditMode(SAVED_QUESTIONS_STATE.editMode));
        state = ctx.getState();
        const limit = state.pageSize;
        const offset = state.pageIndex * state.pageSize;
        ctx.dispatch(new SavedQuestionsActions.LoadSavedQuestionList(limit, offset));
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

  @Action(SavedQuestionsActions.DeleteSavedQuestion)
  deleteSavedQuestion(ctx: StateContext<SavedQuestionsStateModel>, {questionId}: SavedQuestionsActions.DeleteSavedQuestion) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.savedQuestionsService.deleteSavedQuestion(questionId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully deleted the question.',
          delay: 3000,
          type: SnackBarMessageType.SUCCESS,
        }));
        state = ctx.getState();
        const limit = state.pageSize;
        const offset = state.pageIndex * state.pageSize;
        ctx.dispatch(new SavedQuestionsActions.LoadSavedQuestionList(limit, offset));
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

  @Action(SavedQuestionsActions.SetCreationMode)
  setCreationMode(ctx: StateContext<SavedQuestionsStateModel>, {value}: SavedQuestionsActions.SetCreationMode) {
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
      createMode: value,
    });
  }

  @Action(SavedQuestionsActions.SetEditMode)
  setEditMode(ctx: StateContext<SavedQuestionsStateModel>, {value}: SavedQuestionsActions.SetEditMode) {
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
      editMode: value,
    });
  }

  @Action(SavedQuestionsActions.ChangePagination)
  changePagination(ctx: StateContext<SavedQuestionsStateModel>,
                   {paginatedData}: ViewCompanyListPageActions.ChangePagination) {
    const limit = paginatedData.pageSize;
    const offset = paginatedData.pageIndex * paginatedData.pageSize;
    const state = ctx.getState();
    ctx.setState({
      ...state,
      pageIndex: paginatedData.pageIndex,
    });
    return ctx.dispatch(new SavedQuestionsActions.LoadSavedQuestionList(limit, offset));
  }
}
