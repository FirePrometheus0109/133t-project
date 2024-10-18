import { Component, OnDestroy } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { JobSeekerProfile } from '../../models';
import { JSPPageState } from '../../states/jsp-page.state';

import { CoreState } from '../../../core/states/core.state';

import { Enums } from '../../../shared/models/enums.model';

import { EducationType } from '../../../shared/models/education.model';


@Component({
  selector: 'app-job-seeker-print-view',
  templateUrl: './job-seeker-print-view.component.html',
  styleUrls: ['./job-seeker-print-view.component.scss']
})
export class JobSeekerPrintViewComponent implements OnDestroy {
  @Select(JSPPageState.pending) pending$: Observable<boolean>;
  @Select(JSPPageState.initialData) initialData$: Observable<JobSeekerProfile>;
  @Select(JSPPageState.educationAndCertificationData) educationAndCertificationData$: Observable<any>;
  @Select(JSPPageState.experience) experience$: Observable<any>;

  @Select(CoreState.enums) enums$: Observable<Enums>;

  public pending: boolean;
  public enums: Enums;
  public jobSeekerProfile: JobSeekerProfile;
  public educationAndCertificationData: [];
  public experienceData: [];
  public currentJobs = [];

  public educationType = EducationType.EDUCATION;
  public certeficationType = EducationType.CERTIFICATION;

  protected _onDestroy = new Subject<void>();

  constructor() {
    this.pending$
      .pipe(takeUntil(this._onDestroy))
      .subscribe((val) => {
        this.pending = val;
      });
    this.enums$
      .pipe(takeUntil(this._onDestroy))
      .subscribe((val) => {
        this.enums = val;
      });
    this.initialData$
      .pipe(takeUntil(this._onDestroy))
      .subscribe((val) => {
        this.jobSeekerProfile = val;
      });
    this.educationAndCertificationData$
      .pipe(takeUntil(this._onDestroy))
      .subscribe((val) => {
        this.educationAndCertificationData = val;
      });
    this.experience$
      .pipe(takeUntil(this._onDestroy))
      .subscribe((val) => {
        this.experienceData = val;
        this.currentJobs = this.filterCurrentJobs(val);
      });
  }

  ngOnDestroy(): void {
    this._onDestroy.next();
    this._onDestroy.complete();
  }

  public filterCurrentJobs(jobs: any[]) {
    return jobs.filter(job => job.is_current);
  }
}
