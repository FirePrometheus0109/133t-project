import { FilterData, FilterMode } from '../../shared/models/filters.model';


export enum CandidateListParam {
  CANDIDATE_FILTER = 'applied_date',
  RATING_FILTER = 'rating__rating',
  STATUS_FILTER = 'status',
  LOCATION_FILTER = 'location',
}


export enum CandidateListViewParam {
  CANDIDATE_FILTER = 'Applied Date',
  RATING_FILTER = 'Rate',
  STATUS_FILTER = 'Status type',
  LOCATION_FILTER = 'Location',
}


export enum CandidateListMode {
  ALL_CANDIDATE,
  JOB_CANDIDATE,
}


export const LocationSearchFilter = new FilterData(CandidateListViewParam.LOCATION_FILTER,
  CandidateListParam.LOCATION_FILTER, null, FilterMode.SEARCH);
