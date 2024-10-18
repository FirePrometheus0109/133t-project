import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export const PUBLIC_ROUTE = 'public';


@Injectable({
  providedIn: 'root',
})
export class PublicApiService {
  route = PUBLIC_ROUTE;
  initialSettings = 'initial-settings';
  enums = 'enums';
  autoapply = 'autoapply';
  industry = 'industry';
  skill = 'skill';
  statuses = 'statuses';
  allSkills = 'all-skills';
  skills = 'skills';
  company = 'company';
  companies = 'companies';
  job = 'job';
  candidateStatuses = 'candidate-statuses';

  constructor(private api: ApiService) {
  }

  getInitialSettings(): Observable<{validators: object}> {
    return this.api.get(`${this.route}/${this.initialSettings}`);
  }

  getEnums(): Observable<any> {
    return this.api.get(`${this.route}/${this.enums}`);
  }

  getAutoApplyEnums(): Observable<any> {
    return this.api.get(`${this.autoapply}/${this.enums}`);
  }

  getStatuses(): Observable<any> {
    return this.api.get(`${this.statuses}`);
  }

  getIndustries(data): Observable<any> {
    return this.api.get(`${this.route}/${this.industry}`, data);
  }

  getSkillsFiltered(data): Observable<any> {
    return this.api.get(`${this.route}/${this.skills}`, data);
  }

  getCompanies(limit: number, offset: number, search?: string) {
    let params;
    search ? params = {limit: limit, offset: offset, search: search} : params = {limit: limit, offset: offset};
    return this.api.get(`${this.route}/${this.company}`, params);
  }

  getCompaniesForFilter(search?: string) {
    return this.api.get(`${this.enums}/${this.companies}`, {search});
  }

  getPublicCompanyProfile(companyId: number) {
    return this.api.get(`${this.route}/${this.company}/${companyId}`);
  }

  getPublicJobsData(companyId: number) {
    return this.api.get(`${this.route}/${this.job}`, {company_id: companyId});
  }

  getCandidateStatuses() {
    return this.api.get(`${this.route}/${this.candidateStatuses}`);
  }
}
