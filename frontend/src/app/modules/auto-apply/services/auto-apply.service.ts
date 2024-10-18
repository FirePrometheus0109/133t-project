import { Injectable } from '@angular/core';
import { CoverLetterApplyData } from '../../shared/models/cover-letter.model';
import { ApiService } from '../../shared/services/api.service';
import { LocationFilterService } from '../../shared/services/location-filter.service';
import { UtilsService } from '../../shared/services/utils.service';


@Injectable()
export class AutoApplyService {
  route = 'autoapply';
  job = 'job';
  exclude = 'exclude';
  cityId = 'city_id';
  stateId = 'state_id';
  location = 'location';
  start = 'start';
  stop = 'stop';
  restart = 'restart';
  apply = 'apply';
  coverLetter = 'cover-letter';
  applied = 'APPLIED';
  needReview = 'NEED_REVIEW';
  newJob = 'NEW';
  viewed = 'VIEWED';

  constructor(private api: ApiService) {
  }

  getAutoApplyList() {
    return this.api.get(`${this.route}`);
  }

  getAutoApply(id: number) {
    return this.api.getById(`${this.route}`, id);
  }

  getAutoApplyJobsList(params?) {
    return this.api.get(`${this.route}/${this.job}`, params);
  }

  getAutoApplyJobs(autoApplyId) {
    return this.api.get(`${this.route}/${autoApplyId}/${this.job}`);
  }

  getAutoApplyJobDetails(jobId) {
    return this.api.getById(`${this.route}/${this.job}`, jobId);
  }

  getAutoApplyResult(autoApplyId) {
    return this.api.get(`${this.route}/${autoApplyId}/${this.job}`);
  }

  createAutoApply(params) {
    return this.api.post(`${this.route}`, params);
  }

  updateAutoApply(params, autoApplyId) {
    return this.api.patchById(`${this.route}`, autoApplyId, params);
  }

  deleteAutoApplyItem(autoApplyId) {
    return this.api.deleteById(`${this.route}`, autoApplyId);
  }

  startAutoApply(autoApplyId: number, appliedJobs: any) {
    return this.api.put(`${this.route}/${autoApplyId}/${this.start}`, appliedJobs);
  }

  stopAutoApply(autoApplyId: number) {
    return this.api.put(`${this.route}/${autoApplyId}/${this.stop}`, {});
  }

  restartAutoApply(autoApplyId: number) {
    return this.api.put(`${this.route}/${autoApplyId}/${this.restart}`, {});
  }

  applyForNewJob(autoApplyId: number, jobId: number) {
    return this.api.put(`${this.route}/${autoApplyId}/${this.job}/${jobId}/${this.apply}`, {});
  }

  setCoverLetterForApply(autoApplyId: number, jobId: number, coverLetterData: CoverLetterApplyData) {
    return this.api.put(`${this.route}/${autoApplyId}/${this.job}/${jobId}/${this.coverLetter}`, coverLetterData);
  }

  setQueryParams(params) {
    const result = [];
    for (const key in params) {
      if (params.hasOwnProperty(key)) {
        if (key === this.exclude) {
          result.push(key + '=' + params[key].join());
        } else if (key === this.location) {
          const locationItem = params[key];
          if (locationItem) {
            (locationItem.state) ? result.push(`city_id=${locationItem.id}`) : result.push(`state_id=${locationItem.id}`);
          }
        } else {
          result.push(key + '=' + params[key]);
        }
      }
    }
    return result.join('&');
  }

  getQueryParams(params) {
    const result = {};
    const firstStage = params.split('&');
    for (const item of firstStage) {
      const secondStage = item.split('=');
      const objToAdd = {};
      if (secondStage[0] === this.exclude) {
        objToAdd[secondStage[0]] = secondStage[1].split();
      } else if (secondStage[0] === this.cityId || secondStage[0] === this.stateId) {
        continue;
      } else {
        objToAdd[secondStage[0]] = secondStage[1];
      }
      Object.assign(result, objToAdd);
    }
    return result;
  }

  getQueryParamsForResult(params: object) {
    const result = [];
    for (const key in params) {
      if (params.hasOwnProperty(key)) {
        if (key && params[key]) {
          if (UtilsService.isObject(params[key])) {
            result.push(LocationFilterService.buildLocationString(params[key]));
          } else {
            result.push(params[key]);
          }
        }
      }
    }
    return result.join();
  }

  divideAutoApplyResult(result: any) {
    const applied = [];
    const need_review = [];
    const new_jobs = [];
    const viewed = [];
    result.forEach((item) => {
      if (item.apply_job_status === this.applied) {
        applied.push(item);
      } else if (item.apply_job_status === this.needReview) {
        need_review.push(item);
      } else if (item.apply_job_status === this.newJob) {
        new_jobs.push(item);
      } else if (item.apply_job_status === this.viewed) {
        viewed.push(item);
      }
    });
    return {applied, need_review, new_jobs, viewed};
  }
}
