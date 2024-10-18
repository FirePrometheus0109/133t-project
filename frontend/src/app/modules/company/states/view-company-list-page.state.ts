import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { PublicApiService } from '../../shared/services/public-api.service';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { ViewCompanyListPageActions } from '../actions';
import { PublicCompanyItem } from '../models/public-company.model';


class ViewCompanyListPageStateModel extends BasePaginatedPageStateModel {
  results: Array<PublicCompanyItem>;
}


export const DEFAULT_COMPANY_PROFILE_PAGE_STATE = DEFAULT_PAGINATED_STATE;


@State<ViewCompanyListPageStateModel>({
  name: 'ViewCompanyListPage',
  defaults: DEFAULT_COMPANY_PROFILE_PAGE_STATE,
})
export class ViewCompanyListPageState {
  @Selector()
  static count(state: ViewCompanyListPageStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: ViewCompanyListPageStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: ViewCompanyListPageStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: ViewCompanyListPageStateModel): Array<PublicCompanyItem> {
    return state.results;
  }

  constructor(private publicApiService: PublicApiService) {
  }

  @Action(ViewCompanyListPageActions.LoadCompaniesData)
  loadCompaniesData(ctx: StateContext<ViewCompanyListPageStateModel>,
                    {limit, offset}: ViewCompanyListPageActions.LoadCompaniesData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.publicApiService.getCompanies(limit, offset).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          count: result.count,
          next: result.next,
          previous: result.previous,
          results: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          count: 0,
          next: null,
          previous: null,
          results: [],
        }));
      }),
    );
  }

  @Action(ViewCompanyListPageActions.ChangePagination)
  changePagination(ctx: StateContext<ViewCompanyListPageStateModel>,
                   {paginatedData}: ViewCompanyListPageActions.ChangePagination) {
    const limit = paginatedData.pageSize;
    const offset = paginatedData.pageIndex * paginatedData.pageSize;
    return ctx.dispatch(new ViewCompanyListPageActions.LoadCompaniesData(limit, offset));
  }
}
