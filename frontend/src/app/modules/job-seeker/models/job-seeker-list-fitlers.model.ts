import { FilterData, FilterMode } from '../../shared/models/filters.model';

export enum JobSeekerListMode  {
  ALL,
  PURCHASED,
  SAVED,
}

export enum JobSeekerListParam {
  EXPERIENCE_FILTER = 'experience',
  EDUCATION_FILTER = 'education',
  POSITION_FILTER = 'position_type',
  CLEARENCE_FILTER = 'clearance',
  TRAVEL_FILTER = 'travel',
  SKILL_FILTER = 'skills',
  LAST_UPDATE = 'profile_updated_within_days',
  FULL_TEXT_SEARCH = 'search',
  LOCATION_FILTER = 'location'
}

export enum JobSeekerListViewParam {
  EXPERIENCE_FILTER = 'Years of experience',
  EDUCATION_FILTER = 'Education',
  POSITION_FILTER = 'Position type',
  CLEARENCE_FILTER = 'Clearance',
  TRAVEL_FILTER = 'Travel opportunities',
  SKILL_FILTER = 'Skills',
  LAST_UPDATE = 'Last Update',
  LOCATION_FILTER = 'Location'
}

export const SkillSearchFilter = new FilterData(JobSeekerListViewParam.SKILL_FILTER,
   JobSeekerListParam.SKILL_FILTER, null, FilterMode.SEARCH);

export const LocationSearchFilter = new FilterData(JobSeekerListViewParam.LOCATION_FILTER,
   JobSeekerListParam.LOCATION_FILTER, null, FilterMode.SEARCH);
