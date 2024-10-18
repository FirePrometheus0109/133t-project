import { Injectable } from '@angular/core';
import { ApiService } from '../../shared/services/api.service';
import { AnswerData } from '../../survey/models/answer.model';


@Injectable()
export class JobService {
  private public = 'public';
  private shared = 'shared';
  private share = 'share';
  private route = 'job';
  private deleteList = 'delete-list';
  private candidates = 'candidates';
  private jobSeeker = 'job_seeker';
  private answer = 'answer';
  private restore = 'restore';
  private viewers = 'viewers';
  private exportCSV = 'export-csv';
  private comment = 'comment';
  private reapply = 'reapply';

  constructor(private api: ApiService) {
  }

  public getJobById(id: number) {
    return this.api.getById(`${this.route}`, id);
  }

  public getPublicJobByUid(uid: string) {
    return this.api.get(`${this.public}/${this.shared}-${this.route}/${uid}`);
  }

  public shareJobByEmail(id: number, data: {email: string, url: string}) {
    return this.api.put(`${this.route}/${id}/${this.share}`, data);
  }

  public updateJob(id: number, data: any) {
    return this.api.putById(`${this.route}`, id, data);
  }

  public getJobs(params?: object) {
    return this.api.get(`${this.route}`, params);
  }

  public deleteJob(jobId: number) {
    return this.api.deleteById(`${this.route}`, jobId);
  }

  public deleteJobList(jobIds: number[]) {
    return this.api.post(`${this.route}/${this.deleteList}`, {jobs: jobIds});
  }

  public downloadJobList(jobIds: number[]) {
    return this.api.getFiles(`${this.route}/${this.exportCSV}`, {params: {jobs: jobIds.join()}, responseType: 'blob'});
  }

  public restoreJob(jobId: number, data?: object) {
    return this.api.put(`${this.route}/${jobId}/${this.restore}`, data);
  }

  public getCandidates(id: number, params?: Object) {
    return this.api.get(`${this.route}/${id}/${this.candidates}`, params);
  }

  public getCandidateAnswer(jobId: number, jobSeekerId: number) {
    return this.api.get(`${this.route}/${jobId}/${this.jobSeeker}/${jobSeekerId}/${this.answer}`);
  }

  public postAnswersForJob(jobId: number, answerDataList: Array<AnswerData>) {
    return this.api.post(`${this.route}/${jobId}/${this.answer}`, answerDataList);
  }

  public getViewers(jobId: number, limit: number, offset: number) {
    return this.api.get(`${this.route}/${jobId}/${this.viewers}`, {limit: limit, offset: offset});
  }

  public getCommentsForJob(jobId: number, params?: any) {
    return this.api.get(`${this.route}/${jobId}/${this.comment}`, params);
  }

  public reapplyForJob(jobId: number, params?: any) {
    return this.api.post(`${this.route}/${jobId}/${this.reapply}`, params);
  }
}
