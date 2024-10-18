import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CoreActions } from '../../../core/actions';
import { NavigationService } from '../../../core/services/navigation.service';
import { SnackBarMessageType } from '../../../shared/models/snack-bar-message';
import { LetterTemplateManageActions } from '../../actions';
import { LetterTemplateEventType, LetterTemplateItem } from '../../models/letter-templates.model';
import { CompanyLetterTemplatesService } from '../../services/company-letter-templates.service';


export class LetterTemplateManagePageStateModel {
  status: string;
  errors: object;
  createMode: boolean;
  editMode: boolean;
  viewMode: boolean;
  letterTemplateEventTypes: LetterTemplateEventType[];
  currentLetterTemplate: LetterTemplateItem;
}


export const DEFAULT_LETTER_TEMPLATE_MANAGE_PAGE_STATE = {
  status: '',
  errors: null,
  createMode: false,
  editMode: false,
  viewMode: false,
  letterTemplateEventTypes: [],
  currentLetterTemplate: null,
};


@State<LetterTemplateManagePageStateModel>({
  name: 'LetterTemplateManagePageState',
  defaults: DEFAULT_LETTER_TEMPLATE_MANAGE_PAGE_STATE,
})
export class LetterTemplateManagePageState {
  @Selector()
  static createMode(state: LetterTemplateManagePageStateModel): boolean {
    return state.createMode;
  }

  @Selector()
  static editMode(state: LetterTemplateManagePageStateModel): boolean {
    return state.editMode;
  }

  @Selector()
  static viewMode(state: LetterTemplateManagePageStateModel): boolean {
    return state.viewMode;
  }

  @Selector()
  static letterTemplateEventTypes(state: LetterTemplateManagePageStateModel) {
    return state.letterTemplateEventTypes;
  }

  @Selector()
  static currentLetterTemplate(state: LetterTemplateManagePageStateModel) {
    return state.currentLetterTemplate;
  }

  @Selector()
  static errors(state: LetterTemplateManagePageStateModel) {
    return state.errors;
  }

  constructor(private companyLetterTemplatesService: CompanyLetterTemplatesService,
              private navigationService: NavigationService) {
  }

  @Action(LetterTemplateManageActions.LoadLetterTemplatesEventTypes)
  loadLetterTemplatesEventTypes(ctx: StateContext<LetterTemplateManagePageStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyLetterTemplatesService.getLetterTemplatesEventTypes().pipe(
      tap((result: LetterTemplateEventType[]) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          letterTemplateEventTypes: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          letterTemplateEventTypes: [],
        }));
      }),
    );
  }

  @Action(LetterTemplateManageActions.SetCreateMode)
  setCreateMode(ctx: StateContext<LetterTemplateManagePageStateModel>,
                {value}: LetterTemplateManageActions.SetCreateMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      createMode: value,
      editMode: false,
      viewMode: false,
    });
  }

  @Action(LetterTemplateManageActions.SetViewMode)
  setViewMode(ctx: StateContext<LetterTemplateManagePageStateModel>,
              {value}: LetterTemplateManageActions.SetViewMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
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

  @Action(LetterTemplateManageActions.SetEditMode)
  setEditMode(ctx: StateContext<LetterTemplateManagePageStateModel>,
              {value}: LetterTemplateManageActions.SetEditMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      createMode: false,
      editMode: value,
      viewMode: false,
    });
  }

  @Action(LetterTemplateManageActions.CreateLetterTemplate)
  createLetterTemplate(ctx: StateContext<LetterTemplateManagePageStateModel>,
                       {letterTemplate}: LetterTemplateManageActions.CreateLetterTemplate) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyLetterTemplatesService.createNewLetterTemplate(letterTemplate).pipe(
      tap((result: any) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null
        });
        this.navigationService.goToLetterTemplatesListPage();
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: `Letter template ${result.name} created`,
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
      }),
    );
  }

  @Action(LetterTemplateManageActions.LoadLetterTemplateData)
  loadLetterTemplateData(ctx: StateContext<LetterTemplateManagePageStateModel>,
                         {letterTemplateId}: LetterTemplateManageActions.LoadLetterTemplateData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyLetterTemplatesService.getLetterTemplateData(letterTemplateId).pipe(
      tap((result: LetterTemplateItem) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          currentLetterTemplate: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          currentLetterTemplate: null,
        }));
      }),
    );
  }

  @Action(LetterTemplateManageActions.ResetCurrentLetterTemplate)
  resetCurrentLetterTemplate(ctx: StateContext<LetterTemplateManagePageStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      currentLetterTemplate: new LetterTemplateItem()
    });
  }

  @Action(LetterTemplateManageActions.SaveLetterTemplate)
  saveLetterTemplate(ctx: StateContext<LetterTemplateManagePageStateModel>,
                     {letterTemplateId, letterTemplate}: LetterTemplateManageActions.SaveLetterTemplate) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyLetterTemplatesService.saveLetterTemplate(letterTemplateId, letterTemplate).pipe(
      tap((result: any) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null
        });
        this.navigationService.goToLetterTemplatesListPage();
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: result.detail || 'Done',
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
      }),
    );
  }
}
