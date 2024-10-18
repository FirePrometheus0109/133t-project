import { Action, Selector, State } from '@ngxs/store';
import { saveAs } from 'file-saver';
import * as moment from 'moment';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { JobService } from '../../company/services/job.service';
import { FilterHelper } from '../../shared/helpers/filter.helper';
import { GridViewHelper } from '../../shared/helpers/grid-view.helper';
import { CityModel } from '../../shared/models';
import { Filter, SortingFilter, UpdateParamTypes } from '../../shared/models/filters.model';
import { DEFAULT_PAGINATED_OPTIONS, PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { ViewCandidateListPageActions } from '../actions';
import { CandidateItem, CandidateStatus } from '../models/candidate-item.model';
import { CandidateListMode } from '../models/candidate-parametr.model';
import { CandidateService } from '../services/candidate.service';


export class ViewCandidatesListStateModel extends BasePaginatedPageStateModel {
  results: Array<CandidateItem>;
  candidateSortingFilter: SortingFilter[];
  mode: CandidateListMode;
  showFilter: boolean;
  selectedFilters: Array<Filter>;
  currentSortingField: object;
  citySearchResult: Array<CityModel>;
  userId: number;
  initStatus: CandidateStatus;
  params: object;
}


export const DEFAULT_VIEW_CANDIDATE_LIST_PAGE_STATE = Object.assign({
  candidateSortingFilter: [
    {value: 'applied_date', viewValue: 'Applied Data'},
    {value: 'job_seeker__user__first_name', viewValue: 'First Name'},
    {value: 'job_seeker__user__last_name', viewValue: 'Last Name'},
    {value: 'job__title', viewValue: 'Job Post Title'},
  ],
  showFilter: false,
  mode: CandidateListMode.ALL_CANDIDATE,
  selectedFilters: [],
  currentSortingField: null,
  citySearchResult: [],
  userId: null,
  initStatus: null,
  params: {}
}, DEFAULT_PAGINATED_STATE);


@State<ViewCandidatesListStateModel>({
  name: 'ViewCandidatesListPageState',
  defaults: DEFAULT_VIEW_CANDIDATE_LIST_PAGE_STATE,
})
export class ViewCandidatesListPageState extends BaseBlockablePageState {

  @Selector()
  static count(state: ViewCandidatesListStateModel): number {
    return state.count;
  }

  @Selector()
  static showFilter(state: ViewCandidatesListStateModel): boolean {
    return state.showFilter;
  }

  @Selector()
  static selectedFilters(state: ViewCandidatesListStateModel): Array<Filter> {
    return state.selectedFilters;
  }

  @Selector()
  static pageSize(state: ViewCandidatesListStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageIndex(state: ViewCandidatesListStateModel): number {
    return state.pageIndex;
  }

  @Selector()
  static pageSizeOptions(state: ViewCandidatesListStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: ViewCandidatesListStateModel): Array<CandidateItem> {
    return state.results;
  }

  @Selector()
  static candidateSortingFilter(state: ViewCandidatesListStateModel): SortingFilter[] {
    return state.candidateSortingFilter;
  }

  @Selector()
  static citySearchResult(state: ViewCandidatesListStateModel): CityModel[] {
    return state.citySearchResult;
  }

  @Selector()
  static currentSortingField(state: ViewCandidatesListStateModel): object {
    return state.currentSortingField;
  }

  @Selector()
  static mode(state: ViewCandidatesListStateModel): CandidateListMode {
    return state.mode;
  }

  @Selector()
  static userId(state: ViewCandidatesListStateModel): number {
    return state.userId;
  }

  @Selector()
  static params(state: ViewCandidatesListStateModel): object {
    return state.params;
  }

  constructor(private service: CandidateService,
              private jobService: JobService) {
    super();
  }

  @Action(ViewCandidateListPageActions.InitCandidateList)
  initCandidateList(ctx, {mode, userId}: ViewCandidateListPageActions.InitCandidateList) {
    const state = ctx.getState();
    ctx.setState({
      ...DEFAULT_VIEW_CANDIDATE_LIST_PAGE_STATE,
      showFilter: false,
      selectedFilters: [],
      currentSortingField: null,
      citySearchResult: [],
      mode: mode,
      userId: userId,
      initStatus: null,
      params: state.initStatus ? {status: state.initStatus.id} : {}
    });
    return ctx.dispatch(new ViewCandidateListPageActions.LoadCandidateData(ctx.getState().params));
  }

  @Action(ViewCandidateListPageActions.InitJobCandidateList)
  initJobCandidateList(ctx, {status}: ViewCandidateListPageActions.InitJobCandidateList) {
    const state = ctx.getState();
    const preparedParams = status
      ? {
        ...state.params,
        status: status.id
      }
      : GridViewHelper.clearStateParams(state.params, ['status']);

    ctx.patchState({
      initStatus: status,
      params: preparedParams
    });

    return ctx.dispatch(new ViewCandidateListPageActions.LoadCandidateData(ctx.getState().params));
  }

  @Action(ViewCandidateListPageActions.LoadCandidateData)
  loadCandidatesData(ctx, {params}: ViewCandidateListPageActions.LoadCandidateData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    const action = state.mode === CandidateListMode.ALL_CANDIDATE ?
      this.service.getCandidateList.bind(this.service) :
      this.jobService.getCandidates.bind(this.jobService, state.userId);

    return action(params).pipe(
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

  @Action(ViewCandidateListPageActions.ToggleFilterList)
  toggleFilterList(ctx) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      showFilter: !state.showFilter
    });
  }

  @Action(ViewCandidateListPageActions.ChangeSelectedFilters)
  changeSelectedFilters(ctx, {filter}: ViewCandidateListPageActions.ChangeSelectedFilters) {
    let state = ctx.getState();
    const newFilters = FilterHelper.getUpdatedFilterValue(state.selectedFilters, filter);
    const updatedParams = GridViewHelper.updateParamsWithEmptyFilter(state.params, filter);
    ctx.setState({
      ...state,
      selectedFilters: newFilters,
      params: GridViewHelper.getParamsWitFilterValue(updatedParams, newFilters)
    });
    state = ctx.getState();
    return ctx.dispatch(new ViewCandidateListPageActions.LoadCandidateData(state.params));
  }

  @Action(ViewCandidateListPageActions.RemoveSelectedFilter)
  removeSelectedFilter(ctx, {filter}: ViewCandidateListPageActions.RemoveSelectedFilter) {
    let state = ctx.getState();
    const newFilters = FilterHelper.removeFilter(state.selectedFilters, filter);
    ctx.setState({
      ...state,
      selectedFilters: newFilters,
      params: GridViewHelper.getParamsWitFilterValue(state.params, newFilters, filter)
    });
    state = ctx.getState();
    return ctx.dispatch(new ViewCandidateListPageActions.LoadCandidateData(state.params));
  }

  @Action(ViewCandidateListPageActions.SetCurrentSortingField)
  setCurrentSortingField(ctx, {params}: ViewCandidateListPageActions.SetCurrentSortingField) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      currentSortingField: params
    });
  }

  @Action(ViewCandidateListPageActions.SetCurrentPagination)
  setCurrentPagination(ctx, {params}: ViewCandidateListPageActions.SetCurrentPagination) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      ...params
    });
  }

  @Action(ViewCandidateListPageActions.ClearFilters)
  clearFilters(ctx, {}) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      selectedFilters: [],
      params: {}
    });
    state = ctx.getState();
    return ctx.dispatch(new ViewCandidateListPageActions.LoadCandidateData(state.params));
  }

  @Action(ViewCandidateListPageActions.DownloadCandidatesToCSV)
  downloadCandidatesToCSV(ctx, {selectedCandidates}: ViewCandidateListPageActions.DownloadCandidatesToCSV) {
    ctx.patchState({
      status: 'pending',
    });
    return this.service.downloadCandidatesList(selectedCandidates).pipe(
      tap((responseBlob: Blob) => {
        const file = new File([responseBlob], `Candidates_${moment().format('L')}.csv`, {type: 'text/csv'});
        saveAs(file);
        return ctx.patchState({
          status: 'done',
          errors: null,
        });
      }),
      catchError(error => {
        return of(ctx.patchState({
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(ViewCandidateListPageActions.UpdateParams)
  updateParams(ctx, {params, changeType}: ViewCandidateListPageActions.UpdateParams) {
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
    return ctx.dispatch(new ViewCandidateListPageActions.LoadCandidateData(state.params));
  }
}
