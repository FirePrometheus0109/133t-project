import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatAutocompleteSelectedEvent, MatDialog, PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { CoreActions } from 'src/app/modules/core/actions';
import { CoreState } from 'src/app/modules/core/states/core.state';
import { LocationSearchModel } from 'src/app/modules/shared/models';
import { Enums } from 'src/app/modules/shared/models/enums.model';
import { Filter, FilterData, FilterMode, SortingFilter, UpdateParamTypes } from 'src/app/modules/shared/models/filters.model';
import { CommentsActions } from '../../../common-components/actions';
import { CommentsComponent } from '../../../common-components/containers/comments.container';
import { CommentType } from '../../../common-components/models/comment.model';
import { FilterHelper } from '../../../shared/helpers/filter.helper';
import { DEFAULT_PAGINATED_OPTIONS } from '../../../shared/models/paginated-data.model';
import { LocationFilterService } from '../../../shared/services/location-filter.service';
import { ViewJobSeekerListPageActions } from '../../actions';
import { JobSeekerProfile } from '../../models';
import {
  JobSeekerListMode, JobSeekerListParam,
  JobSeekerListViewParam, LocationSearchFilter, SkillSearchFilter
} from '../../models/job-seeker-list-fitlers.model';
import { ViewJobSeekerListState } from '../../states/view-job-seeker-list.state';


@Component({
  selector: 'app-view-job-seeker-list',
  templateUrl: './view-job-seeker-list.component.html',
  styleUrls: ['./view-job-seeker-list.component.css']
})
export class ViewJobSeekerListComponent implements OnInit, OnDestroy {

  @Select(ViewJobSeekerListState.results) results: Observable<Array<JobSeekerProfile>>;
  @Select(ViewJobSeekerListState.count) count$: Observable<number>;
  @Select(ViewJobSeekerListState.pageSize) pageSize$: Observable<number>;
  @Select(ViewJobSeekerListState.sortingFilter) sortingFilter$: Observable<SortingFilter[]>;
  @Select(ViewJobSeekerListState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;
  @Select(ViewJobSeekerListState.showFilter) showFilter$: Observable<boolean>;
  @Select(ViewJobSeekerListState.selectedFilters) selectedFilters$: Observable<Array<Filter>>;
  @Select(ViewJobSeekerListState.mode) mode$: Observable<JobSeekerListMode>;

  @Select(CoreState.enums) enums$: Observable<Enums>;
  @Select(CoreState.skillsFiltered) skillsFiltered$: Observable<object>;
  @Select(CoreState.filteredLocation) filteredLocation$: Observable<Array<any>>;

  radioFilterData: Array<FilterData>;

  skillSearchFilter = SkillSearchFilter;
  locationSearchFilter = LocationSearchFilter;

  jobSeekersSearchForm: FormGroup = new FormGroup({
    search: new FormControl(''),
    location: new FormControl(''),
  });

  constructor(private store: Store, private dialog: MatDialog) {
  }

  ngOnInit() {
    const experienceEnum = this.store.selectSnapshot(CoreState.ExperienceTypes);
    const educationEnum = this.store.selectSnapshot(CoreState.EducationTypes);
    const positionEnum = this.store.selectSnapshot(CoreState.PositionTypes);
    const clearanceEnum = this.store.selectSnapshot(CoreState.ClearanceTypes);
    const travelEnum = this.store.selectSnapshot(CoreState.JSTravelOpportunities);
    const lastUpdateEnum = this.store.selectSnapshot(CoreState.LastUpdatedWithingDays);

    this.radioFilterData = [
      new FilterData(JobSeekerListViewParam.EDUCATION_FILTER,
        JobSeekerListParam.EDUCATION_FILTER, educationEnum, FilterMode.SINGLE),
      new FilterData(JobSeekerListViewParam.EXPERIENCE_FILTER,
        JobSeekerListParam.EXPERIENCE_FILTER, experienceEnum, FilterMode.SINGLE),
      new FilterData(JobSeekerListViewParam.POSITION_FILTER,
        JobSeekerListParam.POSITION_FILTER, positionEnum, FilterMode.MULTIPLE),
      new FilterData(JobSeekerListViewParam.CLEARENCE_FILTER,
        JobSeekerListParam.CLEARENCE_FILTER, clearanceEnum, FilterMode.MULTIPLE),
      new FilterData(JobSeekerListViewParam.TRAVEL_FILTER,
        JobSeekerListParam.TRAVEL_FILTER, travelEnum, FilterMode.SINGLE),
      new FilterData(JobSeekerListViewParam.LAST_UPDATE,
        JobSeekerListParam.LAST_UPDATE, lastUpdateEnum, FilterMode.SINGLE)
    ];
    this.updateSearchFieldFromGlobal();
  }

  ngOnDestroy() {
    this.store.dispatch(new CoreActions.SetGlobalLocationParam(null));
    this.store.dispatch(new CoreActions.SetGlobalSearchParam(''));
    this.store.dispatch(new ViewJobSeekerListPageActions.ClearFilters());
  }

  onPageChanged(event: PageEvent) {
    this.store.dispatch(new ViewJobSeekerListPageActions.UpdateParams(event, UpdateParamTypes.PAGINATION));
  }

  onSortingFilterSelect(event: MatAutocompleteSelectedEvent) {
    this.store.dispatch(new ViewJobSeekerListPageActions.UpdateParams(event['value'], UpdateParamTypes.SORTING));
  }

  onToggleFilter() {
    this.store.dispatch(new ViewJobSeekerListPageActions.ToggleFilterList());
  }

  onSelectSkillFilter(selectedSkill) {
    const filter = new Filter(this.skillSearchFilter, {key: selectedSkill.id, value: selectedSkill.name});
    if (!FilterHelper.isFilterAlreadyAdded(filter, this.selectedFilters, this.store)) {
      this.store.dispatch(new ViewJobSeekerListPageActions.ChangeSelectedFilters(filter));
    }
  }

  onSelectLocationFilter(selectedLocation: LocationSearchModel) {
    const filter = LocationFilterService.getLocationFilter(this.locationSearchFilter, selectedLocation);
    if (!FilterHelper.isFilterAlreadyAdded(filter, this.selectedFilters, this.store)) {
      this.store.dispatch(new ViewJobSeekerListPageActions.ChangeSelectedFilters(filter));
    }
  }

  public onFullTextSearchChanged(event: any) {
    this.store.dispatch(new ViewJobSeekerListPageActions.UpdateParams(event, UpdateParamTypes.COMMON));
  }

  onSkillSearchChange(value: string) {
    this.store.dispatch(new CoreActions.LoadSkillsPart(value));
  }

  onRadioFilterSelect(filter: Filter) {
    this.store.dispatch(new ViewJobSeekerListPageActions.ChangeSelectedFilters(filter));
  }

  onSubmitSearch(formData) {
    this.store.dispatch(new ViewJobSeekerListPageActions.UpdateParams(formData, UpdateParamTypes.COMMON));
  }

  removeFilter(filter: Filter) {
    this.store.dispatch(new ViewJobSeekerListPageActions.RemoveSelectedFilter(filter));
  }

  clearFilters() {
    this.store.dispatch(new ViewJobSeekerListPageActions.ClearFilters());
  }

  shouldShowFilter(mode: JobSeekerListMode) {
    return mode === JobSeekerListMode.ALL;
  }

  onCommentJobSeeker(jobSeekerId: number) {
    this.getCommentData(jobSeekerId).subscribe(() => {
      const dialogRef = this.dialog.open(CommentsComponent, {
        width: '60%'
      });
      dialogRef.afterClosed().subscribe(() => {
        dialogRef.close();
      });
    });
  }

  private updateSearchFieldFromGlobal() {
    const globalSearch = this.store.selectSnapshot(CoreState.globalSearchParam);
    if (globalSearch) {
      this.jobSeekersSearchForm.controls.search.setValue(globalSearch);
    }
  }

  private get selectedFilters() {
    return this.store.selectSnapshot(ViewJobSeekerListState.selectedFilters);
  }

  private getCommentData(jobSeekerId: number) {
    return forkJoin(
      this.store.dispatch(new CommentsActions.SetCommentType(CommentType.JobSeekerComment)),
      this.store.dispatch(new CommentsActions.SetModalMode(true)),
      this.store.dispatch(new CommentsActions.LoadCommentsData(jobSeekerId, DEFAULT_PAGINATED_OPTIONS))
    );
  }
}
