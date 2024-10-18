import { HttpErrorResponse } from '@angular/common/http';
import { MatSnackBarConfig } from '@angular/material';
import { Params } from '@angular/router';
import { LocationSearchModel } from '../../shared/models/address.model';
import { CandidateRatingEnum } from '../../shared/models/enums.model';
import {
  DEFAULT_SNACK_BAR_MESSAGE_DELAY,
  SnackBarMessage,
  SnackBarMessageType,
} from '../../shared/models/snack-bar-message';
import { createActionType } from './utils';

export const SNACKBAR_OPEN = createActionType('SNACKBAR_OPEN');
export const SNACKBAR_CLOSE = createActionType('SNACKBAR_CLOSE');
export const SKILL_LOAD_LIMIT = 100;


export enum CoreActionTypes {
  DispatchActionsOnInit = '[Core] DispatchActionsOnInit',
  SetInitialSettings = '[Core] SetInitialSettings',
  SetCountries = '[Core] SetCountries',
  GetStates = '[Core] GetStates',
  SetEnums = '[Core] SetEnums',
  ShowLoader = '[Core] ShowLoader',
  ShowGlobalLoader = '[Core] ShowGlobalLoader',
  HideLoader = '[Core] HideLoader',
  AddHttpError400 = '[Core] AddHttpError400',
  AddHttpError401 = '[Core] AddHttpError401',
  AddHttpError403 = '[Core] AddHttpError403',
  AddHttpError404 = '[Core] AddHttpError404',
  AddHttpError500 = '[Core] AddHttpError500',
  AddHttpErrorAny = '[Core] AddHttpErrorAny',
  RedirectTo = '[Core] RedirectTo',
  LoadIndustriesPart = '[Core] LoadIndustriesPart',
  LoadSkillsPart = '[Core] LoadSkillsPart',
  LoadIndustryData = '[Core] LoadIndustryData',
  SetStatuses = '[Core] SetStatuses',
  SetAutoApplyEnums = '[Core] SetAutoApplyEnums',
  SaveJobToFavorites = '[Core] SaveJobToFavorites',
  DeleteJobFromFavorites = '[Core] DeleteJobFromFavorites',
  ListFavoriteJobs = '[Core] ListFavoriteJobs',
  LoadAppliedJobs = '[Core] LoadAppliedJobs',
  LoadPurchasedJobSeekers = '[Core] LoadPurchasedJobSeekers',
  PurchaseJobSeeker = '[Core] PurchaseJobSeeker',
  RateCandidate = '[Core] RateCandidate',
  UpdateCandidateStatus = '[Core] UpdateCandidateStatus',
  RestoreCandidateStatus = '[Core] RestoreCandidateStatus',
  GetCities = '[Core] GetCities',
  GetZips = '[Core] GetZips',
  GetCandidateStatuses = '[Core] GetCandidateStatuses',
  LocationSearch = '[Core] LocationSearch',
  SetGlobalSearch = '[Core] SetGlobalSearch',
  SetGlobalSearchParam = '[Core] SetGlobalSearchParam',
  SetGlobalLocationParam = '[Core] SetGlobalLocationParam',
  SaveJobSeekerToFavorites = '[Core] SaveJobSeekerToFavorites',
  UpdateUserPlanSubscription = '[Core] UpdateUserPlanSubscription',
}


export class DispatchActionsOnInit {
  static readonly type = CoreActionTypes.DispatchActionsOnInit;
}


export class SnackbarOpen {
  static readonly type = SNACKBAR_OPEN;
  public message: SnackBarMessage;

  constructor(public payload: SnackBarMessage) {
    this.message = payload;
    let config = this.message.config;
    if (!config) {
      config = new MatSnackBarConfig();
      config.verticalPosition = 'bottom';
      config.horizontalPosition = 'right';
      config.duration = 0;
    }
    if (!this.message.delay) {
      this.message.delay = DEFAULT_SNACK_BAR_MESSAGE_DELAY;
    }
    if (!this.message.type) {
      this.message.type = SnackBarMessageType.DEFAULT_MESSAGE_TYPE;
    }
    config.panelClass = `style-${this.message.type}`;
    this.message.config = config;
  }
}


export class SnackbarClose {
  static readonly type = SNACKBAR_CLOSE;
}


export class SetInitialSettings {
  static readonly type = CoreActionTypes.SetInitialSettings;
}


export class SetCountries {
  static readonly type = CoreActionTypes.SetCountries;
}


export class GetStates {
  static readonly type = CoreActionTypes.GetStates;

  constructor(public params: any) {
  }
}


export class GetCities {
  static readonly type = CoreActionTypes.GetCities;

  constructor(public params: any) {
  }
}


export class GetZips {
  static readonly type = CoreActionTypes.GetZips;

  constructor(public cityId: number, public params?: object) {
  }
}


export class SetEnums {
  static readonly type = CoreActionTypes.SetEnums;
}


export class LocationSearch {
  static readonly type = CoreActionTypes.LocationSearch;

  constructor(public searchStr: string) {
  }
}


export class SetAutoApplyEnums {
  static readonly type = CoreActionTypes.SetAutoApplyEnums;
}


export class SetStatuses {
  static readonly type = CoreActionTypes.SetStatuses;
}


export class ShowLoader {
  static readonly type = CoreActionTypes.ShowLoader;
}


export class ShowGlobalLoader {
  static readonly type = CoreActionTypes.ShowGlobalLoader;
}


export class HideLoader {
  static readonly type = CoreActionTypes.HideLoader;
}


export class AddHttpError400 {
  static readonly type = CoreActionTypes.AddHttpError400;

  constructor(public error: HttpErrorResponse) {
  }
}


export class AddHttpError401 {
  static readonly type = CoreActionTypes.AddHttpError401;

  constructor(public error: HttpErrorResponse) {
  }
}


export class AddHttpError403 {
  static readonly type = CoreActionTypes.AddHttpError403;

  constructor(public error: HttpErrorResponse) {
  }
}


export class AddHttpError404 {
  static readonly type = CoreActionTypes.AddHttpError404;

  constructor(public error: HttpErrorResponse) {
  }
}


export class AddHttpError500 {
  static readonly type = CoreActionTypes.AddHttpError500;

  constructor(public error: HttpErrorResponse) {
  }
}


export class AddHttpErrorAny {
  static readonly type = CoreActionTypes.AddHttpErrorAny;

  constructor(public error: HttpErrorResponse) {
  }
}


export class RedirectTo {
  static readonly type = CoreActionTypes.RedirectTo;

  constructor(public route: string, public isBlank?: boolean, public queryParams?: Params) {
  }
}


export class LoadIndustryData {
  static readonly type = CoreActionTypes.LoadIndustryData;
}


export class GetCandidateStatuses {
  static readonly type = CoreActionTypes.GetCandidateStatuses;
}


export class LoadIndustriesPart {
  static readonly type = CoreActionTypes.LoadIndustriesPart;

  constructor(public offset?: number,
              public limit?: number,
              public ordering?: string) {
    if (!offset) {
      this.offset = 0;
    }
    if (!limit) {
      this.limit = SKILL_LOAD_LIMIT;
    }
    if (!ordering) {
      this.ordering = null;
    }
  }
}


export class LoadSkillsPart {
  static readonly type = CoreActionTypes.LoadSkillsPart;

  constructor(public name?: string,
              public offset?: number,
              public limit?: number,
              public ordering?: string) {
    if (!name) {
      this.name = '';
    }
    if (!offset) {
      this.offset = 0;
    }
    if (!limit) {
      this.limit = SKILL_LOAD_LIMIT;
    }
    if (!ordering) {
      this.ordering = null;
    }
  }
}


export class SaveJobToFavorites {
  static readonly type = CoreActionTypes.SaveJobToFavorites;

  constructor(public id: number, public jobId: number) {
  }
}


export class SaveJobSeekerToFavorites {
  static readonly type = CoreActionTypes.SaveJobSeekerToFavorites;

  constructor(public id: number, public shouldRemove?: boolean) {
  }
}


export class DeleteJobFromFavorites {
  static readonly type = CoreActionTypes.DeleteJobFromFavorites;

  constructor(public id: number, public jobId: number) {
  }
}


export class ListFavoriteJobs {
  static readonly type = CoreActionTypes.ListFavoriteJobs;

  constructor(public id: number, public params?: object) {
  }
}


export class LoadAppliedJobs {
  static readonly type = CoreActionTypes.LoadAppliedJobs;

  constructor() {
  }
}


export class LoadPurchasedJobSeekers {
  static readonly type = CoreActionTypes.LoadPurchasedJobSeekers;

  constructor() {
  }
}


export class PurchaseJobSeeker {
  static readonly type = CoreActionTypes.PurchaseJobSeeker;

  constructor(public id: number) {
  }
}


export class RateCandidate {
  static readonly type = CoreActionTypes.RateCandidate;

  constructor(public id: number, public score: CandidateRatingEnum) {
  }
}


export class UpdateCandidateStatus {
  static readonly type = CoreActionTypes.UpdateCandidateStatus;

  constructor(public id: number, public status) {
  }
}


export class RestoreCandidateStatus {
  static readonly type = CoreActionTypes.RestoreCandidateStatus;

  constructor(public id: number) {
  }
}


export class SetGlobalSearch {
  static readonly type = CoreActionTypes.SetGlobalSearch;

  constructor(public value: boolean) {
  }
}


export class SetGlobalSearchParam {
  static readonly type = CoreActionTypes.SetGlobalSearchParam;

  constructor(public value: string) {
  }
}


export class SetGlobalLocationParam {
  static readonly type = CoreActionTypes.SetGlobalLocationParam;

  constructor(public value: LocationSearchModel) {
  }
}


export class UpdateUserPlanSubscription {
  static readonly type = CoreActionTypes.UpdateUserPlanSubscription;
}


export type CoreActionsUnion =
  | UpdateUserPlanSubscription
  | SetGlobalLocationParam
  | SetGlobalSearchParam
  | SetGlobalSearch
  | GetZips
  | GetCities
  | DispatchActionsOnInit
  | SnackbarOpen
  | SnackbarClose
  | SetInitialSettings
  | SetCountries
  | GetStates
  | SetEnums
  | SetAutoApplyEnums
  | ShowLoader
  | HideLoader
  | AddHttpError400
  | AddHttpError401
  | AddHttpError403
  | AddHttpError404
  | AddHttpError500
  | AddHttpErrorAny
  | RedirectTo
  | LoadIndustryData
  | SetStatuses
  | SaveJobToFavorites
  | DeleteJobFromFavorites
  | ListFavoriteJobs
  | LoadAppliedJobs
  | LoadPurchasedJobSeekers
  | PurchaseJobSeeker
  | UpdateCandidateStatus
  | RestoreCandidateStatus
  | LocationSearch
  | GetCandidateStatuses
  | ShowGlobalLoader
  | SaveJobSeekerToFavorites;
