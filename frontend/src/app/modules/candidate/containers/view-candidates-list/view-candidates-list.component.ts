import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialog, MatSelectChange, PageEvent } from '@angular/material';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { environment } from '../../../../../environments/environment';
import { CommentsActions } from '../../../common-components/actions';
import { CommentsComponent } from '../../../common-components/containers/comments.container';
import { CommentType } from '../../../common-components/models/comment.model';
import { ViewJobDetailsJsPageState } from '../../../company/states/view-job-details-js-page.state';
import { NavigationService } from '../../../core/services/navigation.service';
import { CoreState } from '../../../core/states/core.state';
import { FilterHelper } from '../../../shared/helpers/filter.helper';
import { CheckBoxHelper } from '../../../shared/helpers/list-checkbox.helper';
import { LocationSearchModel } from '../../../shared/models/address.model';
import { Enums } from '../../../shared/models/enums.model';
import { Filter, FilterData, FilterMode, UpdateParamTypes } from '../../../shared/models/filters.model';
import { DEFAULT_PAGINATED_OPTIONS } from '../../../shared/models/paginated-data.model';
import { LocationFilterService } from '../../../shared/services/location-filter.service';
import { QuickViewCandidateActions, ViewCandidateListPageActions } from '../../actions';
import { CandidateItem } from '../../models/candidate-item.model';
import { CandidateListMode, CandidateListParam, CandidateListViewParam, LocationSearchFilter } from '../../models/candidate-parametr.model';
import { ViewCandidatesListPageState } from '../../states/view-candidates-list.states';
import { QuickViewCandidateComponent } from '../quick-view-candidate.container';


@Component({
  selector: 'app-view-candidates-list',
  templateUrl: './view-candidates-list.component.html',
  styleUrls: ['./view-candidates-list.component.scss']
})
export class ViewCandidatesListPageComponent implements OnInit, OnDestroy {

  constructor(private store: Store,
              public dialog: MatDialog,
              private navigationService: NavigationService,
              private route: ActivatedRoute) {
  }

  private get pageIndex() {
    return this.store.selectSnapshot(ViewCandidatesListPageState.pageIndex);
  }

  private get pageSize() {
    return this.store.selectSnapshot(ViewCandidatesListPageState.pageSize);
  }

  private get currentSortingField() {
    return this.store.selectSnapshot(ViewCandidatesListPageState.currentSortingField);
  }

  @Select(ViewCandidatesListPageState.results) results$: Observable<Array<CandidateItem>>;
  @Select(ViewCandidatesListPageState.count) count$: Observable<number>;
  @Select(ViewCandidatesListPageState.pageSize) pageSize$: Observable<number>;
  @Select(ViewCandidatesListPageState.candidateSortingFilter) candidateSortingFilter$: Observable<any>;
  @Select(ViewCandidatesListPageState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;
  @Select(ViewCandidatesListPageState.showFilter) showFilter$: Observable<boolean>;
  @Select(ViewCandidatesListPageState.selectedFilters) selectedFilters$: Observable<Array<Filter>>;

  @Select(CoreState.CandidateStatusEnum) CandidateStatusEnum$: Observable<any>;
  @Select(CoreState.CandidateRatingEnum) CandidateRatingEnum$: Observable<object>;
  @Select(CoreState.enums) enums$: Observable<Enums>;

  @Select(ViewJobDetailsJsPageState.jobData) jobData$: Observable<any>;

  locationSearchFilter = LocationSearchFilter;
  filterData: Array<FilterData>;
  checkBoxHelper = new CheckBoxHelper('candidate-control-checkbox');

  candidateSearchForm: FormGroup = new FormGroup({
    search: new FormControl(''),
    location: new FormControl(''),
  });

  ngOnInit() {
    const ratingEnum = this.store.selectSnapshot(CoreState.CandidateRatingEnum);
    const statusEnum = this.store.selectSnapshot(CoreState.CandidateStatuses);
    const appliedDataEnum = this.store.selectSnapshot(CoreState.AppliedDateFilterEnum);

    this.filterData = [
      new FilterData(
        CandidateListViewParam.CANDIDATE_FILTER, CandidateListParam.CANDIDATE_FILTER, appliedDataEnum, FilterMode.SINGLE
      ),
      new FilterData(
        CandidateListViewParam.RATING_FILTER, CandidateListParam.RATING_FILTER, ratingEnum, FilterMode.SINGLE
      ),
      new FilterData(
        CandidateListViewParam.STATUS_FILTER, CandidateListParam.STATUS_FILTER, statusEnum, FilterMode.SINGLE
      ),
    ];
  }

  ngOnDestroy() {
    this.store.dispatch(new ViewCandidateListPageActions.ClearFilters());
  }

  public onSelectLocationFilter(selectedLocation: LocationSearchModel) {
    const filter = LocationFilterService.getLocationFilter(this.locationSearchFilter, selectedLocation);
    if (!FilterHelper.isFilterAlreadyAdded(filter, this.selectedFilters, this.store)) {
      this.store.dispatch(new ViewCandidateListPageActions.ChangeSelectedFilters(filter));
    }
  }

  public onFullTextSearchChanged(event: any) {
    this.store.dispatch(new ViewCandidateListPageActions.UpdateParams(event, UpdateParamTypes.COMMON));
  }

  onSubmitSearch(formData: any) {
    this.store.dispatch(new ViewCandidateListPageActions.UpdateParams(formData, UpdateParamTypes.COMMON));
  }

  onPageChanged(event: PageEvent) {
    this.store.dispatch(new ViewCandidateListPageActions.SetCurrentPagination(event));
    this.store.dispatch(new ViewCandidateListPageActions.UpdateParams(event, UpdateParamTypes.PAGINATION));
  }

  backToPostingPage() {
    this.navigationService.goToCompanyJobViewDetailsPage(this.store.selectSnapshot(ViewCandidatesListPageState.userId).toString());
  }

  onSortingFilterSelect(event: MatSelectChange) {
    this.store.dispatch(new ViewCandidateListPageActions.UpdateParams(event.value, UpdateParamTypes.SORTING));
    this.store.dispatch(new ViewCandidateListPageActions.SetCurrentSortingField(event.value));
  }

  onRadioFilterSelect(filter: Filter) {
    this.store.dispatch(new ViewCandidateListPageActions.ChangeSelectedFilters(filter));
  }

  public onSelectAllCandidate() {
    this.checkBoxHelper.selectAllCheckboxes();
  }

  isUserMode() {
    return this.store.selectSnapshot(ViewCandidatesListPageState.mode) === CandidateListMode.JOB_CANDIDATE;
  }

  getSelectedCandidates() {
    const data = this.store.selectSnapshot(ViewCandidatesListPageState.results);
    return data.filter(item => this.checkBoxHelper.getAllSelectedItems().includes(item.id))
      .map(item => item.job_seeker);
  }

  toggleFilterPanel() {
    this.store.dispatch(new ViewCandidateListPageActions.ToggleFilterList());
  }

  removeFilter(filter: Filter) {
    this.store.dispatch(new ViewCandidateListPageActions.RemoveSelectedFilter(filter));
  }

  clearFilters() {
    this.store.dispatch(new ViewCandidateListPageActions.ClearFilters());
  }

  goToCandidatesPage(item) {
    const jobId = this.route.snapshot.params['jobId'];
    const status = this.store.selectSnapshot(CoreState.CandidateStatuses).find(candidateStatus =>
      candidateStatus.name.toLowerCase() === item.key);
    this.store.dispatch(new ViewCandidateListPageActions.InitJobCandidateList(status));
    this.navigationService.goToViewCandidatesPage(jobId);
  }

  downloadCandidatesToCSV() {
    this.store.dispatch(new ViewCandidateListPageActions.DownloadCandidatesToCSV(this.selectedCandidates));
  }

  isCandidatesSelected() {
    return this.selectedCandidates.length > 0;
  }

  public get selectedCandidates() {
    return this.checkBoxHelper.getAllSelectedItems();
  }

  public onCommentCandidate(jsId: number) {
    this.getCommentData(jsId).subscribe(() => {
      const dialogRef = this.dialog.open(CommentsComponent, {
        width: '60%'
      });
      dialogRef.afterClosed().subscribe(() => {
        dialogRef.close();
      });
    });
  }

  public onQuickViewCandidate(candidateIndex: number) {
    this.store.dispatch(new QuickViewCandidateActions.LoadCandidateData(this.prepareQueryData(candidateIndex))).subscribe((res) => {
      const dialogRef = this.dialog.open(QuickViewCandidateComponent, {
        width: '90%'
      });
      dialogRef.afterClosed().subscribe(() => {
        this.store.dispatch(new ViewCandidateListPageActions.LoadCandidateData(this.params));
        dialogRef.close();
      });
    });
  }

  private prepareQueryData(candidateIndex: number) {
    const queryData = {
      limit: environment.quickViewLimit
    };
    if (this.pageIndex === 0) {
      Object.assign(queryData, {offset: candidateIndex});
    } else {
      Object.assign(queryData, {offset: this.pageIndex * this.pageSize + candidateIndex});
    }
    if (this.currentSortingField) {
      Object.assign(queryData, {ordering: this.currentSortingField});
    }
    return queryData;
  }

  private getCommentData(candidateId: number) {
    return forkJoin(
      this.store.dispatch(new CommentsActions.SetCommentType(CommentType.JobSeekerComment)),
      this.store.dispatch(new CommentsActions.SetModalMode(true)),
      this.store.dispatch(new CommentsActions.LoadCommentsData(candidateId, DEFAULT_PAGINATED_OPTIONS))
    );
  }

  private updateParamsWithLocation(formData) {
    if (formData.location) {
      const locationId = formData.location.id;
      Object.defineProperty(this.params, CandidateListParam.LOCATION_FILTER,
        {
          value: locationId,
          enumerable: true
        });
    } else {
      delete (this.params[CandidateListParam.LOCATION_FILTER]);
    }
  }

  public onChangeCandidate(data) {
    // Reload page after restore status
    if (data && data['action'] && data['action'] === environment.actionToRestore) {
      this.store.dispatch(new ViewCandidateListPageActions.LoadCandidateData(this.params));
    }
  }

  private get selectedFilters() {
    return this.store.selectSnapshot(ViewCandidatesListPageState.selectedFilters);
  }

  private get params() {
    return this.store.selectSnapshot(ViewCandidatesListPageState.params);
  }
}
