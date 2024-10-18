import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatAutocompleteSelectedEvent, PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreActions } from '../../../core/actions';
import { CoreState } from '../../../core/states/core.state';
import { FilterHelper } from '../../../shared/helpers/filter.helper';
import { LocationSearchModel } from '../../../shared/models/address.model';
import { Enums } from '../../../shared/models/enums.model';
import { Filter, FilterData, FilterMode, SortingFilter, UpdateParamTypes } from '../../../shared/models/filters.model';
import { SkillItem } from '../../../shared/models/skill.model';
import { LocationFilterService } from '../../../shared/services/location-filter.service';
import { SearchJobListPageActions } from '../../actions';
import {
  CompanyExcludeFilter,
  CompanyFilter,
  JobsListParam,
  JobsListViewParam,
  LocationSearchFilter,
  SalaryMaxFilter,
  SalaryMinFilter,
  SkillSearchFilter
} from '../../models/jobs-list-filters.model';
import { PublicCompanyItem } from '../../models/public-company.model';
import { SearchJobListPageState } from '../../states/search-job-list-page.state';


@Component({
  selector: 'app-search-job-list-page',
  templateUrl: './search-job-list-page.component.html',
  styleUrls: ['./search-job-list-page.component.css']
})
export class SearchJobListPageComponent implements OnInit, OnDestroy {
  @Select(CoreState.enums) enums$: Observable<Enums>;
  @Select(CoreState.JobStatusEnum) jobStatusEnum$: Observable<object>;
  @Select(CoreState.skillsFiltered) skillsFiltered$: Observable<object>;
  @Select(CoreState.globalSearchParam) globalSearchParam$: Observable<string>;

  @Select(SearchJobListPageState.jobSortingFilters) jobSortingFilters$: Observable<SortingFilter[]>;
  @Select(SearchJobListPageState.results) results$: Observable<any>;
  @Select(SearchJobListPageState.count) count$: Observable<number>;
  @Select(SearchJobListPageState.pageSize) pageSize$: Observable<number>;
  @Select(SearchJobListPageState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;
  @Select(SearchJobListPageState.showFilter) showFilter$: Observable<boolean>;
  @Select(SearchJobListPageState.selectedFilters) selectedFilters$: Observable<Array<Filter>>;
  @Select(SearchJobListPageState.companiesInclude) companiesInclude$: Observable<PublicCompanyItem[]>;
  @Select(SearchJobListPageState.companiesIncludeSearch) companiesIncludeSearch$: Observable<string>;
  @Select(SearchJobListPageState.companiesExclude) companiesExclude$: Observable<PublicCompanyItem[]>;
  @Select(SearchJobListPageState.companiesExcludeSearch) companiesExcludeSearch$: Observable<string>;

  public jobSearchForm: FormGroup = new FormGroup({
    search: new FormControl(''),
    location: new FormControl(''),
  });

  public salaryMinFilterForm: FormGroup = new FormGroup({
    salary_min: new FormControl(''),
  });

  public salaryMaxFilterForm: FormGroup = new FormGroup({
    salary_max: new FormControl(''),
  });

  public radioFilterData: Array<FilterData>;
  public skillSearchFilter = SkillSearchFilter;
  public salaryMinFilter = SalaryMinFilter;
  public salaryMaxFilter = SalaryMaxFilter;
  public companyFilter = CompanyFilter;
  public companyExcludeFilter = CompanyExcludeFilter;
  public locationSearchFilter = LocationSearchFilter;

  constructor(private store: Store) {
  }

  ngOnInit() {
    this.updateSearchFieldFromGlobal();
    this.defineFilters();
  }

  ngOnDestroy() {
    this.store.dispatch(new CoreActions.SetGlobalLocationParam(null));
    this.store.dispatch(new CoreActions.SetGlobalSearchParam(''));
    this.store.dispatch(new SearchJobListPageActions.ClearFilters());
  }

  public onFullTextSearchChanged(event: any) {
    this.store.dispatch(new SearchJobListPageActions.UpdateParams(event, UpdateParamTypes.COMMON));
  }

  public onSelectLocationFilter(selectedLocation: LocationSearchModel) {
    const filter = LocationFilterService.getLocationFilter(this.locationSearchFilter, selectedLocation);
    if (!FilterHelper.isFilterAlreadyAdded(filter, this.selectedFilters, this.store)) {
      this.store.dispatch(new SearchJobListPageActions.ChangeSelectedFilters(filter));
    }
  }

  public searchCompanyInclude(event: string) {
    this.store.dispatch(new SearchJobListPageActions.LoadCompaniesInclude(event));
  }

  public searchCompanyExclude(event: string) {
    this.store.dispatch(new SearchJobListPageActions.LoadCompaniesExclude(event));
  }

  public onSalaryMinChanged(event) {
    this.provideSalaryFilter(this.salaryMinFilter, event.salary_min);
  }

  public onSalaryMaxChanged(event) {
    this.provideSalaryFilter(this.salaryMaxFilter, event.salary_max);
  }

  public onCompanyChanged(event) {
    this.provideCompanyFilter(this.companyFilter, event);
  }

  public onCompanyExcludeChanged(event) {
    this.provideCompanyFilter(this.companyExcludeFilter, event);
  }

  public onSortingFilterSelect(event: MatAutocompleteSelectedEvent) {
    this.store.dispatch(new SearchJobListPageActions.UpdateParams(event['value'], UpdateParamTypes.SORTING));
  }

  public onSubmitSearch(formData: any) {
    this.store.dispatch(new SearchJobListPageActions.UpdateParams(formData, UpdateParamTypes.COMMON));
  }

  public onPageChanged(event: PageEvent) {
    this.store.dispatch(new SearchJobListPageActions.UpdateParams(event, UpdateParamTypes.PAGINATION));
  }

  public onToggleFilter() {
    this.store.dispatch(new SearchJobListPageActions.ToggleFilterList());
  }

  public onRadioFilterSelect(filter: Filter) {
    this.store.dispatch(new SearchJobListPageActions.ChangeSelectedFilters(filter));
  }

  public onSkillSearchChange(value: string) {
    this.store.dispatch(new CoreActions.LoadSkillsPart(value));
  }

  public onSelectSkillFilter(selectedSkill: SkillItem) {
    const filter = new Filter(this.skillSearchFilter, {key: selectedSkill.id, value: selectedSkill.name});
    if (!FilterHelper.isFilterAlreadyAdded(filter, this.selectedFilters, this.store)) {
      this.store.dispatch(new SearchJobListPageActions.ChangeSelectedFilters(filter));
    }
  }

  public clearFilters() {
    this.store.dispatch(new SearchJobListPageActions.ClearFilters());
  }

  public removeFilter(filter: Filter) {
    this.store.dispatch(new SearchJobListPageActions.RemoveSelectedFilter(filter));
  }

  private provideSalaryFilter(salaryFilter, eventValue) {
    const filter = new Filter(salaryFilter, {key: eventValue, value: eventValue});
    if (eventValue) {
      if (!FilterHelper.isFilterAlreadyAdded(filter, this.selectedFilters, this.store, true)) {
        this.store.dispatch(new SearchJobListPageActions.ChangeSelectedFilters(filter));
      }
    } else {
      this.store.dispatch(new SearchJobListPageActions.RemoveSelectedFilter(filter));
    }
  }

  private defineFilters() {
    const experienceEnum = this.store.selectSnapshot(CoreState.ExperienceTypes);
    const educationEnum = this.store.selectSnapshot(CoreState.EducationTypes);
    const positionEnum = this.store.selectSnapshot(CoreState.PositionTypes);
    const clearanceEnum = this.store.selectSnapshot(CoreState.ClearanceTypes);
    const travelEnum = this.store.selectSnapshot(CoreState.TravelOpportunities);
    const lastUpdateEnum = this.store.selectSnapshot(CoreState.LastUpdatedWithingDays);

    this.radioFilterData = [
      new FilterData(JobsListViewParam.EDUCATION_FILTER,
        JobsListParam.EDUCATION_FILTER, educationEnum, FilterMode.SINGLE),
      new FilterData(JobsListViewParam.EXPERIENCE_FILTER,
        JobsListParam.EXPERIENCE_FILTER, experienceEnum, FilterMode.SINGLE),
      new FilterData(JobsListViewParam.POSITION_FILTER,
        JobsListParam.POSITION_FILTER, positionEnum, FilterMode.MULTIPLE),
      new FilterData(JobsListViewParam.CLEARENCE_FILTER,
        JobsListParam.CLEARENCE_FILTER, clearanceEnum, FilterMode.MULTIPLE),
      new FilterData(JobsListViewParam.TRAVEL_FILTER,
        JobsListParam.TRAVEL_FILTER, travelEnum, FilterMode.SINGLE),
      new FilterData(JobsListViewParam.POSTED_DATE_FILTER,
        JobsListParam.POSTED_DATE_FILTER, lastUpdateEnum, FilterMode.SINGLE)
    ];
  }

  private provideCompanyFilter(companyFilter: FilterData, outputEvent) {
    const filter = new Filter(companyFilter, {key: outputEvent.value.id, value: outputEvent.value.name});
    outputEvent.isSelected ? this.store.dispatch(new SearchJobListPageActions.RemoveSelectedFilter(filter)) :
      this.store.dispatch(new SearchJobListPageActions.ChangeSelectedFilters(filter));
  }

  private updateSearchFieldFromGlobal() {
    const globalSearch = this.store.selectSnapshot(CoreState.globalSearchParam);
    if (globalSearch) {
      this.jobSearchForm.controls.search.setValue(globalSearch);
    }
  }

  private get selectedFilters() {
    return this.store.selectSnapshot(SearchJobListPageState.selectedFilters);
  }
}
