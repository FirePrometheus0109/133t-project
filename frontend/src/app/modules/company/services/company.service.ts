import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';
import {JobStatus} from '../../shared/enums/job-statuses';
import {Photo} from '../../shared/models';
import {SortingFilter} from '../../shared/models/filters.model';
import {ApiService} from '../../shared/services/api.service';
import {CompanyProfile} from '../models/company-profile.model';
import {ReportsGraphRequestData} from '../models/company-reports.model';


@Injectable()
export class CompanyService {
  route = 'company';
  job = 'job';
  routeImg = 'photo';
  report = 'report';
  usersActivity = 'users-activity';
  workflowStats = 'candidates-workflow-stats';
  events = 'events';
  jobOwners = 'job-owners';
  dummy = 'create_dummy';

  constructor(private api: ApiService) {
  }

  setDummyJob(data) {
    return this.api.post(`${this.job}/${this.dummy}`, data);
  }

  getCompanyProfile(id: number) {
    return this.api.getById(`${this.route}`, id).pipe(
      map(data => {
        return new CompanyProfile().deserialize(data);
      }));
  }

  getCompanyJob() {
    return this.api.get(`${this.job}`);
  }

  getActiveCompanyJob() {
    return this.api.get(`${this.job}`, {status: JobStatus.ACTIVE});
  }

  partialUpdateCompanyProfile(id: number, data: any) {
    return this.api.patchById(`${this.route}`, id, data);
  }

  createNewJob(data: any) {
    return this.api.post(`${this.job}`, data);
  }

  updateCompanyLogo(id: number, data: Photo) {
    return this.api.patch(`${this.route}/${id}/${this.routeImg}`, data);
  }

  getCompanyPhotoRoute(id: number): string {
    return `${this.api.getFullApiRoute(this.route, id)}${this.routeImg}/`;
  }

  getReportData(reportData: ReportsGraphRequestData) {
    return this.api.get(`${this.route}/${reportData.id}/${this.report}`, reportData);
  }

  getUserActivity(id: number) {
    return this.api.get(`${this.route}/${id}/${this.usersActivity}`);
  }

  getWorkflowStats(period?: SortingFilter) {
    let data = {};
    if (period) {
      data = {created_at: period.value, all: true};
    }
    return this.api.get(`${this.workflowStats}`, data);
  }

  getAllWorkflowStats() {
    return this.api.get(`${this.workflowStats}`, {all: true});
  }

  getJobAuthors() {
    return this.api.get(`${this.jobOwners}`);
  }
}
