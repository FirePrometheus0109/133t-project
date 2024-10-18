import { Injectable } from '@angular/core';
import { CandidateRatingEnum } from '../../shared/models/enums.model';
import { ApiService } from '../../shared/services/api.service';


@Injectable({
  providedIn: 'root',
})
export class CandidateService {
  route = 'candidate';
  assignment = 'assignment';
  rating = 'rating';
  status = 'status';
  restoring = 'restoring';
  quickView = 'quick-view';
  quickList = 'candidates-quick-list';
  candidatesActivity = 'candidates/activities';
  exportToCSV = 'export-to-csv';

  constructor(private api: ApiService) {
  }

  assignCandidate(jobSeekersIds: Array<number>, jobsIds: Array<number>) {
    const data = {job_seekers: jobSeekersIds, jobs: jobsIds};
    return this.api.post(`${this.route}/${this.assignment}`, data);
  }

  setRating(id: number, rating: CandidateRatingEnum) {
    const data = {rating: rating};
    return this.api.put(`${this.route}/${id}/${this.rating}`, data);
  }

  updateCandidateStatus(id: number, statusID: string) {
    const data = {status: statusID};
    return this.api.patch(`${this.route}/${id}/${this.status}`, data);
  }

  restoreCandidateStatus(id: number) {
    return this.api.post(`${this.route}/${id}/${this.restoring}`);
  }

  getCandidateList(params?: object) {
    return this.api.get(`${this.route}`, params);
  }

  getCandidateForQuickView(params?: object) {
    return this.api.get(`${this.route}/${this.quickView}`, params);
  }

  getCandidate(candidateId: number) {
    return this.api.getById(`${this.route}`, candidateId);
  }

  getCandidatesActivityForDashboard(params: object) {
    return this.api.get(`${this.candidatesActivity}`, params);
  }

  getCandidatesQuickList(params?: object) {
    return this.api.get(`${this.quickList}`, params);
  }

  downloadCandidatesList(selectedCandidates: number[]) {
    return this.api.getFiles(`${this.route}/${this.exportToCSV}`, {params: {candidates: selectedCandidates.join()}, responseType: 'blob'});
  }
}
