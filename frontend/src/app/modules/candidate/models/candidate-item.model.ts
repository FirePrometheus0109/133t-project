import { Job } from '../../auto-apply/models/auto-apply.model';
import { JobSeekerProfile } from '../../job-seeker/models';
import { CoverLetterItem } from '../../shared/models/cover-letter.model';


export interface CandidateItem {
  id: number;
  job_seeker: JobSeekerProfile;
  job: Job;
  applied_date: Date;
  candidate_type: any;
  status: CandidateStatus;
  is_applied_after_assignment: boolean;
  is_disqualified_for_questionnaire: boolean;
  is_disqualified_for_skills: boolean;
  cover_letter: CoverLetterItem;
  rating?: CandidateRating;
}


export interface CandidateRating {
  owner: string;
  rating: string;
}

export interface CandidateStatus {
  id: string;
  name: string;
}
