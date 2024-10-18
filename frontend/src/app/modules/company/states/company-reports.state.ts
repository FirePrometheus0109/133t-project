import { Action, Selector, State } from '@ngxs/store';
import * as moment from 'moment';
import { forkJoin, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { DateBasis } from '../../shared/enums/company-reports.enums';
import { DateTimeHelper } from '../../shared/helpers/date-time.helper';
import { SortingFilter } from '../../shared/models/filters.model';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { UtilsService } from '../../shared/services/utils.service';
import { CompanyReportsActions } from '../actions';
import {
  ActivityStats, ReportGraphPoint, ReportsGraphData,
  ReportsGraphRequestData, UserActivityData
} from '../models/company-reports.model';
import { CompanyService } from '../services/company.service';

import { environment } from '../../../../environments/environment';


class CompanyReportsStateModel {
  status: string;
  errors: object;
  graphData: Array<ReportsGraphData>;
  graphBasic: DateBasis;
  fromDate: string;
  companyId: number;
  recruiterActivityData: Array<UserActivityData>;
  workflowStatsFilter: SortingFilter;
  workflowStatsData: Array<ActivityStats>;
}


export const DEFAULT_COMPANY_REPORTS_STATE = {
  status: '',
  errors: null,
  graphData: [],
  graphBasic: DateBasis.DAY,
  companyId: null,
  fromDate: moment().utc().startOf(DateBasis.DAY).format(),
  recruiterActivityData: [],
  workflowStatsFilter: null,
  workflowStatsData: [],
};

export const WORK_FLOW_SORTING_FILTER = {
  TWO_WEEKS: '2 weeks',
  THIRTY_DAYS: '30 days',
  SIXTY_DAYS: '60 days'
};

export const dateSwitchStep = 1;


@State<CompanyReportsStateModel>({
  name: 'CompanyReportsState',
  defaults: DEFAULT_COMPANY_REPORTS_STATE,
})
export class CompanyReportsState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static graphData(state: CompanyReportsStateModel) {
    return state.graphData;
  }

  @Selector()
  static graphBasic(state: CompanyReportsStateModel) {
    return state.graphBasic;
  }

  @Selector()
  static companyId(state: CompanyReportsStateModel) {
    return state.companyId;
  }

  @Selector()
  static fromDate(state: CompanyReportsStateModel) {
    return state.fromDate;
  }

  @Selector()
  static recruiterActivityData(state: CompanyReportsStateModel) {
    return state.recruiterActivityData;
  }

  @Selector()
  static workflowStatsData(state: CompanyReportsStateModel) {
    return state.workflowStatsData;
  }

  @Selector()
  static workflowStatsFilter(state: CompanyReportsStateModel) {
    return state.workflowStatsFilter;
  }

  @Selector()
  static workflowFilter() {
    const sortingKeys = Object.keys(WORK_FLOW_SORTING_FILTER);
    return sortingKeys.reduce((newResultArray, item) => {
      return [
        ...newResultArray,
        new SortingFilter(item, WORK_FLOW_SORTING_FILTER[item])
      ];
    }, []);
  }

  constructor(private companyService: CompanyService) {
  }

  @Action(CompanyReportsActions.InitCompanyId)
  InitCompanyId(ctx, {companyId}: CompanyReportsActions.InitCompanyId) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      companyId: companyId,
    });
  }

  @Action(CompanyReportsActions.ChangeGraphDateBasic)
  changeGraphBasic(ctx, {basic}: CompanyReportsActions.ChangeGraphDateBasic) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      graphBasic: basic,
      fromDate: DEFAULT_COMPANY_REPORTS_STATE.fromDate
    });
    return ctx.dispatch(new CompanyReportsActions.LoadGraphData());
  }

  @Action(CompanyReportsActions.InitReportData)
  InitReportData(ctx) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      fromDate: DEFAULT_COMPANY_REPORTS_STATE.fromDate,
      workflowStatsFilter: CompanyReportsState.workflowFilter()[0],
    });
    return forkJoin(ctx.dispatch(new CompanyReportsActions.LoadGraphData()),
      ctx.dispatch(new CompanyReportsActions.LoadRecruiterActivity()),
      ctx.dispatch(new CompanyReportsActions.LoadWorkflowStats()));
  }

  @Action(CompanyReportsActions.MoveGraphToPast)
  moveGraphToPast(ctx) {
    const state: CompanyReportsStateModel = ctx.getState();
    const newDate = moment(state.fromDate).subtract(dateSwitchStep, state.graphBasic).format();

    ctx.setState({
      ...state,
      fromDate: newDate,
    });

    return ctx.dispatch(new CompanyReportsActions.LoadGraphData());
  }

  @Action(CompanyReportsActions.MoveGraphToFuture)
  moveGraphToFuture(ctx) {
    const state: CompanyReportsStateModel = ctx.getState();
    const newDate = moment(state.fromDate).add(dateSwitchStep, state.graphBasic).format();

    ctx.setState({
      ...state,
      fromDate: newDate,
    });

    return ctx.dispatch(new CompanyReportsActions.LoadGraphData());

  }

  @Action(CompanyReportsActions.LoadRecruiterActivity)
  loadRecruiterActivity(ctx) {
    let state: CompanyReportsStateModel = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyService.getUserActivity(state.companyId).pipe(
      tap((result: PaginatedData) => {
        return ctx.setState({
          ...ctx.getState(),
          status: 'done',
          errors: null,
          recruiterActivityData: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          recruiterActivityData: {},
        }));
      }),
    );
  }

  @Action(CompanyReportsActions.LoadWorkflowStats)
  loadWorkflowStats(ctx) {
    let state: CompanyReportsStateModel = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyService.getWorkflowStats(state.workflowStatsFilter).pipe(
      tap((result) => {
        return ctx.setState({
          ...ctx.getState(),
          status: 'done',
          errors: null,
          workflowStatsData: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          workflowStatsData: [],
        }));
      }),
    );
  }

  @Action(CompanyReportsActions.ChangeWorkflowFilter)
  changeWorkflowFilter(ctx, {filter}: CompanyReportsActions.ChangeWorkflowFilter) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      workflowStatsFilter: filter,
    });
    return ctx.dispatch(new CompanyReportsActions.LoadWorkflowStats());
  }

  @Action(CompanyReportsActions.LoadGraphData)
  loadGraphData(ctx) {
    const state: CompanyReportsStateModel = ctx.getState();
    const reportData = this.getReportRequestData(state);

    ctx.patchState({
      status: 'pending',
    });
    return this.companyService.getReportData(reportData).pipe(
      tap((result) => {
        const newResult = result.reduce((newResultArray, item) => {
          return [
            ...newResultArray,
            {
              ...item,
              series: item.series.map(series => {
                return UtilsService.renameProp([{oldProp: 'date', newProp: 'name'}, {oldProp: 'count', newProp: 'value'}], series);
              })
            }];
        }, []);
        return ctx.patchState({
          status: 'done',
          errors: null,
          graphData: this.fillEmptyDateByNull(newResult, reportData),
        });
      }),
      catchError(error => {
        ctx.patchState({
          status: 'error',
          errors: error.error,
          initialData: null,
        });
        return of(error);
      }),
    );

  }

  private getReportRequestData(state: CompanyReportsStateModel) {
    const mReqFromDate = moment(state.fromDate).utc().subtract(environment.reportGraphDateLength, state.graphBasic);
    const mReqToDate = moment(state.fromDate).utc().endOf(state.graphBasic);
    return {
      id: state.companyId,
      basis: state.graphBasic,
      to_date: mReqToDate.format(),
      from_date: mReqFromDate.format()
    };
  }

  private fillEmptyDateByNull(incomingReportsData: Array<ReportsGraphData>, reportData: ReportsGraphRequestData) {
    let dates: Array<any>;

    switch (reportData.basis) {
      case (DateBasis.DAY):
        dates = DateTimeHelper.enumerateDaysBetweenDates(reportData.from_date, reportData.to_date);
        break;
      case (DateBasis.MONTH):
        dates = DateTimeHelper.enumerateMonthBetweenDates(reportData.from_date, reportData.to_date);
        break;
      case (DateBasis.WEEK):
        dates = DateTimeHelper.enumerateWeeksBetweenDates(reportData.from_date, reportData.to_date);
        break;
      default:
        dates = DateTimeHelper.enumerateDaysBetweenDates(reportData.from_date, reportData.to_date);
        break;
    }

    return incomingReportsData.reduce((newResultArray, item) => {
      return [
        ...newResultArray,
        {
          ...item,
          series: this.updateSeries(item.series, dates)
        }];
    }, []);
  }

  private updateSeries(itemSeries: ReportGraphPoint[], dates: string[]) {
    return dates.reduce((newResultArray, dateItem) => {
      const existingValue = itemSeries.find((item) => DateTimeHelper.isDateEqual(item.name, dateItem));
      if (existingValue) {
        return [
          ...newResultArray,
          {
            ...existingValue,
            name: dateItem
          }
        ];
      } else {
        return [
          ...newResultArray,
          {
            ...new ReportGraphPoint(dateItem)
          }
        ];
      }
    }, []);
  }
}
