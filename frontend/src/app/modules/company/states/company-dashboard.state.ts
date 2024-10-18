import { Action, Selector, State, StateContext, Store } from '@ngxs/store';
import { forkJoin, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { AuthState } from '../../auth/states/auth.state';
import { CandidateService } from '../../candidate/services/candidate.service';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { SetSubscriptionActions } from '../../subscription/actions';
import { CompanyDashboardActions } from '../actions';
import { CandidateActivityModel } from '../models/candidate-activity.model';
import { ActivityStats } from '../models/company-reports.model';
import { JobItem } from '../models/job.model';
import { ScoreCardMode } from '../models/scorecard-mode.model';
import { CompanyUserService } from '../services/company-user.service';
import { CompanyService } from '../services/company.service';
import { JobService } from '../services/job.service';


export class CompanyDashboardStateModel extends BasePaginatedPageStateModel {
  status: string;
  errors: object;
  candidatesActivity: CandidateActivityModel[];
  newestJobs: JobItem[];
  statCardData: Array<ActivityStats>;
  allStatCardData: Array<ActivityStats>;
  statCardDataIds: Array<number>;
  statCardMode: ScoreCardMode;
}


export const DEFAULT_COMPANY_DASHBOARD_STATE = Object.assign({
  status: '',
  errors: null,
  candidatesActivity: [],
  newestJobs: [],
  statCardData: [],
  allStatCardData: [],
  statCardDataIds: [],
  statCardMode: ScoreCardMode.VIEW
}, DEFAULT_PAGINATED_STATE);


@State<CompanyDashboardStateModel>({
  name: 'CompanyDashboardState',
  defaults: DEFAULT_COMPANY_DASHBOARD_STATE
})
export class CompanyDashboardState {
  @Selector()
  static count(state: CompanyDashboardStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: CompanyDashboardStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: CompanyDashboardStateModel): number[] {
    return state.pageSizeOptions;
  }

  @Selector()
  static candidatesActivity(state: CompanyDashboardStateModel): CandidateActivityModel[] {
    return state.candidatesActivity;
  }

  @Selector()
  static newestJobs(state: CompanyDashboardStateModel): JobItem[] {
    return state.newestJobs;
  }

  @Selector()
  static statCardData(state: CompanyDashboardStateModel): ActivityStats[] {
    return state.statCardData;
  }

  @Selector()
  static allStatCardData(state: CompanyDashboardStateModel): ActivityStats[] {
    return state.allStatCardData;
  }

  @Selector()
  static statCardDataIds(state: CompanyDashboardStateModel): number[] {
    return state.statCardDataIds;
  }

  @Selector()
  static statCardMode(state: CompanyDashboardStateModel): ScoreCardMode {
    return state.statCardMode;
  }

  constructor(private jobService: JobService, private candidateService: CandidateService,
              private companyService: CompanyService, private companyUserService: CompanyUserService, private store: Store) {
  }

  @Action(CompanyDashboardActions.LoadInitialData)
  loadInitialData(ctx) {
    const state = ctx.getState();
    if (this.store.selectSnapshot(AuthState.isSubscriptionExpired)) {
      ctx.dispatch(new SetSubscriptionActions.LoadAllPlans()).subscribe(() => {
        this.provideCurrentPlanSelection(ctx);
      });
    } else {
      return this.provideInitialActions(ctx, state);
    }
  }

  @Action(CompanyDashboardActions.LoadScoreCardData)
  loadScoreCardData(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.companyService.getWorkflowStats().pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          statCardData: result,
          statCardDataIds: result.map(item => item.id),
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

  @Action(CompanyDashboardActions.ToggleScoreCardMode)
  toggleScoreCardMode(ctx, {}) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      statCardMode: state.statCardMode === ScoreCardMode.VIEW ? ScoreCardMode.EDIT : ScoreCardMode.VIEW,
    });
  }

  @Action(CompanyDashboardActions.SetScoreCardSettings)
  setScoreCardSettings(ctx, {cardIds}: CompanyDashboardActions.SetScoreCardSettings) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.setCandidateStatuses(cardIds).pipe(
      tap((result: Array<any>) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          statCardDataIds: result.map(item => item.id)
        });
        return forkJoin(
          ctx.dispatch(new CompanyDashboardActions.LoadScoreCardData()),
          ctx.dispatch(new CompanyDashboardActions.ToggleScoreCardMode())
        );
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

  @Action(CompanyDashboardActions.LoadCandidatesActivity)
  loadCandidatesActivity(ctx: StateContext<CompanyDashboardStateModel>, {params}: CompanyDashboardActions.LoadCandidatesActivity) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.candidateService.getCandidatesActivityForDashboard(params).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          candidatesActivity: result.results,
          count: result.count,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          candidatesActivity: [],
        }));
      }),
    );
  }

  @Action(CompanyDashboardActions.SetCurrentPagination)
  setCurrentPagination(ctx, {params}: CompanyDashboardActions.SetCurrentPagination) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      ...params
    });
  }

  @Action(CompanyDashboardActions.LoadNewestJobs)
  loadNewestJobs(ctx: StateContext<CompanyDashboardStateModel>, {params}: CompanyDashboardActions.LoadNewestJobs) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getJobs(params).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          newestJobs: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          newestJobs: [],
        }));
      }),
    );
  }

  @Action(CompanyDashboardActions.LoadAllScoreCardData)
  loadAllScoreCardData(ctx, {}: CompanyDashboardActions.LoadAllScoreCardData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.companyService.getAllWorkflowStats().pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          allStatCardData: result,
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

  private provideCurrentPlanSelection(ctx) {
    if (this.store.selectSnapshot(AuthState.isSubsctiptionPurchased)) {
      ctx.dispatch(new SetSubscriptionActions.LoadCurrentPlan());
    } else {
      ctx.dispatch(new SetSubscriptionActions.SetFirstPlanSelected());
    }
  }

  private provideInitialActions(ctx, state) {
    return forkJoin([
      ctx.dispatch(new SetSubscriptionActions.LoadAllPlans()),
      ctx.dispatch(new SetSubscriptionActions.LoadCurrentPlan()),
      ctx.dispatch(new CompanyDashboardActions.LoadCandidatesActivity({limit: state.limit, offset: state.offset})),
      ctx.dispatch(new CompanyDashboardActions.LoadNewestJobs(environment.newestJobsParamsOnDashboard)),
      ctx.dispatch(new CompanyDashboardActions.LoadScoreCardData()),
    ]);
  }
}
