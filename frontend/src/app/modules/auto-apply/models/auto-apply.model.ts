import { PublicCompanyItem } from '../../company/models/public-company.model';
import { CityModel, StateModel } from '../../shared/models/address.model';
import { BaseJob } from '../../shared/models/job.model';
import { SkillItem } from '../../shared/models/skill.model';


export interface AutoApply {
  id: number;
  title: string;
  status: string;
  query_params: any;
  number: number;
  jobs_count: number;
  new_jobs_count: number;
  days_to_completion: number;
  owner: number;
  stopped_jobs: Array<number>;
  deleted_jobs: Array<number>;
  autoapply_result: Array<any>;
  location?: CityModel | StateModel;
  education: string;
}


export interface Job extends BaseJob {
  company: PublicCompanyItem;
  matching_percent: string;
  is_clearance_match: boolean;
  is_required_skills_match: boolean;
  is_education_match: boolean;
  required_skills: Array<SkillItem>;
  optional_skills: Array<SkillItem>;
  description: string;
  applied_at: null;
  apply_job_status: string;
  all_required_skills_count: number;
  matched_required_skills_count: number;
}
