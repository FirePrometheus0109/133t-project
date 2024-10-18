import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, debounceTime, tap } from 'rxjs/operators';
import { CoreActions } from '../../core/actions';
import { FilterHelper } from '../../shared/helpers/filter.helper';
import { GridViewHelper } from '../../shared/helpers/grid-view.helper';
import { Filter, SortingFilter, UpdateParamTypes } from '../../shared/models/filters.model';
import { DEFAULT_PAGINATED_OPTIONS, PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { ViewJobSeekerListPageActions } from '../actions';
import { JobSeekerProfile } from '../models';
import { JobSeekerListMode } from '../models/job-seeker-list-fitlers.model';
import { JobSeekerService } from '../services';

import { environment } from '../../../../environments/environment';


export class ViewJobSeekerListStateModel extends BasePaginatedPageStateModel {
  results: Array<JobSeekerProfile>;
  sortingFilter: SortingFilter[];
  showFilter: boolean;
  selectedFilters: Array<Filter>;
  globalFilters: Array<Filter>;
  mode: JobSeekerListMode;
}


export const DEFAULT_VIEW_JOB_SEEKER_LIST_PAGE_STATE = Object.assign({
  sortingFilter: [
    {value: 'first_name', viewValue: 'By First Name'},
    {value: 'last_name', viewValue: 'By Last Name'},
    {value: 'modified_at', viewValue: 'By Date'}
  ],
  showFilter: false,
  selectedFilters: [],
  globalFilters: [],
  mode: JobSeekerListMode.ALL,
}, DEFAULT_PAGINATED_STATE);


@State<ViewJobSeekerListStateModel>({
  name: 'ViewJobSeekerListState',
  defaults: DEFAULT_VIEW_JOB_SEEKER_LIST_PAGE_STATE
})
export class ViewJobSeekerListState extends BaseBlockablePageState {

  @Selector()
  static count(state: ViewJobSeekerListStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: ViewJobSeekerListStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageIndex(state: ViewJobSeekerListStateModel): number {
    return state.pageIndex;
  }

  @Selector()
  static pageSizeOptions(state: ViewJobSeekerListStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: ViewJobSeekerListStateModel): Array<JobSeekerProfile> {
    return state.results;
  }

  @Selector()
  static sortingFilter(state: ViewJobSeekerListStateModel): SortingFilter[] {
    return state.sortingFilter;
  }

  @Selector()
  static showFilter(state: ViewJobSeekerListStateModel): boolean {
    return state.showFilter;
  }

  @Selector()
  static selectedFilters(state: ViewJobSeekerListStateModel): Array<Filter> {
    return state.selectedFilters;
  }

  @Selector()
  static mode(state: ViewJobSeekerListStateModel): JobSeekerListMode {
    return state.mode;
  }

  constructor(private service: JobSeekerService) {
    super();
  }

  @Action(ViewJobSeekerListPageActions.InitJobSeekerList)
  initJobSeekerList(ctx, {mode, params}: ViewJobSeekerListPageActions.InitJobSeekerList) {
    const state = ctx.getState();
    ctx.setState({
        ...DEFAULT_VIEW_JOB_SEEKER_LIST_PAGE_STATE,
        showFilter: false,
        selectedFilters: state.globalFilters,
        params: params,
        mode: mode,
      }
    );
    return ctx.dispatch(new ViewJobSeekerListPageActions.LoadJobSeekerData(params));
  }

  @Action(ViewJobSeekerListPageActions.LoadJobSeekerData)
  loadJobSeekerData(ctx, {params}: ViewJobSeekerListPageActions.LoadJobSeekerData) {
    let state: ViewJobSeekerListStateModel = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    ctx.dispatch(new CoreActions.ShowGlobalLoader());

    let action;
    switch (state.mode) {
      case JobSeekerListMode.ALL:
        action = this.service.getJobSeekerList.bind(this.service);
        break;
      case JobSeekerListMode.PURCHASED:
        action = this.service.getJobSeekerPurchasedList.bind(this.service);
        break;
      case JobSeekerListMode.SAVED:
        action = this.service.getJobSeekerSavedList.bind(this.service);
        break;
      default:
        action = this.service.getJobSeekerList.bind(this.service);
        break;
    }

    return action(params).pipe(
      debounceTime(environment.searchDebounceTime),
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

  @Action(ViewJobSeekerListPageActions.ToggleFilterList)
  toggleFilterList(ctx) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      showFilter: !state.showFilter
    });
  }

  @Action(ViewJobSeekerListPageActions.ClearFilters)
  clearFilters(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      selectedFilters: [],
      params: {}
    });
    state = ctx.getState();
    return ctx.dispatch(new ViewJobSeekerListPageActions.LoadJobSeekerData(state.params));
  }

  @Action(ViewJobSeekerListPageActions.ChangeSelectedFilters)
  changeSelectedFilters(ctx, {filter}: ViewJobSeekerListPageActions.ChangeSelectedFilters) {
    let state = ctx.getState();
    const newFilters = FilterHelper.getUpdatedFilterValue(state.selectedFilters, filter);
    const updatedParams = GridViewHelper.updateParamsWithEmptyFilter(state.params, filter);
    ctx.setState({
      ...state,
      selectedFilters: newFilters,
      params: GridViewHelper.getParamsWitFilterValue(updatedParams, newFilters)
    });
    state = ctx.getState();
    return ctx.dispatch(new ViewJobSeekerListPageActions.LoadJobSeekerData(state.params));
  }

  @Action(ViewJobSeekerListPageActions.RemoveSelectedFilter)
  removeSelectedFilter(ctx, {filter}: ViewJobSeekerListPageActions.RemoveSelectedFilter) {
    let state = ctx.getState();
    const newFilters = FilterHelper.removeFilter(state.selectedFilters, filter);
    ctx.setState({
      ...state,
      selectedFilters: newFilters,
      params: GridViewHelper.getParamsWitFilterValue(state.params, newFilters, filter)
    });
    state = ctx.getState();
    return ctx.dispatch(new ViewJobSeekerListPageActions.LoadJobSeekerData(state.params));
  }

  @Action(ViewJobSeekerListPageActions.UpdateParams)
  updateParams(ctx, {params, changeType}: ViewJobSeekerListPageActions.UpdateParams) {
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
    return ctx.dispatch(new ViewJobSeekerListPageActions.LoadJobSeekerData(state.params));
  }

  @Action(ViewJobSeekerListPageActions.SetGlobalFilterOnInit)
  setGlobalFilterOnInit(ctx, {filter}: ViewJobSeekerListPageActions.SetGlobalFilterOnInit) {
    const state = ctx.getState();
    const newFilters = FilterHelper.getUpdatedFilterValue([], filter);
    return ctx.setState({
      ...state,
      globalFilters: newFilters
    });
  }
}
