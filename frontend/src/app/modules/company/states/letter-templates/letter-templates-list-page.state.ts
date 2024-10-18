import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { SortingFilter } from '../../../shared/models/filters.model';
import { PaginatedData } from '../../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../../shared/states/base-paginated.state';
import { LetterTemplatesListActions } from '../../actions';
import { LetterTemplateItem } from '../../models/letter-templates.model';
import { CompanyLetterTemplatesService } from '../../services/company-letter-templates.service';


export class LetterTemplatesListStateModel extends BasePaginatedPageStateModel {
  status: string;
  errors: object;
  templatesSortingFilter: SortingFilter[];
  letterTemplatesList: LetterTemplateItem[];
  params: object;
}


export const DEFAULT_LETTER_TEMPLATES_LIST_STATE = Object.assign({
  status: '',
  errors: null,
  templatesSortingFilter: [
    {value: 'name', viewValue: 'Name'},
    {value: '-modified_at', viewValue: 'Modified date'},
  ],
  letterTemplatesList: [],
  params: {}
}, DEFAULT_PAGINATED_STATE);


@State<LetterTemplatesListStateModel>({
  name: 'LetterTemplatesListState',
  defaults: DEFAULT_LETTER_TEMPLATES_LIST_STATE
})
export class LetterTemplatesListState {
  @Selector()
  static letterTemplatesList(state: LetterTemplatesListStateModel): LetterTemplateItem[] {
    return state.letterTemplatesList;
  }

  @Selector()
  static count(state: LetterTemplatesListStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: LetterTemplatesListStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: LetterTemplatesListStateModel): number[] {
    return state.pageSizeOptions;
  }

  @Selector()
  static params(state: LetterTemplatesListStateModel): object {
    return state.params;
  }

  @Selector()
  static templatesSortingFilter(state: LetterTemplatesListStateModel): SortingFilter[] {
    return state.templatesSortingFilter;
  }

  constructor(private letterTemplatesService: CompanyLetterTemplatesService) {
  }

  @Action(LetterTemplatesListActions.UpdateListParams)
  updateListParams(ctx: StateContext<LetterTemplatesListStateModel>,
                   {params}: LetterTemplatesListActions.UpdateListParams) {
    let state = ctx.getState();
    const updatedParams = Object.assign(state.params, params);
    for (const [key, value] of Object.entries(updatedParams)) {
      if (!value) {
        delete updatedParams[key];
      }
    }
    ctx.setState({
      ...state,
      pageSize: params['limit'],
      params: updatedParams
    });
    state = ctx.getState();
    return ctx.dispatch(new LetterTemplatesListActions.GetLetterTemplatesList(state.params));
  }

  @Action(LetterTemplatesListActions.GetLetterTemplatesList)
  getLetterTemplatesList(ctx: StateContext<LetterTemplatesListStateModel>,
                         {params}: LetterTemplatesListActions.GetLetterTemplatesList) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.letterTemplatesService.getLetterTemplates(params).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          letterTemplatesList: result.results,
          count: result.count
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          letterTemplatesList: [],
        }));
      }),
    );
  }

  @Action(LetterTemplatesListActions.DeleteLetterTemplate)
  deleteLetterTemplate(ctx: StateContext<LetterTemplatesListStateModel>,
                       {letterTemplateId}: LetterTemplatesListActions.DeleteLetterTemplate) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.letterTemplatesService.deleteLetterTemplate(letterTemplateId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null
        });
        return ctx.dispatch(new LetterTemplatesListActions.GetLetterTemplatesList(state.params));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error
        }));
      }),
    );
  }
}
