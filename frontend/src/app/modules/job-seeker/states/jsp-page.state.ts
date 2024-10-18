import { HttpErrorResponse } from '@angular/common/http';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CandidateItem } from '../../candidate/models/candidate-item.model';
import { CandidateService } from '../../candidate/services/candidate.service';
import { CommentsActions, LogsActions } from '../../common-components/actions';
import { JobService } from '../../company/services/job.service';
import { NavigationService } from '../../core/services/navigation.service';
import { HttpStatuses } from '../../shared/constants/http-statuses';
import { CoverLetterItem, CoverLetterMode } from '../../shared/models/cover-letter.model';
import { CertificationItem, EducationItem, EducationMode, EducationType } from '../../shared/models/education.model';
import { ExperienceMode, JobItem } from '../../shared/models/experience.model';
import { DEFAULT_PAGINATED_OPTIONS, PaginatedData } from '../../shared/models/paginated-data.model';
import { JobSeekerProfilePageActions, JobSeekerProfilePublicPageActions } from '../actions';
import { JobSeekerProfile, JSNameAndId } from '../models';
import { JobSeekerProfileForCompany } from '../models/job-seeker-profile.model';
import { JobSeekerService } from '../services';


class JSPPageStateModel {
  status: string;
  errors: object;
  initialData: object;
  education: Array<EducationItem>;
  certification: Array<CertificationItem>;
  educationMode: string;
  educationType: string;
  experience: Array<JobItem>;
  experienceMode: string;
  coverLetter: Array<CoverLetterItem>;
  coverLetterMode: string;
  defaultCoverLetter: CoverLetterItem;
  photo: {
    original: string;
    small: string;
    name: string;
  };
  publishHideProfileTooltipText: string;
  currentJspObject: JobSeekerProfile;
  jspDataForCompany: any;
  currentCandidate: CandidateItem;
  answeredQuestionnaire: any[];
  mainInfoSectionEditMode: boolean;
  addressSectionEditMode: boolean;
  aboutSectionEditMode: boolean;
  profileDetailsSectionEditMode: boolean;
  skillsSectionEditMode: boolean;
}


export const DEFAULT_JSPPAGE_STATE = {
  status: '',
  errors: null,
  initialData: null,
  education: [],
  certification: [],
  educationMode: EducationMode.VIEW,
  educationType: '',
  experience: [],
  experienceMode: ExperienceMode.VIEW,
  coverLetter: [],
  coverLetterMode: CoverLetterMode.VIEW,
  defaultCoverLetter: null,
  photo: {
    original: '',
    small: '',
    name: '',
  },
  publishHideProfileTooltipText: '',
  currentJspObject: <JobSeekerProfile>{},
  jspDataForCompany: null,
  currentCandidate: null,
  answeredQuestionnaire: [],
  mainInfoSectionEditMode: false,
  addressSectionEditMode: false,
  aboutSectionEditMode: false,
  profileDetailsSectionEditMode: false,
  skillsSectionEditMode: false,
};


@State<JSPPageStateModel>({
  name: 'JSPPage',
  defaults: DEFAULT_JSPPAGE_STATE,
})
export class JSPPageState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static initialData(state: any) {
    return state.initialData;
  }

  @Selector()
  static NameAndId(state: any): JSNameAndId {
    const result: JSNameAndId = {
      id: 0,
      first_name: '',
      last_name: '',
    };
    if (state.initialData && state.initialData.id) {
      result.id = state.initialData.id;
    }
    if (state.initialData && state.initialData.user) {
      if (state.initialData.user.first_name) {
        result.first_name = state.initialData.user.first_name;
      }
      if (state.initialData.user.last_name) {
        result.last_name = state.initialData.user.last_name;
      }
    }
    return result;
  }

  @Selector()
  static Photo(state: any) {
    return state.photo;
  }

  @Selector()
  static educationData(state: any) {
    return state.education;
  }

  @Selector()
  static certificationData(state: any) {
    return state.certification;
  }

  @Selector()
  static educationMode(state: any) {
    return state.educationMode;
  }

  @Selector()
  static educationType(state: any) {
    return state.educationType;
  }

  @Selector()
  static educationAndCertificationData(state: any) {
    const education = state.education;
    const certification = state.certification;
    education.forEach(item => item.type = EducationType.EDUCATION);
    certification.forEach(item => item.type = EducationType.CERTIFICATION);
    const result = certification.concat(education);
    return result;
  }

  @Selector()
  static experience(state: any) {
    return state.experience;
  }

  @Selector()
  static experienceCount(state: any): number {
    return state.experience.length;
  }

  @Selector()
  static experienceMode(state: any) {
    return state.experienceMode;
  }

  @Selector()
  static coverLetter(state: any) {
    return state.coverLetter;
  }

  @Selector()
  static coverLetterMode(state: any) {
    return state.coverLetterMode;
  }

  @Selector()
  static currentJspObject(state: JSPPageStateModel): JobSeekerProfile {
    return state.currentJspObject;
  }

  @Selector()
  static publishHideProfileTooltipText(state: JSPPageStateModel): string {
    return state.publishHideProfileTooltipText;
  }

  @Selector()
  static defaultCoverLetter(state: JSPPageStateModel): CoverLetterItem {
    return state.defaultCoverLetter;
  }

  @Selector()
  static currentCandidate(state: JSPPageStateModel): CandidateItem {
    return state.currentCandidate;
  }

  @Selector()
  static answeredQuestionnaire(state: JSPPageStateModel): any {
    return state.answeredQuestionnaire;
  }

  @Selector()
  static mainInfoSectionEditMode(state: JSPPageStateModel): boolean {
    return state.mainInfoSectionEditMode;
  }

  @Selector()
  static addressSectionEditMode(state: JSPPageStateModel): boolean {
    return state.addressSectionEditMode;
  }

  @Selector()
  static aboutSectionEditMode(state: JSPPageStateModel): boolean {
    return state.aboutSectionEditMode;
  }

  @Selector()
  static profileDetailsSectionEditMode(state: JSPPageStateModel): boolean {
    return state.profileDetailsSectionEditMode;
  }

  @Selector()
  static skillsSectionEditMode(state: JSPPageStateModel): boolean {
    return state.skillsSectionEditMode;
  }

  constructor(private jssService: JobSeekerService,
              private candidateService: CandidateService,
              private jobService: JobService,
              private navigationService: NavigationService) {
  }

  @Action(JobSeekerProfilePageActions.SetJSPSectionMode)
  setJSPSectionMode(ctx, {sectionEditName, value}: JobSeekerProfilePageActions.SetJSPSectionMode) {
    const state = ctx.getState();
    return of(ctx.setState({
      ...state,
      [sectionEditName]: value,
    }));
  }

  @Action(JobSeekerProfilePageActions.PartialUpdate)
  partialUpdate(ctx, {part, id, data}: JobSeekerProfilePageActions.PartialUpdate) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.partialUpdateJobSeekerProfile(id, data).pipe(
      tap((result) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          initialData: {
            ...state.initialData,
            ...new JobSeekerProfile().deserialize(result),
          },
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.UpdateCurrentJspObject());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.UpdatePhoto)
  updatePhoto(ctx, {jspId, data}: JobSeekerProfilePageActions.UpdatePhoto) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      photo: data,
    });
  }

  @Action(JobSeekerProfilePageActions.LoadInitialData)
  loadInitialData(ctx, {id}: JobSeekerProfilePageActions.LoadInitialData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.getJobSeekerProfile(id).pipe(
      tap((result) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          initialData: {
            ...result,
            ...new JobSeekerProfile().deserialize(result)
          },
          photo: result['photo'],
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.UpdateCurrentJspObject());
      }),
      catchError((error: HttpErrorResponse) => {
        state = ctx.getState();
        if (error.status === HttpStatuses['403_FORBIDDEN']) {
          return of(this.navigationService.goToHomePage());
        } else {
          return of(ctx.setState({
            ...state,
            status: 'error',
            errors: error.error,
            initialData: null,
          }));
        }
      })
    );
  }

  @Action(JobSeekerProfilePageActions.LoadCurrentJobSeeker)
  loadCurrentJobSeeker(ctx, {id}: JobSeekerProfilePageActions.LoadCurrentJobSeeker) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.getJobSeekerProfile(id).pipe(
      tap((result: JobSeekerProfileForCompany) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          jspDataForCompany: result,
          initialData: result,
          photo: result.photo,
          education: result.educations,
          certification: result.certifications,
          experience: result.job_experience,
          currentCandidate: null
        });
      }),
      catchError((error: HttpErrorResponse) => {
        state = ctx.getState();
        if (error.status === HttpStatuses['403_FORBIDDEN']) {
          return of(this.navigationService.goToHomePage());
        } else {
          return of(ctx.setState({
            ...state,
            status: 'error',
            errors: error.error,
            initialData: null,
          }));
        }
      })
    );
  }

  @Action(JobSeekerProfilePageActions.LoadJobSeekerAsCandidate)
  loadJobSeekerAsCandidate(ctx, {id}: JobSeekerProfilePageActions.LoadJobSeekerAsCandidate) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.candidateService.getCandidate(id).pipe(
      tap((result: any) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          currentCandidate: result,
          jspDataForCompany: result.job_seeker,
          initialData: result.job_seeker,
          photo: result.job_seeker.photo,
          education: result.job_seeker.educations,
          certification: result.job_seeker.certifications,
          experience: result.job_seeker.job_experience,
        });
        state = ctx.getState();
        ctx.dispatch(new JobSeekerProfilePageActions.LoadAnswers(state.currentCandidate.job.id, state.currentCandidate.job_seeker.id));
        ctx.dispatch(new LogsActions.LoadLogsData(state.initialData.id, DEFAULT_PAGINATED_OPTIONS));
        return ctx.dispatch(new CommentsActions.LoadCommentsData(state.initialData.id, DEFAULT_PAGINATED_OPTIONS));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          currentCandidate: null,
          initialDate: null,
          photo: null,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.LoadAnswers)
  loadAnswers(ctx, {jobId, jobSeekerId}: JobSeekerProfilePageActions.LoadAnswers) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getCandidateAnswer(jobId, jobSeekerId).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          answeredQuestionnaire: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          answeredQuestionnaire: [],
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.LoadEducationData)
  loadEducationData(ctx, {jspId}: JobSeekerProfilePageActions.LoadEducationData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.getJobSeekerEducations(jspId).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          education: result['results'],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          education: [],
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.LoadCertificationData)
  loadCertificationData(ctx, {jspId}: JobSeekerProfilePageActions.LoadCertificationData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.getJobSeekerCertifications(jspId).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          certification: result['results'],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          certification: [],
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.CreateNewEducation)
  createNewEducation(ctx, {jspId, data}: JobSeekerProfilePageActions.CreateNewEducation) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.postJobSeekerNewEducation(jspId, data).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadEducationData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.DeleteEducation)
  deleteEducation(ctx, {jspId, educationId}: JobSeekerProfilePageActions.DeleteEducation) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.deleteJobSeekerEducation(jspId, educationId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadEducationData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.UpdateEducation)
  updateEducation(ctx, {jspId, educationId, formData}: JobSeekerProfilePageActions.UpdateEducation) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.updateJobSeekerEducation(jspId, educationId, formData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadEducationData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.CreateNewCertification)
  createNewCertification(ctx, {jspId, data}: JobSeekerProfilePageActions.CreateNewCertification) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.postJobSeekerNewCertification(jspId, data).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadCertificationData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.DeleteCertification)
  deleteCertification(ctx, {jspId, certificationId}: JobSeekerProfilePageActions.DeleteCertification) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.deleteJobSeekerCertification(jspId, certificationId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadCertificationData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.UpdateCertification)
  updateCertification(ctx, {jspId, certificationId, formData}: JobSeekerProfilePageActions.UpdateCertification) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.updateJobSeekerCertification(jspId, certificationId, formData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadCertificationData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.UpdateEducationMode)
  updateEducationMode(ctx, {value}: JobSeekerProfilePageActions.UpdateEducationMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      educationMode: value,
    });
  }

  @Action(JobSeekerProfilePageActions.UpdateEducationType)
  updateEducationType(ctx, {value}: JobSeekerProfilePageActions.UpdateEducationType) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      educationType: value,
    });
  }

  @Action(JobSeekerProfilePageActions.UpdateExperienceMode)
  updateExperienceMode(ctx, {value}: JobSeekerProfilePageActions.UpdateExperienceMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      experienceMode: value,
    });
  }

  @Action(JobSeekerProfilePageActions.LoadExperienceData)
  loadExperienceData(ctx, {jspId}: JobSeekerProfilePageActions.LoadExperienceData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.getJobSeekerExperience(jspId).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          experience: result['results'],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          experience: [],
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.CreateNewExperience)
  createNewExperience(ctx, {jspId, experienceData}: JobSeekerProfilePageActions.CreateNewExperience) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.postJobSeekerNewExperience(jspId, experienceData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadExperienceData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.UpdateExperience)
  updateExperience(ctx, {jspId, jobId, experienceData}: JobSeekerProfilePageActions.UpdateExperience) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.updateJobSeekerExperience(jspId, jobId, experienceData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadExperienceData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.DeleteExperience)
  DeleteExperience(ctx, {jspId, jobId}: JobSeekerProfilePageActions.DeleteExperience) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.deleteJobSeekerExperience(jspId, jobId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadExperienceData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  // CoverLetter
  @Action(JobSeekerProfilePageActions.UpdateCoverLetterMode)
  updateCoverLetterMode(ctx, {value}: JobSeekerProfilePageActions.UpdateCoverLetterMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      coverLetterMode: value,
    });
  }

  @Action(JobSeekerProfilePageActions.LoadCoverLetterData)
  loadCoverLetterData(ctx, {jspId}: JobSeekerProfilePageActions.LoadCoverLetterData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.getJobSeekerCoverLetter(jspId).pipe(
      tap((result: PaginatedData) => {
        const defaultLetter = result.results.find((letter: CoverLetterItem) => letter.is_default === true);
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          defaultCoverLetter: defaultLetter,
          coverLetter: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          coverLetter: [],
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.CreateNewCoverLetter)
  createNewCoverLetter(ctx, {jspId, coverLetterData}: JobSeekerProfilePageActions.CreateNewCoverLetter) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.postJobSeekerNewCoverLetter(jspId, coverLetterData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new JobSeekerProfilePageActions.UpdateCoverLetterMode(CoverLetterMode.VIEW));
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadCoverLetterData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.UpdateCoverLetter)
  updateCoverLetter(ctx, {jspId, coverLetterId, coverLetterData}: JobSeekerProfilePageActions.UpdateCoverLetter) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.updateJobSeekerCoverLetter(jspId, coverLetterId, coverLetterData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new JobSeekerProfilePageActions.UpdateCoverLetterMode(CoverLetterMode.VIEW));
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadCoverLetterData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.DeleteCoverLetter)
  DeleteCoverLetter(ctx, {jspId, coverLetterId}: JobSeekerProfilePageActions.DeleteCoverLetter) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.deleteJobSeekerCoverLetter(jspId, coverLetterId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new JobSeekerProfilePageActions.LoadCoverLetterData(jspId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(JobSeekerProfilePageActions.UpdatePublishHideProfileTooltipText)
  updatePublishHideProfileTooltipText(ctx) {
    const state = ctx.getState();
    const publishProfileText = 'Here\'s what you need to publish profile:\n\n';
    const hideProfileText = 'Nobody will see your profile.\nYou won\'t be able to apply a job.';
    const text: string = (state.currentJspObject.is_public)
      ? hideProfileText
      : `${publishProfileText}${state.currentJspObject.getPublishHideProfileValidationText()}`;
    return ctx.setState({
      ...state,
      publishHideProfileTooltipText: text,
    });
  }

  @Action(JobSeekerProfilePageActions.UpdateCurrentJspObject)
  updateCurrentJspObject(ctx) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      currentJspObject: new JobSeekerProfile().deserialize(state.initialData),
    });
    return ctx.dispatch(new JobSeekerProfilePageActions.UpdatePublishHideProfileTooltipText());
  }

  @Action(JobSeekerProfilePublicPageActions.LoadPublicProfile)
  loadPublicProfile({patchState, dispatch}: StateContext<JSPPageStateModel>, {jsUid}: JobSeekerProfilePublicPageActions.LoadPublicProfile) {
    patchState({
      status: 'pending'
    });
    return this.jssService.getJobSeekerPublicProfile(jsUid).pipe(
      tap((result) => {
        patchState({
          status: 'done',
          errors: null,
          initialData: result,
          photo: result['photo'],
          education: result['educations'],
          certification: result['certifications'],
          experience: result['job_experience'],
        });
        return dispatch(new JobSeekerProfilePageActions.UpdateCurrentJspObject());
      }),
      catchError(error => {
        return of(patchState({
          status: 'error',
          errors: error.error
        }));
      })
    );
  }

  @Action(JobSeekerProfilePageActions.DeleteProfileImage)
  deleteProfileImage(ctx, {jspId}: JobSeekerProfilePageActions.DeleteProfileImage) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jssService.deleteJobSeekerProfileImage(jspId).pipe(
      tap(() => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }
}
