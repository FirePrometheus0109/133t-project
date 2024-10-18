import { Industry } from '../../shared/models/industry.model';
import { BaseJob } from '../../shared/models/job.model';
import { SkillItem } from '../../shared/models/skill.model';
import { Question } from '../../survey/models/question.model';


export class JobItem extends BaseJob {
  company: number;
  industry: Industry;
  description: string;
  status: string;
  education_strict: boolean;
  questions: Question[];
  views_count: number;
  applies_count: number;
  required_skills: Array<SkillItem>;
  optional_skills: Array<SkillItem>;
  is_deleted: boolean;
  deleted_at: Date;
  publish_date: Date;
}
