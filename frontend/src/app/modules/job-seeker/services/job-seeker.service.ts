import { Injectable } from '@angular/core';
import { CoverLetterItem } from '../../shared/models/cover-letter.model';
import { CertificationItem, EducationItem } from '../../shared/models/education.model';
import { JobItem } from '../../shared/models/experience.model';
import { ApiService } from '../../shared/services/api.service';


@Injectable({
  providedIn: 'root',
})
export class JobSeekerService {
  public = 'public';
  route = 'job-seeker';
  alternativeRoute = 'job-seekers';
  routeImg = 'photo';
  educations = 'educations';
  certifications = 'certifications';
  jobExperience = 'job-experience';
  coverLetter = 'cover-letter';
  favorites = 'favorites';
  favoritesJobs = 'favorites-jobs';
  appliedJobs = 'applied-jobs';
  purchase = 'purchase';
  comment = 'comment';
  viewers = 'viewers';
  autoAppliesStats = 'autoapplies/stats';

  constructor(private api: ApiService) {
  }

  getJobSeekerList(params?: object) {
    return this.api.get(`${this.route}`, params);
  }

  getJobSeekerPurchasedList(params?: object) {
    const data = {...params, purchased: true};
    return this.api.get(`${this.route}`, data);
  }

  getJobSeekerSavedList(params?: object) {
    const data = {...params, saved: true};
    return this.api.get(`${this.route}`, data);
  }

  getJobSeekerPhotoRoute(id: number): string {
    return `${this.api.getFullApiRoute(this.route, id)}${this.routeImg}/`;
  }

  getJobSeekerProfile(id: number) {
    return this.api.getById(`${this.route}`, id);
  }

  getJobSeekerPublicProfile(uid: string) {
    return this.api.get(`${this.public}/${this.route}/${uid}`);
  }

  getJobSeekerEducations(id: number) {
    return this.api.get(`${this.route}/${id}/${this.educations}`);
  }

  postJobSeekerNewEducation(id: number, data: EducationItem) {
    return this.api.post(`${this.route}/${id}/${this.educations}`, data);
  }

  deleteJobSeekerEducation(id: number, educationId: number) {
    return this.api.delete(`${this.route}/${id}/${this.educations}/${educationId}`);
  }

  updateJobSeekerEducation(id: number, educationId: number, formData: EducationItem) {
    return this.api.put(`${this.route}/${id}/${this.educations}/${educationId}`, formData);
  }

  deleteJobSeekerCertification(id: number, certificationId: number) {
    return this.api.delete(`${this.route}/${id}/${this.certifications}/${certificationId}`);
  }

  updateJobSeekerCertification(id: number, certificationId: number, formData: CertificationItem) {
    return this.api.put(`${this.route}/${id}/${this.certifications}/${certificationId}`, formData);
  }

  getJobSeekerCertifications(id: number) {
    return this.api.get(`${this.route}/${id}/${this.certifications}`);
  }

  getJobSeekerAplliedJobs() {
    return this.api.get(`${this.appliedJobs}`);
  }

  postJobSeekerNewCertification(id: number, data: CertificationItem) {
    return this.api.post(`${this.route}/${id}/${this.certifications}`, data);
  }

  partialUpdateJobSeekerProfile(id: number, data: any) {
    return this.api.patchById(`${this.route}`, id, data);
  }

  getJobSeekerExperience(id: number) {
    return this.api.get(`${this.route}/${id}/${this.jobExperience}`);
  }

  postJobSeekerNewExperience(id: number, data: JobItem) {
    return this.api.post(`${this.route}/${id}/${this.jobExperience}`, data);
  }

  updateJobSeekerExperience(id: number, jobId: number, experienceData: JobItem) {
    return this.api.put(`${this.route}/${id}/${this.jobExperience}/${jobId}`, experienceData);
  }

  deleteJobSeekerExperience(id: number, jobId: number) {
    return this.api.delete(`${this.route}/${id}/${this.jobExperience}/${jobId}`);
  }

  getJobSeekerCoverLetter(id: number) {
    return this.api.get(`${this.route}/${id}/${this.coverLetter}`);
  }

  postJobSeekerNewCoverLetter(id: number, data: CoverLetterItem) {
    return this.api.post(`${this.route}/${id}/${this.coverLetter}`, data);
  }

  updateJobSeekerCoverLetter(id: number, letterId: number, data: CoverLetterItem) {
    return this.api.put(`${this.route}/${id}/${this.coverLetter}/${letterId}`, data);
  }

  deleteJobSeekerCoverLetter(id: number, letterId: number) {
    return this.api.delete(`${this.route}/${id}/${this.coverLetter}/${letterId}`);
  }

  saveJobSeekerToFavorites(id: number, shouldRemove?: boolean) {
    const data = {id: id, add: true, remove: false};
    if (shouldRemove) {
      data.add = false;
      data.remove = true;
    }
    return this.api.post(
      `${this.alternativeRoute}/${id}/${this.favorites}`, data);
  }

  saveJobToFavorites(id: number, jobId: number) {
    return this.api.post(
      `${this.route}/${id}/${this.favoritesJobs}`,
      {job: jobId, add: true, remove: false}
    );
  }

  deleteJobFromFavorites(id: number, jobId: number) {
    return this.api.post(
      `${this.route}/${id}/${this.favoritesJobs}`,
      {job: jobId, add: false, remove: true}
    );
  }

  listFavoriteJobs(id: number, params?: object) {
    return this.api.get(`${this.route}/${id}/${this.favoritesJobs}`, params);
  }

  purchaseJobSeeker(id: number) {
    return this.api.put(`${this.route}/${id}/${this.purchase}`, {});
  }

  getCommentsForJS(jsId: number, params?: object) {
    return this.api.get(`${this.route}/${jsId}/${this.comment}`, params);
  }

  getLastViewsForJS(jsId: number, params?: object) {
    return this.api.get(`${this.route}/${jsId}/${this.viewers}`, params);
  }

  getAutoApplyStats() {
    return this.api.get(`${this.autoAppliesStats}`);
  }

  deleteJobSeekerProfileImage(id: number) {
    return this.api.put(`${this.route}/${id}/${this.routeImg}`, {photo: null});
  }
}
