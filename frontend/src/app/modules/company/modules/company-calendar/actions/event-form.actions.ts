export enum EventFormActionTypes {
  LoadJobPostings = '[Event Form] LoadJobPostings',
  LoadColleagues = '[Event Form] LoadColleagues',
  LoadCandidates = '[Event Form] LoadCandidates',
  UpdateCandidates = '[Event Form] UpdateCandidates',
  LoadZones = '[Event Form] LoadZones',
  LoadLetterTemplates = '[Event Form] LoadLetterTemplates',
  LoadCountries = '[Event Form] LoadCountries',
  LoadCities = '[Event Form] LoadCities',
  ChangeCitiesSearch = '[Event Form] ChangeCitiesSearch',
  UpdateCities = '[Event Form] UpdateCities',
  GetNextCities = '[Event Form] GetNextCities',
  LoadZips = '[Event Form] LoadZips',
  UpdateZips = '[Event Form] UpdateZips',
  LoadEvent = '[Event Form] LoadEvent',
  LoadInitData = '[Event Form] LoadInitData',
  Submit = '[Event Form] Submit',
  DeleteEvent = '[Event Form] DeleteEvent',
  CloseEventFormDialog = '[Event Form] CloseEventFormDialog',
  CleenUp = '[Event Form] CleenUp'
}

export class LoadJobPostings {
  static readonly type = EventFormActionTypes.LoadJobPostings;
}

export class LoadColleagues {
  static readonly type = EventFormActionTypes.LoadColleagues;
}

export class LoadZones {
  static readonly type = EventFormActionTypes.LoadZones;
}

export class LoadLetterTemplates {
  static readonly type = EventFormActionTypes.LoadLetterTemplates;
}

export class LoadEvent {
  static readonly type = EventFormActionTypes.LoadEvent;
  constructor(public eventId: number) {}
}

export class LoadCandidates {
  static readonly type = EventFormActionTypes.LoadCandidates;
  constructor(public jobId: number) {}
}

export class UpdateCandidates {
  static readonly type = EventFormActionTypes.UpdateCandidates;
  constructor(public jobId: number) {}
}

export class LoadCountries {
  static readonly type = EventFormActionTypes.LoadCountries;
}

export class LoadCities {
  static readonly type = EventFormActionTypes.LoadCities;
  constructor(public countryId: number, public cityName?: string) {}
}

export class ChangeCitiesSearch {
  static readonly type = EventFormActionTypes.ChangeCitiesSearch;
  constructor(public searchStr: string) {}
}

export class UpdateCities {
  static readonly type = EventFormActionTypes.UpdateCities;
  constructor(public countryId: number) {}
}

export class GetNextCities {
  static readonly type = EventFormActionTypes.GetNextCities;
}

export class LoadZips {
  static readonly type = EventFormActionTypes.LoadZips;
  constructor(public cityId: number) {}
}

export class UpdateZips {
  static readonly type = EventFormActionTypes.UpdateZips;
  constructor(public cityId: number) {}
}

export class LoadInitData {
  static readonly type = EventFormActionTypes.LoadInitData;
  constructor(public forEvent: any) {}
}

export class Submit {
  static readonly type = EventFormActionTypes.Submit;
  constructor(public force?: boolean) {}
}

export class DeleteEvent {
  static readonly type = EventFormActionTypes.DeleteEvent;
}

export class CloseEventFormDialog {
  static readonly type = EventFormActionTypes.CloseEventFormDialog;
}

export class CleenUp {
  static readonly type = EventFormActionTypes.CleenUp;
}

export type EventFormActionsUnion =
  | LoadJobPostings
  | LoadColleagues
  | LoadCandidates
  | UpdateCandidates
  | LoadZones
  | LoadLetterTemplates
  | LoadCountries
  | LoadCities
  | ChangeCitiesSearch
  | UpdateCities
  | GetNextCities
  | LoadZips
  | UpdateZips
  | LoadEvent
  | LoadInitData
  | Submit
  | DeleteEvent
  | CloseEventFormDialog
  | CleenUp;
