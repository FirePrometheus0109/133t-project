import {Injectable} from '@angular/core';
import {Store} from '@ngxs/store';
import {Observable} from 'rxjs';

@Injectable()
export class JobMatchingService {
  private static readonly base = `not match`;
  private static readonly newLine = `\n`;
  private static readonly coverLetterMessage = `Cover letter is required`;
  enums$: Observable<any>;

  constructor(private store: Store) {
    this.enums$ = this.store.select(state => state.core.enums);
  }

  private static educationMatchingMessage(jobData) {
    return `This position requires a ${jobData}`;
  }

  private static formSkillMatchMessage(matched, all) {
    return `You are missing ${all - matched} out of ${all} skills`;
  }

  private static formClearanceMatchMessage(name) {
    return `This position requires a ${name}`;
  }

  public getValidationMessage(jobData) {
    const result = [];
    if (!jobData.is_required_skills_match) {
      result.push(JobMatchingService.formSkillMatchMessage(jobData.matched_required_skills_count, jobData.all_required_skills_count));
    }
    if (!jobData.is_clearance_match) {
      this.enums$.subscribe((payload) => {
        result.push(JobMatchingService.formClearanceMatchMessage(payload.ClearanceTypes[jobData.clearance]));
      });
    }
    if (!jobData.is_education_match) {
      this.enums$.subscribe((payload) => {
        result.push(JobMatchingService.educationMatchingMessage(payload.EducationTypes[jobData.education]));
      });
    }
    if (jobData.is_cover_letter_required && !jobData.is_cover_letter_provided) {
      result.push(JobMatchingService.coverLetterMessage);
    }
    return result.join(JobMatchingService.newLine);
  }
}
