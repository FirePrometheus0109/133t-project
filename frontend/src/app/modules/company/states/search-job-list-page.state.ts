import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { FilterHelper } from '../../shared/helpers/filter.helper';
import { GridViewHelper } from '../../shared/helpers/grid-view.helper';
import { Filter, SortingFilter, UpdateParamTypes } from '../../shared/models/filters.model';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { PublicApiService } from '../../shared/services/public-api.service';
import {
  BasePaginatedPageStateModel,
  DEFAULT_PAGINATED_STATE,
} from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { SearchJobListPageActions } from '../actions';
import { CompanySelectionType } from '../models/jobs-list-filters.model';
import { PublicCompanyItem } from '../models/public-company.model';
import { JobService } from '../services/job.service';


class SearchJobListPageStateModel extends BasePaginatedPageStateModel {
  results: object[];
  jobSortingFilter: SortingFilter[];
  showFilter: boolean;
  selectedFilters: Array<Filter>;
  companiesInclude: PublicCompanyItem[];
  companiesIncludeSearch: string;
  companiesExclude: PublicCompanyItem[];
  companiesExcludeSearch: string;
  params: object;
}


export const DEFAULT_SEARCH_JOB_LIST_PAGE_STATE = Object.assign({
  jobSortingFilter: [
    {value: 'publish_date', viewValue: 'by Date'},
    {value: 'matching_percent', viewValue: 'by Match'},
    {value: 'rank', viewValue: 'by Relevance'},
  ],
  showFilter: false,
  selectedFilters: [],
  companiesInclude: [],
  companiesIncludeSearch: '',
  companiesExclude: [],
  companiesExcludeSearch: '',
  params: {}
}, DEFAULT_PAGINATED_STATE);


@State<SearchJobListPageStateModel>({
  name: 'SearchJobListPageState',
  defaults: DEFAULT_SEARCH_JOB_LIST_PAGE_STATE,
})
export class SearchJobListPageState extends BaseBlockablePageState {
  @Selector()
  static count(state: SearchJobListPageStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: SearchJobListPageStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: SearchJobListPageStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: SearchJobListPageStateModel): Array<any> {
    return state.results;
  }

  @Selector()
  static jobSortingFilters(state: SearchJobListPageStateModel): SortingFilter[] {
    return state.jobSortingFilter;
  }

  @Selector()
  static showFilter(state: SearchJobListPageStateModel): boolean {
    return state.showFilter;
  }

  @Selector()
  static selectedFilters(state: SearchJobListPageStateModel): Array<Filter> {
    return state.selectedFilters;
  }

  @Selector()
  static companiesInclude(state: SearchJobListPageStateModel): PublicCompanyItem[] {
    return state.companiesInclude;
  }

  @Selector()
  static companiesIncludeSearch(state: SearchJobListPageStateModel): string {
    return state.companiesIncludeSearch;
  }

  @Selector()
  static companiesExclude(state: SearchJobListPageStateModel): PublicCompanyItem[] {
    return state.companiesExclude;
  }

  @Selector()
  static companiesExcludeSearch(state: SearchJobListPageStateModel): string {
    return state.companiesExcludeSearch;
  }

  @Selector()
  static params(state: SearchJobListPageStateModel): object {
    return state.params;
  }

  constructor(private jobService: JobService,
              private publicService: PublicApiService) {
    super();
  }

  @Action(SearchJobListPageActions.LoadJobsData)
  loadJobsData(ctx: StateContext<SearchJobListPageStateModel>, {params}: SearchJobListPageActions.LoadJobsData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getJobs(params).pipe(
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

  @Action(SearchJobListPageActions.LoadCompanies)
  loadCompanies(ctx: StateContext<SearchJobListPageStateModel>,
                {search, companySelectionType}: SearchJobListPageActions.LoadCompanies) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.publicService.getCompaniesForFilter(search).pipe(
      tap((result: PublicCompanyItem[]) => {
        state = ctx.getState();
        const filterObj = {};
        filterObj[companySelectionType] = result;
        filterObj[`${companySelectionType}Search`] = search;
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          ...filterObj
        });
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

  @Action(SearchJobListPageActions.LoadCompaniesInclude)
  loadCompaniesInclude(ctx: StateContext<SearchJobListPageStateModel>,
                       {search}: SearchJobListPageActions.LoadCompaniesInclude) {
    return ctx.dispatch(new SearchJobListPageActions.LoadCompanies(search, CompanySelectionType.INCLUDE));
  }

  @Action(SearchJobListPageActions.LoadCompaniesExclude)
  loadCompaniesExclude(ctx: StateContext<SearchJobListPageStateModel>,
                       {search}: SearchJobListPageActions.LoadCompaniesExclude) {
    return ctx.dispatch(new SearchJobListPageActions.LoadCompanies(search, CompanySelectionType.EXCLUDE));
  }

  @Action(SearchJobListPageActions.ToggleFilterList)
  toggleFilterList(ctx) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      showFilter: !state.showFilter
    });
  }

  @Action(SearchJobListPageActions.ClearFilters)
  clearFilters(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      selectedFilters: [],
      params: {}
    });
    state = ctx.getState();
    return ctx.dispatch(new SearchJobListPageActions.LoadJobsData(state.params));
  }

  @Action(SearchJobListPageActions.ChangeSelectedFilters)
  changeSelectedFilters(ctx, {filter}: SearchJobListPageActions.ChangeSelectedFilters) {
    let state = ctx.getState();
    const newFilters = FilterHelper.getUpdatedFilterValue(state.selectedFilters, filter);
    const updatedParams = GridViewHelper.updateParamsWithEmptyFilter(state.params, filter);
    ctx.setState({
      ...state,
      selectedFilters: newFilters,
      params: GridViewHelper.getParamsWitFilterValue(updatedParams, newFilters)
    });
    state = ctx.getState();
    return ctx.dispatch(new SearchJobListPageActions.LoadJobsData(state.params));
  }

  @Action(SearchJobListPageActions.SetSelectedFiltersOnInit)
  setSelectedFiltersOnInit(ctx, {filter}: SearchJobListPageActions.SetSelectedFiltersOnInit) {
    const state = ctx.getState();
    const newFilters = FilterHelper.getUpdatedFilterValue([], filter);
    return ctx.setState({
      ...state,
      selectedFilters: newFilters
    });
  }

  @Action(SearchJobListPageActions.RemoveSelectedFilter)
  removeSelectedFilter(ctx, {filter}: SearchJobListPageActions.RemoveSelectedFilter) {
    let state = ctx.getState();
    const newFilters = FilterHelper.removeFilter(state.selectedFilters, filter);
    ctx.setState({
      ...state,
      selectedFilters: newFilters,
      params: GridViewHelper.getParamsWitFilterValue(state.params, newFilters, filter)
    });
    state = ctx.getState();
    return ctx.dispatch(new SearchJobListPageActions.LoadJobsData(state.params));
  }

  @Action(SearchJobListPageActions.UpdateParams)
  updateParams(ctx, {params, changeType}: SearchJobListPageActions.UpdateParams) {
    let state = ctx.getState();
    const newParams = GridViewHelper.prepareNewParams(params, changeType);
    ctx.setState({
      ...state,
      params: {
        ...state.params,
        ...newParams
      }
    });
    state = ctx.getState();
    return ctx.dispatch(new SearchJobListPageActions.LoadJobsData(state.params));
  }
}
