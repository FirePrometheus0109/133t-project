export class PositionEnum {
  FULL_TIME: string;
  PART_TIME: string;
  CONTRACT: string;
  TEMPORARY: string;
  INTERNSHIP: string;
  COMMISSION: string;
}


export class EducationEnum {
  HIGH_SCHOOL: string;
  CERTIFICATION: string;
  ASSOCIATES_DEGREE: string;
  BACHELORS_DEGREE: string;
  MASTERS_DEGREE: string;
  PHD: string;
}


export class JobSeekerEducationModelEnum {
  ASSOCIATES_DEGREE: string;
  BACHELORS_DEGREE: string;
  HIGH_SCHOOL: string;
  MASTERS_DEGREE: string;
  PHD: string;
}


export class ClearanceEnum {
  SECRET: string;
  TOP_SECRET: string;
  TOP_SECRET_SCI: string;
  MBI: string;
  PUBLIC_TRUST: string;
  CONFIDENTIAL: string;
  UNCLASSIFIED: string;
}


export class ExperienceEnum {
  NO_EXPERIENCE: string;
  LESS_THAN_1: string;
  FROM_1_TO_2: string;
  FROM_3_TO_5: string;
  FROM_5_TO_10: string;
  MORE_THAN_10: string;
}


export class BenefitsEnum {
  FULL_BENEFITS: string;
  PARTIAL_BENEFITS: string;
  HEALTH: string;
  VISION: string;
  HEALTH_AND_VISION: string;
  FOUR_OH_ONE_KEY: string;
}


export class TravelOpportunitiesEnum {
  FIFTY_OR_LESS: string;
  FIFTY_OR_MORE: string;
  MINIMAL: string;
  NO_TRAVEL: string;
  TWENTY_FIVE_OR_LESS: string;
}


export class JobStatusEnum {
  DRAFT: string;
  ACTIVE: string;
  CLOSED: string;
  DELAYED: string;
  DELETED: string;
}


export class AutoapplyStatusEnum {
  SAVED: string;
  IN_PROGRESS: string;
  FINISHED: string;
  STOPPED: string;
}


export class ApplyStatusEnum {
  APPLIED: string;
  NEED_REVIEW: string;
  VIEWED: string;
  NEW: string;
}


export class EmploymentEnum {
  FULL_TIME: string;
  PART_TIME: string;
}


export class CompanyUserStatusEnum {
  NEW: string;
  ACTIVE: string;
  DISABLED: string;
}


export class CandidateRatingEnum {
  NO_RATING: string;
  POOR: string;
  GOOD: string;
  VERY_GOOD: string;
  EXCELLENT: string;
}


export class CandidateStatusEnum {
  APPLIED: string;
  SCREENED: string;
  INTERVIEWED: string;
  OFFERED: string;
  HIRED: string;
  REJECTED: string;
}


export class AppliedDateFilterEnum {
  LAST_MONTH: string;
  LAST_WEEK: string;
  LAST_YEAR: string;
  THIS_MONTH: string;
  THIS_WEEK: string;
  THIS_YEAR: string;
  YESTERDAY: string;
}


export class JSTravelOpportunitiesEnum {
  NO_TRAVEL: string;
  WILLING_TO_TRAVEL: string;
}


export class LastUpdatedWithingDaysEnum {
  FIFTEEN_DAYS: string;
  FIVE_DAYS: string;
  SIXTY_DAYS: string;
  TEN_DAYS: string;
  THIRTY_DAYS: string;
}


export class Enums {
  PositionTypes: PositionEnum;
  EducationTypes: EducationEnum;
  ClearanceTypes: ClearanceEnum;
  ExperienceTypes: ExperienceEnum;
  Benefits: BenefitsEnum;
  TravelOpportunities: TravelOpportunitiesEnum;
  JobStatusEnum: JobStatusEnum;
  AutoapplyStatusEnum: AutoapplyStatusEnum;
  ApplyStatusEnum: ApplyStatusEnum;
  Employment: EmploymentEnum;
  CompanyUserStatus: CompanyUserStatusEnum;
  CandidateRating: CandidateRatingEnum;
  CandidateStatusEnum: CandidateStatusEnum;
  AppliedDateFilterEnum: AppliedDateFilterEnum;
  JSTravelOpportunities: JSTravelOpportunitiesEnum;
  LastUpdatedWithingDays: LastUpdatedWithingDaysEnum;
  JobSeekerEducationModelEnumDict: JobSeekerEducationModelEnum;
}
