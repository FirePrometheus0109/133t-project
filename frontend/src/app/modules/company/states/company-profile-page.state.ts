import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Photo } from '../../shared/models';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { PublicApiService } from '../../shared/services/public-api.service';
import { CompanyProfilePageActions } from '../actions';
import { CompanyProfile } from '../models/company-profile.model';
import { CompanyService } from '../services/company.service';
import { JobService } from '../services/job.service';


class CompanyProfilePageStateModel {
  status: string;
  errors: object;
  initialData: CompanyProfile;
  photo: Photo;
  jobs: Array<any>;
}


export const DEFAULT_COMPANY_PROFILE_PAGE_STATE = {
  status: '',
  errors: null,
  initialData: null,
  photo: new Photo(),
  jobs: [],
};


@State<CompanyProfilePageStateModel>({
  name: 'CompanyProfilePage',
  defaults: DEFAULT_COMPANY_PROFILE_PAGE_STATE,
})
export class CompanyProfilePageState {
  @Selector()
  static photo(state: any) {
    return state.photo;
  }

  @Selector()
  static pending(state: CompanyProfilePageStateModel) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: CompanyProfilePageStateModel) {
    return state.errors;
  }

  @Selector()
  static initialData(state: CompanyProfilePageStateModel) {
    return state.initialData;
  }

  @Selector()
  static jobs(state: CompanyProfilePageStateModel) {
    return state.jobs;
  }

  constructor(private companyService: CompanyService,
              private publicApiService: PublicApiService,
              private jobService: JobService) {
  }

  @Action(CompanyProfilePageActions.PartialUpdate)
  partialUpdate(ctx, {part, id, data}: CompanyProfilePageActions.PartialUpdate) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyService.partialUpdateCompanyProfile(id, data).pipe(
      tap(() => {
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
          errors: error.error,
        }));
      }),
    );
  }

  @Action(CompanyProfilePageActions.UpdateLogo)
  updateLogo(ctx, {id, data}: CompanyProfilePageActions.UpdateLogo) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      photo: data,
    });
  }

  @Action(CompanyProfilePageActions.LoadInitialData)
  loadInitialData(ctx, {id}: CompanyProfilePageActions.LoadInitialData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyService.getCompanyProfile(id).pipe(
      tap((result: CompanyProfile) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          initialData: result,
          photo: result.photo
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          initialData: null,
        }));
      }),
    );
  }

  @Action(CompanyProfilePageActions.LoadPublicInitialData)
  loadPublicInitialData(ctx, {id}: CompanyProfilePageActions.LoadPublicInitialData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.publicApiService.getPublicCompanyProfile(id).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          initialData: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          initialData: null,
        }));
      }),
    );
  }

  @Action(CompanyProfilePageActions.LoadJobsData)
  loadJobsData(ctx, {id}: CompanyProfilePageActions.LoadJobsData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getJobs({company_id: id}).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          jobs: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          jobs: [],
        }));
      }),
    );
  }

  @Action(CompanyProfilePageActions.LoadPublicJobsData)
  loadPublicJobsData(ctx, {id}: CompanyProfilePageActions.LoadPublicJobsData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.publicApiService.getPublicJobsData(id).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          jobs: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          jobs: [],
        }));
      }),
    );
  }
}
