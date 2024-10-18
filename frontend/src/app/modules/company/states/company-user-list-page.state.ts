import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { CompanyUserListPageActions } from '../actions';
import { CompanyUser } from '../models/company-user.model';
import { CompanyUserService } from '../services/company-user.service';


class CompanyUserListPageStateModel extends BasePaginatedPageStateModel {
  results: object[];
  companyUsers: Array<CompanyUser>;
}


export const DEFAULT_COMPANY_USER_LIST_PAGE_STATE = Object.assign({
  companyUsers: [],
}, DEFAULT_PAGINATED_STATE);


@State<CompanyUserListPageStateModel>({
  name: 'CompanyUserListPageState',
  defaults: DEFAULT_COMPANY_USER_LIST_PAGE_STATE,
})
export class CompanyUserListPageState extends BaseBlockablePageState {
  @Selector()
  static count(state: CompanyUserListPageStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: CompanyUserListPageStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: CompanyUserListPageStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: CompanyUserListPageStateModel): Array<any> {
    return state.results;
  }

  @Selector()
  static companyUserList(state: CompanyUserListPageStateModel): Array<CompanyUser> {
    return state.companyUsers;
  }

  constructor(private companyUserService: CompanyUserService) {
    super();
  }

  @Action(CompanyUserListPageActions.LoadCompanyUsersData)
  loadCompanyUsersData(ctx: StateContext<CompanyUserListPageStateModel>, {params}: CompanyUserListPageActions.LoadCompanyUsersData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.getCompanyUsers(params).pipe(
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
          companyUsers: result.results,
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

  @Action(CompanyUserListPageActions.DeleteCompanyUser)
  deleteCompanyUser(ctx: StateContext<CompanyUserListPageStateModel>,
                    {companyUserId}: CompanyUserListPageActions.DeleteCompanyUser) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.deleteCompanyUser(companyUserId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done'
        });
        ctx.dispatch(new CompanyUserListPageActions.LoadCompanyUsersData([{}, state.pageSize, state.pageIndex]));
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

  @Action(CompanyUserListPageActions.ChangePagination)
  changePagination(ctx: StateContext<CompanyUserListPageStateModel>,
                   {params}: CompanyUserListPageActions.ChangePagination) {
    return ctx.dispatch(new CompanyUserListPageActions.LoadCompanyUsersData(params));
  }
}
