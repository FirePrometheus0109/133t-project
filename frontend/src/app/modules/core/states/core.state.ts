import { HttpErrorResponse } from '@angular/common/http';
import { MatSnackBar, MatSnackBarRef, SimpleSnackBar } from '@angular/material';
import { Navigate } from '@ngxs/router-plugin';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, debounceTime, delay, map, tap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { AuthActions } from '../../auth/actions';
import { Changelog } from '../../auth/models/version.model';
import { AuthSocialService } from '../../auth/services/auth-social.service';
import { CandidateStatus } from '../../candidate/models/candidate-item.model';
import { CandidateService } from '../../candidate/services/candidate.service';
import { JobSeekerService } from '../../job-seeker/services/job-seeker.service';
import { CityModel, LocationSearchModel, ZipModel } from '../../shared/models/address.model';
import {
  AppliedDateFilterEnum, ApplyStatusEnum, AutoapplyStatusEnum, BenefitsEnum, CandidateRatingEnum,
  CandidateStatusEnum, ClearanceEnum, EducationEnum, Enums,
  ExperienceEnum, JobSeekerEducationModelEnum, JobStatusEnum, JSTravelOpportunitiesEnum, LastUpdatedWithingDaysEnum, PositionEnum,
  TravelOpportunitiesEnum
} from '../../shared/models/enums.model';
import { Industry } from '../../shared/models/industry.model';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { SkillItem } from '../../shared/models/skill.model';
import { SnackBarMessage, SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { GeneralActionService } from '../../shared/services/general-action.service';
import { GeoService } from '../../shared/services/geo.service';
import { PublicApiService } from '../../shared/services/public-api.service';
import { UtilsService } from '../../shared/services/utils.service';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { SubscriptionModel } from '../../subscription/models/subsctiption-plan.model';
import { SubscriptionService } from '../../subscription/services/subsctiption.service';
import { CoreActions } from '../actions';
import { NavigationService } from '../services/navigation.service';

export const UNAUTHORIZED = 'Unauthorized';


export class CoreStateModel extends BasePaginatedPageStateModel {
  applicationBusy: boolean;
  showGlobalSpinner: boolean;
  showGlobalSearch: boolean;
  globalSearchParam: string;
  globalLocationSearchParam: LocationSearchModel;
  settings?: object;
  changelog?: Changelog;
  countries?: object[];
  cities?: CityModel[];
  availableZips?: ZipModel[];
  states?: object[];
  enums?: Enums;
  autoApplyEnums?: object;
  statuses?: object;
  httpError?: HttpErrorResponse;
  industries: Array<Industry> | null;
  skills: SkillItem[] | null;
  favoriteJobs: Array<any>;
  appliedJobData: Array<any>;
  purchasedJobSeekers: Array<any>;
  filteredLocation: Array<any>;
  candidateStatuses: Array<any>;
}


@State<CoreStateModel>({
  name: 'core',
  defaults: {
    applicationBusy: false,
    showGlobalSpinner: false,
    showGlobalSearch: true,
    globalSearchParam: '',
    globalLocationSearchParam: null,
    settings: {validators: {password_validator: '^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$'}},
    changelog: null,
    countries: [],
    cities: [],
    availableZips: [],
    states: [],
    enums: <Enums>{},
    autoApplyEnums: {},
    statuses: {},
    httpError: null,
    industries: [],
    skills: [],
    favoriteJobs: [],
    appliedJobData: [],
    purchasedJobSeekers: [],
    filteredLocation: [],
    candidateStatuses: [],
    ...DEFAULT_PAGINATED_STATE
  },
})
export class CoreState {

  snackBarRef: MatSnackBarRef<SimpleSnackBar>;

  @Selector()
  static applicationBusy(state: CoreStateModel) {
    return state.applicationBusy;
  }

  @Selector()
  static showGlobalSpinner(state: CoreStateModel) {
    return state.showGlobalSpinner;
  }

  @Selector()
  static showGlobalSearch(state: CoreStateModel) {
    return state.showGlobalSearch;
  }

  @Selector()
  static globalSearchParam(state: CoreStateModel) {
    return state.globalSearchParam;
  }

  @Selector()
  static globalLocationSearchParam(state: CoreStateModel) {
    return state.globalLocationSearchParam;
  }

  @Selector()
  static validators(state: CoreStateModel) {
    return state.settings['validators'];
  }

  @Selector()
  static version(state: CoreStateModel) {
    return state.settings['version'];
  }

  @Selector()
  static changelog(state: CoreStateModel) {
    return state.changelog;
  }

  @Selector()
  static accountDeletionReasons(state: CoreStateModel) {
    return state.settings['account_deletion_reasons'];
  }

  @Selector()
  static countries(state: CoreStateModel): object[] {
    return state.countries;
  }

  @Selector()
  static defaultCountry(state: CoreStateModel): any {
    return state.countries[0];
  }

  @Selector()
  static citiesFiltered(state: CoreStateModel): CityModel[] {
    return state.cities;
  }

  @Selector()
  static availableZips(state: CoreStateModel): ZipModel[] {
    return state.availableZips;
  }

  @Selector()
  static filteredLocationItems(state: CoreStateModel): any[] {
    return state.states.concat(state.cities);
  }

  @Selector()
  static CandidateStatuses(state: CoreStateModel): Array<CandidateStatus> {
    return state.candidateStatuses;
  }

  @Selector()
  static enums(state: CoreStateModel): Enums {
    return state.enums;
  }

  @Selector()
  static autoApplyEnums(state: CoreStateModel): AutoapplyStatusEnum {
    return state.enums.AutoapplyStatusEnum;
  }

  @Selector()
  static AppliedDateFilterEnum(state: CoreStateModel): AppliedDateFilterEnum {
    return state.enums.AppliedDateFilterEnum;
  }

  @Selector()
  static JobStatusEnum(state: CoreStateModel): JobStatusEnum {
    return state.enums.JobStatusEnum;
  }

  @Selector()
  static ApplyStatusEnum(state: CoreStateModel): ApplyStatusEnum {
    return state.enums.ApplyStatusEnum;
  }

  @Selector()
  static CandidateRatingEnum(state: CoreStateModel): CandidateRatingEnum {
    return state.enums.CandidateRating;
  }

  @Selector()
  static CandidateStatusEnum(state: CoreStateModel): CandidateStatusEnum {
    return state.enums.CandidateStatusEnum;
  }

  @Selector()
  static PositionTypes(state: CoreStateModel): PositionEnum {
    return state.enums.PositionTypes;
  }

  @Selector()
  static EducationTypes(state: CoreStateModel): EducationEnum {
    return state.enums.EducationTypes;
  }

  @Selector()
  static JobSeekerEducationModelEnumDict(state: CoreStateModel): JobSeekerEducationModelEnum {
    return state.enums.JobSeekerEducationModelEnumDict;
  }

  @Selector()
  static ClearanceTypes(state: CoreStateModel): ClearanceEnum {
    return state.enums.ClearanceTypes;
  }

  @Selector()
  static ExperienceTypes(state: CoreStateModel): ExperienceEnum {
    return state.enums.ExperienceTypes;
  }

  @Selector()
  static LastUpdatedWithingDays(state: CoreStateModel): LastUpdatedWithingDaysEnum {
    return state.enums.LastUpdatedWithingDays;
  }

  @Selector()
  static Benefits(state: CoreStateModel): BenefitsEnum {
    return state.enums.Benefits;
  }

  @Selector()
  static TravelOpportunities(state: CoreStateModel): TravelOpportunitiesEnum {
    return state.enums.TravelOpportunities;
  }

  @Selector()
  static JSTravelOpportunities(state: CoreStateModel): JSTravelOpportunitiesEnum {
    return state.enums.JSTravelOpportunities;
  }

  @Selector()
  static industries(state: CoreStateModel): Array<Industry> {
    return state.industries;
  }

  @Selector()
  static skillsFiltered(state: string[]): any {
    return state['skills'];
  }

  @Selector()
  static allJobStatuses(state: CoreStateModel): Array<string> {
    return Object.getOwnPropertyNames(state.enums.JobStatusEnum);
  }

  @Selector()
  static favoriteJobs(state: any) {
    return state.favoriteJobs;
  }

  @Selector()
  static favoriteJobsCount(state: any) {
    return state.count;
  }

  @Selector()
  static favoriteJobsPageSize(state: any) {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: any) {
    return state.pageSizeOptions;
  }

  @Selector()
  static jobInFavorites(state: any): any {
    return (jobId: string) => {
      let result = false;
      state.favoriteJobs.some((job) => {
        if (job.id === jobId) {
          result = true;
          return true;
        }
      });
      return result;
    };
  }

  @Selector()
  static appliedJobData(state: CoreStateModel): Array<number> {
    return state.appliedJobData;
  }

  @Selector()
  static appliedJobDataIds(state: CoreStateModel): Array<number> {
    return state.appliedJobData.map(({id}) => id);
  }

  @Selector()
  static profilePurchased(state: CoreStateModel): any {
    return (profileId: number) => {
      const purchasedIds = state.purchasedJobSeekers.map(x => x.id);
      return purchasedIds.includes(profileId);
    };
  }

  @Selector()
  static stripeKey(state: CoreStateModel) {
    return state.settings['stripe_public_key'];
  }

  @Selector()
  static filteredLocation(state: CoreStateModel): any[] {
    return state.filteredLocation;
  }

  @Selector()
  static errors(state: CoreStateModel): object {
    return state.errors;
  }

  constructor(private publicApi: PublicApiService,
              private geoService: GeoService,
              private matSnackBar: MatSnackBar,
              private jssService: JobSeekerService,
              private navigationService: NavigationService,
              private generalActionService: GeneralActionService,
              private candidateService: CandidateService,
              private authSocialService: AuthSocialService,
              private subscriptionService: SubscriptionService) {
  }

  @Action(CoreActions.DispatchActionsOnInit)
  dispatchActionsOnInit(ctx, action: CoreActions.DispatchActionsOnInit) {
    return this.generalActionService.dispatchActionsOnInit();
  }

  @Action(CoreActions.SnackbarClose)
  closeSnackbar(ctx: StateContext<CoreStateModel>) {
    return of(null).pipe(
      tap(() => this.snackBarRef.dismiss()),
    );
  }

  @Action(CoreActions.SnackbarOpen)
  showSnackbar(ctx: StateContext<CoreStateModel>, action: CoreActions.SnackbarOpen) {
    const message: SnackBarMessage = action.message;
    return of(null).pipe(
      tap(() => this.snackBarRef = this.matSnackBar.open(message.message, message.action, message.config)),
      delay(message.delay),
      map(() => ctx.dispatch(new CoreActions.SnackbarClose())),
    );
  }

  @Action(CoreActions.SetInitialSettings)
  setInitialSettings(ctx: StateContext<CoreStateModel>) {
    return this.publicApi.getInitialSettings().pipe((tap(settings => {
      settings['account_deletion_reasons'].push(environment.OTHER_REASON);
      let changelog: Changelog;
      try {
        if (settings && settings['version'] && settings['version']['changelog']) {
          changelog = JSON.parse(settings['version']['changelog']);
        }
      } catch (e) {
        console.error(e);
      }
      this.authSocialService.createSocialProvidersInstances(settings['socials']);
      const state = ctx.getState();
      ctx.setState({
        ...state,
        settings: settings,
        changelog: changelog,
      });
    })));
  }

  @Action(CoreActions.SetCountries)
  getCountries(ctx: StateContext<CoreStateModel>) {
    return this.geoService.getCountries().pipe((tap(countries => {
      const state = ctx.getState();
      return ctx.setState({
        ...state,
        countries: countries['results'],
      });
    })));
  }

  @Action(CoreActions.GetCities)
  getCities(ctx: StateContext<CoreStateModel>, {params}: CoreActions.GetCities) {
    return this.geoService.getCities(params).pipe(
      debounceTime(environment.searchDebounceTime),
      tap((result: PaginatedData) => {
        const state = ctx.getState();
        return ctx.setState({
          ...state,
          cities: result.results,
        });
      }));
  }

  @Action(CoreActions.GetZips)
  getZips(ctx: StateContext<CoreStateModel>, {cityId, params}: CoreActions.GetZips) {
    return this.geoService.getZips(cityId, params).pipe((tap((result: PaginatedData) => {
      const state = ctx.getState();
      return ctx.setState({
        ...state,
        availableZips: result.results,
      });
    })));
  }

  @Action(CoreActions.GetStates)
  getStates(ctx: StateContext<CoreStateModel>, {params}: CoreActions.GetStates) {
    return this.geoService.getStates(params).pipe((tap((result: PaginatedData) => {
      const state = ctx.getState();
      ctx.setState({
        ...state,
        states: result.results,
      });
    })));
  }

  @Action(CoreActions.SetEnums)
  setEnums(ctx: StateContext<CoreStateModel>) {
    return this.publicApi.getEnums().pipe((tap(enums => {
      const state = ctx.getState();
      ctx.setState({
        ...state,
        enums: enums,
      });
    })));
  }

  @Action(CoreActions.SetGlobalSearch)
  SetGlobalSearch(ctx: StateContext<CoreStateModel>, {value}: CoreActions.SetGlobalSearch) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      showGlobalSearch: value,
    });
  }

  @Action(CoreActions.SetGlobalSearchParam)
  setGlobalSearchParam(ctx: StateContext<CoreStateModel>, {value}: CoreActions.SetGlobalSearchParam) {
    return ctx.patchState({
      globalSearchParam: value,
    });
  }

  @Action(CoreActions.SetGlobalLocationParam)
  setGlobalLocationParam(ctx: StateContext<CoreStateModel>, {value}: CoreActions.SetGlobalLocationParam) {
    return ctx.patchState({
      globalLocationSearchParam: value,
    });
  }

  @Action(CoreActions.SetAutoApplyEnums)
  SetAutoApplyEnums(ctx: StateContext<CoreStateModel>) {
    return this.publicApi.getAutoApplyEnums().pipe((tap(enums => {
      const state = ctx.getState();
      ctx.setState({
        ...state,
        autoApplyEnums: enums,
      });
    })));
  }

  @Action(CoreActions.ShowLoader)
  showLoader(ctx: StateContext<CoreStateModel>) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      applicationBusy: true,
    });
  }

  @Action(CoreActions.ShowGlobalLoader)
  showGlobalLoader(ctx: StateContext<CoreStateModel>) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      showGlobalSpinner: true,
    });
  }

  @Action(CoreActions.HideLoader)
  hideLoader(ctx: StateContext<CoreStateModel>) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      applicationBusy: false,
      showGlobalSpinner: false,
    });
  }

  @Action(CoreActions.AddHttpError400)
  addHttpError400(ctx: StateContext<CoreStateModel>, {error}: CoreActions.AddHttpError400) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      httpError: error,
    });
  }

  @Action(CoreActions.AddHttpError401)
  addHttpError401(ctx: StateContext<CoreStateModel>, {error}: CoreActions.AddHttpError401) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      httpError: error,
    });
    if (error.statusText === UNAUTHORIZED) {
      ctx.dispatch(new AuthActions.CleanAuthData());
      return this.navigationService.goToLoginPage();
    }
  }

  @Action(CoreActions.AddHttpError403)
  addHttpError403(ctx: StateContext<CoreStateModel>, {error}: CoreActions.AddHttpError403) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      httpError: error,
    });
  }

  @Action(CoreActions.AddHttpError404)
  addHttpError404(ctx: StateContext<CoreStateModel>, {error}: CoreActions.AddHttpError404) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      httpError: error,
    });
    return this.navigationService.goTo404();
  }

  @Action(CoreActions.AddHttpError500)
  addHttpError500(ctx: StateContext<CoreStateModel>, {error}: CoreActions.AddHttpError500) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      httpError: error,
    });
  }

  @Action(CoreActions.AddHttpErrorAny)
  addHttpErrorAny(ctx: StateContext<CoreStateModel>, {error}: CoreActions.AddHttpErrorAny) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      httpError: error,
    });
  }

  @Action(CoreActions.GetCandidateStatuses)
  getCandidateStatuses(ctx: StateContext<CoreStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.publicApi.getCandidateStatuses().pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          candidateStatuses: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
          candidateStatuses: []
        }));
      }),
    );
  }

  @Action(CoreActions.RedirectTo)
  redirectTo({dispatch}: StateContext<CoreStateModel>, {route, isBlank, queryParams}: CoreActions.RedirectTo) {
    if (isBlank) {
      return UtilsService.nativeWindow.open(`#/${route}/${UtilsService.getQueryParamsString(queryParams)}`);
    }
    return dispatch(new Navigate([route], null, {queryParams: queryParams}));
  }

  @Action(CoreActions.LoadIndustriesPart)
  loadIndustriesPart(ctx: StateContext<CoreStateModel>,
                     {offset, limit, ordering}: CoreActions.LoadIndustriesPart) {
    const params = {
      limit: limit,
      offset: offset,
      ordering: ordering
    };
    return this.publicApi.getIndustries(params).pipe(tap(
      (data: PaginatedData) => {
        const newIndustries: Industry[] = data.results;
        if (data.next) {
          ctx.dispatch(new CoreActions.LoadIndustriesPart(limit + offset, limit));
        }
        const state = ctx.getState();
        const existsIndustries: Industry[] = state.industries;
        const industries = [...existsIndustries, ...newIndustries];
        return ctx.setState({
          ...state,
          industries: industries,
        });
      }
    ));
  }

  @Action(CoreActions.LoadSkillsPart)
  loadSkillsPart(ctx: StateContext<CoreStateModel>,
                 {name, offset, limit, ordering}: CoreActions.LoadSkillsPart) {
    const params = {
      name: name,
      limit: limit,
      offset: offset,
      ordering: ordering
    };
    if (!params.name) {
      delete params['name'];
    }
    return this.publicApi.getSkillsFiltered(params).pipe(tap(
      (data: PaginatedData) => {
        const state = ctx.getState();
        ctx.setState({
          ...state,
          skills: data.results,
        });
      }
    ));
  }

  @Action(CoreActions.LoadIndustryData)
  loadIndustryData(ctx: StateContext<CoreStateModel>) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      industries: [],
    });
    return ctx.dispatch(new CoreActions.LoadIndustriesPart(0));
  }

  @Action(CoreActions.ListFavoriteJobs)
  listFavoriteJobs(ctx, {id, params}: CoreActions.ListFavoriteJobs) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.listFavoriteJobs(id, params).pipe(
      tap((data: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          favoriteJobs: data.results,
          count: data.count
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.SaveJobSeekerToFavorites)
  saveJobSeekerToFavorites(ctx, {id, shouldRemove}: CoreActions.SaveJobSeekerToFavorites) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.saveJobSeekerToFavorites(id, shouldRemove).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: shouldRemove ? 'Job Seeker Removed from Favorites' : 'Job Seeker Added to Favorites',
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.SaveJobToFavorites)
  saveJobToFavorites(ctx, {id, jobId}: CoreActions.SaveJobToFavorites) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.saveJobToFavorites(id, jobId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.ListFavoriteJobs(id));
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'Job Added to Favorites',
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.DeleteJobFromFavorites)
  deleteJobFromFavorites(ctx, {id, jobId}: CoreActions.DeleteJobFromFavorites) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.deleteJobFromFavorites(id, jobId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.ListFavoriteJobs(id));
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'Job Deleted from Favorites',
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.LoadAppliedJobs)
  loadAppliedJobs(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.getJobSeekerAplliedJobs().pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          appliedJobData: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          appliedJobData: [],
        }));
      }),
    );
  }

  @Action(CoreActions.LoadPurchasedJobSeekers)
  loadPurchasedJobSeekers(ctx, action: CoreActions.LoadPurchasedJobSeekers) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.getJobSeekerPurchasedList().pipe(
      tap((data: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          purchasedJobSeekers: data.results
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.PurchaseJobSeeker)
  purchaseJobSeeker(ctx, {id}: CoreActions.PurchaseJobSeeker) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.purchaseJobSeeker(id).pipe(
      tap(_ => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new CoreActions.LoadPurchasedJobSeekers());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.RateCandidate)
  rateCandidate(ctx, {id, score}: CoreActions.RateCandidate) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.candidateService.setRating(id, score).pipe(
      tap(_ => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.UpdateCandidateStatus)
  updateCandidateStatus(ctx, {id, status}: CoreActions.UpdateCandidateStatus) {
    let state: CoreStateModel = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    const statusName = state.enums.CandidateStatusEnum[status];
    const statusId = state.candidateStatuses.find(item => item.name === statusName).id;
    return this.candidateService.updateCandidateStatus(id, statusId).pipe(
      tap(_ => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.LocationSearch)
  locationSearch(ctx, {searchStr}: CoreActions.LocationSearch) {
    if (searchStr.length < environment.minimalLengthOfSearchStr) {
      return;
    }
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.geoService.filterLocation(searchStr).pipe(
      debounceTime(environment.searchDebounceTime),
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          filteredLocation: result
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.RestoreCandidateStatus)
  restoreCandidateStatus(ctx, {id}: CoreActions.RestoreCandidateStatus) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.candidateService.restoreCandidateStatus(id).pipe(
      tap(_ => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error,
        }));
      }),
    );
  }

  @Action(CoreActions.UpdateUserPlanSubscription)
  updateUserPlanSubscription(ctx) {
    ctx.patchState({
      status: 'pending',
    });
    return this.subscriptionService.getActivePlan().pipe(
      tap((activeSubscription: SubscriptionModel) => {
        ctx.patchState({
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new AuthActions.UpdateSubsctiption(activeSubscription))
          .subscribe(() => this.navigationService.goToCompanyDashboardPage());
      }),
      catchError(error => {
        return of(ctx.patchState({
          status: 'error',
          errors: error,
        }));
      }),
    );
  }
}
