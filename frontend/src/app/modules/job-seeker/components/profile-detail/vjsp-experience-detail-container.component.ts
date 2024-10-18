import { Component, Input } from '@angular/core';
import { Enums } from '../../../shared/models/enums.model';
import { JobItem } from '../../../shared/models/experience.model';


@Component({
  selector: 'app-vjsp-experience-detail',
  template: `
    <div *ngIf="!shouldGetShortCurWorkPresentation()">
      <div class="experience-detail-container" *ngFor="let exp of experience">
        <div class="experience-detail">
          <mat-card-subtitle class="experience-title">Company</mat-card-subtitle>
          <mat-card-content class="experience-value">{{ exp.company }}</mat-card-content>
        </div>
        <div class="experience-detail">
          <mat-card-subtitle class="experience-title">Job title</mat-card-subtitle>
          <mat-card-content class="experience-value">{{ exp.job_title }}</mat-card-content>
        </div>
        <div class="experience-detail">
          <mat-card-subtitle class="experience-title">Years of work</mat-card-subtitle>
          <mat-card-content class="experience-value">from {{ exp.date_from | date }} to {{ (exp.date_to | date) ||
          'present' }}
          </mat-card-content>
        </div>
        <div class="experience-detail">
          <mat-card-subtitle class="experience-title">{{enums.Employment[exp.employment]}}</mat-card-subtitle>
        </div>
        <div class="experience-detail">
          <mat-card-subtitle class="experience-title">Description</mat-card-subtitle>
          <mat-card-content class="experience-value">{{ exp.description }}</mat-card-content>
        </div>
      </div>
    </div>
    <div *ngIf="shouldGetShortCurWorkPresentation()">
      <mat-card-subtitle>
        <div
          *ngFor="let exp of getCurExperience()"
          class="mat-caption"
        >
        {{ exp.job_title }} at {{ exp.company }}
        </div>
      </mat-card-subtitle>
      <br/>
    </div>
  `,
  styles: [`
    .experience-detail-container {
      border-bottom: .15px solid rgba(0, 0, 0, 0.87);
      margin-bottom: 45px;
    }

    .experience-detail {
      display: flex;
      flex-direction: row;
    }

    .experience-title {
      text-align: right;
      width: 20%;
    }

    .experience-value {
      padding-left: 25px;
      text-align: left;
      width: 80%;
    }

    .mat-chip-list {
      display: flex;
      justify-content: center;
    }
  `],
})
export class VjspExperienceDetailComponent {
  @Input() experience: Array<JobItem>;
  @Input() enums: Enums;
  @Input() currentWork = false;
  @Input() short = false;

  shouldGetShortCurWorkPresentation() {
    return this.currentWork && this.short;
  }

  getCurExperience() {
    return this.experience.filter(exp => exp.is_current);
  }
}
