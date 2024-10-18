import { CoverLetterItem } from '../../shared/models/cover-letter.model';
import { CertificationItem, EducationItem } from '../../shared/models/education.model';
import { JobItem } from '../../shared/models/experience.model';
import { Photo } from '../../shared/models/photo.model';


export enum JobSeekerProfilePageActionTypes {
  LoadInitialData = '[Job Seeker Profile Page] LoadInitialData',
  PartialUpdate = '[Job Seeker Profile Page] PartialUpdate',
  LoadEducationData = '[Job Seeker Profile Page] LoadEducationData',
  LoadCertificationData = '[Job Seeker Profile Page] LoadCertificationData',
  CreateNewEducation = '[Job Seeker Profile Page] CreateNewEducation',
  CreateNewCertification = '[Job Seeker Profile Page] CreateNewCertification',
  DeleteEducation = '[Job Seeker Profile Page] DeleteEducation',
  DeleteCertification = '[Job Seeker Profile Page] DeleteCertification',
  UpdateEducationMode = '[Job Seeker Profile Page] UpdateEducationMode',
  UpdateEducationType = '[Job Seeker Profile Page] UpdateEducationType',
  UpdateEducation = '[Job Seeker Profile Page] UpdateEducation',
  UpdateCertification = '[Job Seeker Profile Page] UpdateCertification',
  LoadExperienceData = '[Job Seeker Profile Page] LoadExperienceData',
  UpdateExperienceMode = '[Job Seeker Profile Page] UpdateExperienceMode',
  CreateNewExperience = '[Job Seeker Profile Page] CreateNewExperience',
  UpdateExperience = '[Job Seeker Profile Page] UpdateExperience',
  DeleteExperience = '[Job Seeker Profile Page] DeleteExperience',
  LoadCoverLetterData = '[Job Seeker Profile Page] LoadCoverLetterData',
  CreateNewCoverLetter = '[Job Seeker Profile Page] CreateNewCoverLetter',
  UpdateCoverLetter = '[Job Seeker Profile Page] UpdateCoverLetter',
  DeleteCoverLetter = '[Job Seeker Profile Page] DeleteCoverLetter',
  UpdateCoverLetterMode = '[Job Seeker Profile Page] UpdateCoverLetterMode',
  UpdatePhoto = '[Job Seeker Profile Page] UpdatePhoto',
  UpdatePublishHideProfileTooltipText = '[Job Seeker Profile Page] UpdatePublishHideProfileTooltipText',
  UpdateCurrentJspObject = '[Job Seeker Profile Page] UpdateCurrentJspObject',
  LoadCurrentJobSeeker = '[Job Seeker Profile Page] LoadCurrentJobSeeker',
  LoadJobSeekerAsCandidate = '[Job Seeker Profile Page] LoadJobSeekerAsCandidate',
  LoadAnswers = '[Job Seeker Profile Page] LoadAnswers',
  SetJSPSectionMode = '[Job Seeker Profile Page] SetJSPSectionMode',
  DeleteProfileImage = '[Job Seeker Profile Page] DeleteProfileImage',
}


export class LoadInitialData {
  static readonly type = JobSeekerProfilePageActionTypes.LoadInitialData;

  constructor(public id: number) {
  }
}


export class LoadCurrentJobSeeker {
  static readonly type = JobSeekerProfilePageActionTypes.LoadCurrentJobSeeker;

  constructor(public id: number) {
  }
}


export class LoadJobSeekerAsCandidate {
  static readonly type = JobSeekerProfilePageActionTypes.LoadJobSeekerAsCandidate;

  constructor(public id: number) {
  }
}


export class LoadEducationData {
  static readonly type = JobSeekerProfilePageActionTypes.LoadEducationData;

  constructor(public jspId: number) {
  }
}


export class CreateNewEducation {
  static readonly type = JobSeekerProfilePageActionTypes.CreateNewEducation;

  constructor(public jspId: number, public data: EducationItem) {
  }
}


export class DeleteEducation {
  static readonly type = JobSeekerProfilePageActionTypes.DeleteEducation;

  constructor(public jspId: number, public educationId: number) {
  }
}


export class UpdateEducation {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateEducation;

  constructor(public jspId: number, public educationId: number, public formData: EducationItem) {
  }
}


export class LoadCertificationData {
  static readonly type = JobSeekerProfilePageActionTypes.LoadCertificationData;

  constructor(public jspId: number) {
  }
}


export class CreateNewCertification {
  static readonly type = JobSeekerProfilePageActionTypes.CreateNewCertification;

  constructor(public jspId: number, public data: CertificationItem) {
  }
}


export class DeleteCertification {
  static readonly type = JobSeekerProfilePageActionTypes.DeleteCertification;

  constructor(public jspId: number, public certificationId: number) {
  }
}


export class UpdateCertification {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateCertification;

  constructor(public jspId: number, public certificationId: number, public formData: CertificationItem) {
  }
}


export class PartialUpdate {
  static readonly type = JobSeekerProfilePageActionTypes.PartialUpdate;

  constructor(public part: string, public id: number, public data: any) {
  }
}


export class UpdateEducationMode {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateEducationMode;

  constructor(public value: string) {
  }
}


export class UpdateEducationType {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateEducationType;

  constructor(public value: string) {
  }
}


export class LoadExperienceData {
  static readonly type = JobSeekerProfilePageActionTypes.LoadExperienceData;

  constructor(public jspId: number) {
  }
}


export class CreateNewExperience {
  static readonly type = JobSeekerProfilePageActionTypes.CreateNewExperience;

  constructor(public jspId: number, public experienceData: JobItem) {
  }
}


export class UpdateExperience {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateExperience;

  constructor(public jspId: number, public jobId: number, public experienceData: JobItem) {
  }
}


export class DeleteExperience {
  static readonly type = JobSeekerProfilePageActionTypes.DeleteExperience;

  constructor(public jspId: number, public jobId: number) {
  }
}


export class UpdateExperienceMode {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateExperienceMode;

  constructor(public value: string) {
  }
}


export class LoadCoverLetterData {
  static readonly type = JobSeekerProfilePageActionTypes.LoadCoverLetterData;

  constructor(public jspId: number) {
  }
}


export class CreateNewCoverLetter {
  static readonly type = JobSeekerProfilePageActionTypes.CreateNewCoverLetter;

  constructor(public jspId: number, public coverLetterData: CoverLetterItem) {
  }
}


export class UpdateCoverLetter {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateCoverLetter;

  constructor(public jspId: number, public coverLetterId: number, public coverLetterData: CoverLetterItem) {
  }
}


export class DeleteCoverLetter {
  static readonly type = JobSeekerProfilePageActionTypes.DeleteCoverLetter;

  constructor(public jspId: number, public coverLetterId: number) {
  }
}


export class UpdateCoverLetterMode {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateCoverLetterMode;

  constructor(public value: string) {
  }
}


export class UpdatePhoto {
  static readonly type = JobSeekerProfilePageActionTypes.UpdatePhoto;

  constructor(public jspId: number, public data: Photo) {
  }
}


export class UpdatePublishHideProfileTooltipText {
  static readonly type = JobSeekerProfilePageActionTypes.UpdatePublishHideProfileTooltipText;

  constructor() {
  }
}


export class UpdateCurrentJspObject {
  static readonly type = JobSeekerProfilePageActionTypes.UpdateCurrentJspObject;

  constructor() {
  }
}


export class LoadAnswers {
  static readonly type = JobSeekerProfilePageActionTypes.LoadAnswers;

  constructor(public jobId: number, public jobSeekerId: number) {
  }
}


export class SetJSPSectionMode {
  static readonly type = JobSeekerProfilePageActionTypes.SetJSPSectionMode;

  constructor(public sectionEditName: string, public value: boolean) {
  }
}

export class DeleteProfileImage {
  static readonly type = JobSeekerProfilePageActionTypes.DeleteProfileImage;

  constructor(public jspId: number) {
  }
}


export type JobSeekerProfilePageActionsUnion =
  | DeleteProfileImage
  | SetJSPSectionMode
  | LoadAnswers
  | LoadJobSeekerAsCandidate
  | LoadCurrentJobSeeker
  | LoadInitialData
  | LoadEducationData
  | CreateNewEducation
  | DeleteEducation
  | UpdateEducation
  | LoadCertificationData
  | CreateNewCertification
  | DeleteCertification
  | UpdateCertification
  | UpdateEducationMode
  | UpdateEducationType
  | LoadExperienceData
  | CreateNewExperience
  | UpdateExperience
  | DeleteExperience
  | UpdateExperienceMode
  | LoadCoverLetterData
  | CreateNewCoverLetter
  | UpdateCoverLetter
  | DeleteCoverLetter
  | UpdateCoverLetterMode
  | PartialUpdate
  | UpdatePhoto
  | UpdatePublishHideProfileTooltipText
  | UpdateCurrentJspObject;
