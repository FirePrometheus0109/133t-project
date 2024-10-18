import { DateBasis } from '../../shared/enums/company-reports.enums';
import { DateTimeHelper } from '../../shared/helpers/date-time.helper';


export class ReportsGraphRequestData {
  id: number;
  from_date: string;
  to_date: string;
  basis: DateBasis;

  constructor(to_date: Date, basis: DateBasis, id: number) {
    this.to_date = to_date.toJSON();
    this.basis = basis;
    this.id = id;
    this.from_date = DateTimeHelper.getGraphFirstDate(to_date, basis).toJSON();
  }
}

export class ReportGraphPoint {
  name: string;
  value: number;

  constructor(date: string) {
    this.name = date;
    this.value = 0;
  }
}

export interface ReportsGraphData {
  name: string;
  series: Array<ReportGraphPoint>;
}

export interface ReportUserData {
  id: number;
  name: string;
}

export interface ActivityStats {
  id: number;
  name: string;
  n_candidates: number;
}

export interface UserActivityData {
  is_online: boolean;
  user: ReportUserData;
  stats: ActivityStats;
}
