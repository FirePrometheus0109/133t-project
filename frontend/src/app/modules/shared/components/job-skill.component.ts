import { Component, Input, OnInit } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';


@Component({
  selector: 'app-view-job-skill-component',
  template: `
    <mat-card-content>
      <div *ngIf="isMatchMode && isMustSkillsMissed && (isJobSeeker$ | async)" align="start">
        <span class="mat-error">You are missing {{missedMustSkillsCount}} of {{jobItem.required_skills.length}} must have skills.</span>
      </div>
      <app-skills-view-component [skillsToDisplay]="jobItem.required_skills"
                                 [isMatchMode]="isMatchMode && (isJobSeeker$ | async)"
                                 [title]="'Must have'"></app-skills-view-component>
      <app-skills-view-component [skillsToDisplay]="jobItem.optional_skills"
                                 [isMatchMode]="isMatchMode && (isJobSeeker$ | async)"
                                 [title]="'Nice to have'"></app-skills-view-component>
    </mat-card-content>
  `,
  styles: []
})
export class ViewJobSkillComponent implements OnInit {
  @Select(AuthState.isJobSeeker) isJobSeeker$: Observable<boolean>;

  @Input() jobItem: any;
  @Input() isMatchMode: any;

  public isMustSkillsMissed: boolean;
  public missedMustSkillsCount = 0;

  ngOnInit() {
    this.checkMustSkills();
  }

  public checkMustSkills() {
    if (this.isMatchMode) {
      this.jobItem.required_skills.forEach(skillItem => {
        if (!skillItem.match) {
          this.missedMustSkillsCount++;
        }
      });
      if (this.missedMustSkillsCount) {
        this.isMustSkillsMissed = true;
      }
    }
  }
}
