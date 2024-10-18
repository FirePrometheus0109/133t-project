import { FilterData, FilterMode } from '../../shared/models/filters.model';


export enum JobsListParam {
  EXPERIENCE_FILTER = 'experience',
  EDUCATION_FILTER = 'education',
  POSITION_FILTER = 'position_type',
  CLEARENCE_FILTER = 'clearance',
  TRAVEL_FILTER = 'travel',
  SKILL_FILTER = 'skills',
  POSTED_DATE_FILTER = 'posted_ago',
  FULL_TEXT_SEARCH = 'search',
  LOCATION_FILTER = 'location',
  SALARY_MIN_FILTER = 'salary_min',
  SALARY_MAX_FILTER = 'salary_max',
  COMPANY_FILTER = 'company',
  COMPANY_EXCLUDE_FILTER = 'excl_company',
}


export enum JobsListViewParam {
  EXPERIENCE_FILTER = 'Years of experience',
  EDUCATION_FILTER = 'Education',
  POSITION_FILTER = 'Position type',
  CLEARENCE_FILTER = 'Clearance',
  TRAVEL_FILTER = 'Travel opportunities',
  SKILL_FILTER = 'Skills',
  POSTED_DATE_FILTER = 'Posted Date',
  FULL_TEXT_SEARCH = 'Search',
  LOCATION_FILTER = 'Location',
  SALARY_MIN_FILTER = 'Salary from',
  SALARY_MAX_FILTER = 'Salary to',
  COMPANY_FILTER = 'Company',
  COMPANY_EXCLUDE_FILTER = 'Company exclude',
}


export const SkillSearchFilter = new FilterData(JobsListViewParam.SKILL_FILTER,
  JobsListParam.SKILL_FILTER, null, FilterMode.SEARCH);

export const LocationSearchFilter = new FilterData(JobsListViewParam.LOCATION_FILTER,
  JobsListParam.LOCATION_FILTER, null, FilterMode.SEARCH);

export const SalaryMinFilter = new FilterData(JobsListViewParam.SALARY_MIN_FILTER,
  JobsListParam.SALARY_MIN_FILTER, null, FilterMode.SINGLE);

export const SalaryMaxFilter = new FilterData(JobsListViewParam.SALARY_MAX_FILTER,
  JobsListParam.SALARY_MAX_FILTER, null, FilterMode.SINGLE);

export const CompanyFilter = new FilterData(JobsListViewParam.COMPANY_FILTER,
  JobsListParam.COMPANY_FILTER, null, FilterMode.MULTIPLE);

export const CompanyExcludeFilter = new FilterData(JobsListViewParam.COMPANY_EXCLUDE_FILTER,
  JobsListParam.COMPANY_EXCLUDE_FILTER, null, FilterMode.MULTIPLE);

export const FullTextSearchFilter = new FilterData(JobsListViewParam.FULL_TEXT_SEARCH,
  JobsListParam.FULL_TEXT_SEARCH, null, FilterMode.SEARCH);


export enum CompanySelectionType {
  INCLUDE = 'companiesInclude',
  EXCLUDE = 'companiesExclude'
}
