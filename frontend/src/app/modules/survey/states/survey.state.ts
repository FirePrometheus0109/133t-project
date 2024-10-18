import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { SurveyListActions } from '../actions';
import { Question } from '../models/question.model';
import { Survey } from '../models/survey.model';
import { SurveyService } from '../services/survey.service';


class SurveyStateModel extends BasePaginatedPageStateModel {
  createMode: boolean;
  editMode: boolean;
  viewMode: boolean;
  jobEditMode: boolean;
  modalMode: boolean;
  currentSurvey: Survey;
  surveyForJobEdit: any;
  surveyList: Array<Survey>;
  searchTitle: string;
}


export const SURVEY_STATE = {
  ...DEFAULT_PAGINATED_STATE,
  createMode: false,
  editMode: false,
  viewMode: false,
  jobEditMode: false,
  modalMode: false,
  currentSurvey: null,
  searchTitle: '',
  surveyForJobEdit: {
    questions: []
  },
  surveyList: [],
};


@State<SurveyStateModel>({
  name: 'Survey',
  defaults: SURVEY_STATE
})
export class SurveyState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static surveyList(state: any): Array<Survey> {
    return state.surveyList;
  }

  @Selector()
  static createMode(state: SurveyStateModel): boolean {
    return state.createMode;
  }

  @Selector()
  static viewMode(state: SurveyStateModel): boolean {
    return state.viewMode;
  }

  @Selector()
  static editMode(state: SurveyStateModel): boolean {
    return state.editMode;
  }

  @Selector()
  static jobEditMode(state: SurveyStateModel): boolean {
    return state.jobEditMode;
  }

  @Selector()
  static modalMode(state: SurveyStateModel): boolean {
    return state.modalMode;
  }

  @Selector()
  static count(state: SurveyStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: SurveyStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: SurveyStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static pageIndex(state: SurveyStateModel): number {
    return state.pageIndex;
  }

  @Selector()
  static currentSurvey(state: SurveyStateModel): Survey {
    return state.currentSurvey;
  }

  @Selector()
  static surveyForJobEdit(state: SurveyStateModel): Survey {
    return state.surveyForJobEdit;
  }

  @Selector()
  static questionsCountInSurvey(state: SurveyStateModel): number {
    if (state.jobEditMode) {
      return state.surveyForJobEdit.questions.length;
    } else {
      return state.currentSurvey.questions.length;
    }
  }

  constructor(private surveyService: SurveyService) {
  }

  @Action(SurveyListActions.LoadSurveyList)
  loadSurveyList(ctx: StateContext<SurveyStateModel>, {limit, offset, search}: SurveyListActions.LoadSurveyList) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.getSurveyList(limit, offset, search).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          count: result.count,
          surveyList: result['results'],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          surveyList: [],
        }));
      })
    );
  }

  @Action(SurveyListActions.UpdateSurveyList)
  updateSurveyList(ctx: StateContext<SurveyStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    const limit = state.pageSize;
    const offset = state.pageIndex * state.pageSize;
    return this.surveyService.getSurveyList(limit, offset).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          count: result.count,
          surveyList: result['results'],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          surveyList: [],
        }));
      })
    );
  }

  @Action(SurveyListActions.UpdateSurveyForJobEdit)
  updateSurveyForJobEdit(ctx: StateContext<SurveyStateModel>, {questions}: SurveyListActions.UpdateSurveyForJobEdit) {
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
      surveyForJobEdit: {questions: questions}
    });
  }

  @Action(SurveyListActions.UpdateQuestionInSurveyForJobEdit)
  updateQuestionInSurveyForJobEdit(ctx: StateContext<SurveyStateModel>,
                                   {updatedQuestionData}: SurveyListActions.UpdateQuestionInSurveyForJobEdit) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    const currentQuestions = ctx.getState().surveyForJobEdit.questions;
    currentQuestions[currentQuestions
      .findIndex((question: Question) => question.id === updatedQuestionData.id)] = updatedQuestionData;
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      surveyForJobEdit: {questions: currentQuestions}
    });
  }

  @Action(SurveyListActions.DeleteQuestionFromSurveyForJobEdit)
  deleteQuestionFromSurveyForJobEdit(ctx: StateContext<SurveyStateModel>,
                                     {questionId}: SurveyListActions.DeleteQuestionFromSurveyForJobEdit) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    const currentQuestions = ctx.getState().surveyForJobEdit.questions;
    const indexToDelete = currentQuestions.findIndex((question: Question) => question.id === questionId);
    currentQuestions.splice(indexToDelete, 1);
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      surveyForJobEdit: {questions: currentQuestions}
    });
  }

  @Action(SurveyListActions.SearchSurvey)
  SearchSurvey(ctx: StateContext<SurveyStateModel>, {searchTitle}: SurveyListActions.SearchSurvey) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      searchTitle: searchTitle
    });
    state = ctx.getState();
    const limit = state.pageSize;
    const offset = state.pageIndex * state.pageSize;
    return ctx.dispatch(new SurveyListActions.LoadSurveyList(limit, offset, searchTitle));
  }

  @Action(SurveyListActions.SetCreationMode)
  setCreationMode(ctx: StateContext<SurveyStateModel>, {value}: SurveyListActions.SetCreationMode) {
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
      viewMode: false,
      editMode: false,
      createMode: value,
    });
  }

  @Action(SurveyListActions.SetEditMode)
  setEditMode(ctx: StateContext<SurveyStateModel>, {value}: SurveyListActions.SetEditMode) {
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
      createMode: false,
      viewMode: false,
      editMode: value,
    });
  }

  @Action(SurveyListActions.SetViewMode)
  setViewMode(ctx: StateContext<SurveyStateModel>, {value}: SurveyListActions.SetViewMode) {
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
      createMode: false,
      editMode: false,
      viewMode: value,
    });
  }

  @Action(SurveyListActions.SetJobEditMode)
  setJobEditMode(ctx: StateContext<SurveyStateModel>, {value}: SurveyListActions.SetJobEditMode) {
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
      jobEditMode: value,
    });
  }

  @Action(SurveyListActions.SetModalMode)
  setModalMode(ctx: StateContext<SurveyStateModel>, {value}: SurveyListActions.SetModalMode) {
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
      modalMode: value,
    });
  }

  @Action(SurveyListActions.SetCurrentSurvey)
  setCurrentSurvey(ctx: StateContext<SurveyStateModel>, {survey}: SurveyListActions.SetCurrentSurvey) {
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
      currentSurvey: survey,
    });
  }

  @Action(SurveyListActions.UpdateCurrentSurvey)
  updateCurrentSurvey(ctx: StateContext<SurveyStateModel>, {surveyId}: SurveyListActions.UpdateCurrentSurvey) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.surveyService.getSurvey(surveyId).pipe(
      tap((survey: Survey) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          currentSurvey: survey,
        });
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

  @Action(SurveyListActions.ChangePagination)
  changePagination(ctx: StateContext<SurveyStateModel>,
                   {paginatedData}: SurveyListActions.ChangePagination) {
    const limit = paginatedData.pageSize;
    const offset = paginatedData.pageIndex * paginatedData.pageSize;
    const state = ctx.getState();
    const searchTitle = state.searchTitle || '';
    ctx.setState({
      ...state,
      pageIndex: paginatedData.pageIndex,
    });
    return ctx.dispatch(new SurveyListActions.LoadSurveyList(limit, offset, searchTitle));
  }
}
