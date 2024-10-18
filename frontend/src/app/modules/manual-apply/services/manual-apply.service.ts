import { Injectable } from '@angular/core';
import { CoverLetterApplyData } from '../../shared/models/cover-letter.model';
import { ApiService } from '../../shared/services/api.service';


@Injectable({
  providedIn: 'root',
})
export class ManualApplyService {
  apply = 'apply';
  job = 'job';

  constructor(private api: ApiService) {
  }

  applyForJob(jobId: number, coverLetterData?: CoverLetterApplyData) {
    const preparedData = {job: jobId};
    if (coverLetterData) {
      Object.assign(preparedData, coverLetterData);
    }
    return this.api.post(`${this.apply}`, preparedData);
  }

  getJobData(jobId: number) {
    return this.api.getById(`${this.job}`, jobId);
  }
}
