import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Enums } from '../models/enums.model';


@Component({
  selector: 'app-job-metadata',
  template: `
    <div>Position: {{enums.PositionTypes[jobItem.position_type]}}</div>
    <div>Salary: 
        <span *ngIf="!jobItem.salary_negotiable; else salaryNegotiable">
            <span *ngIf="!jobItem.salary_min && !jobItem.salary_max; else salaryKnown">
                N/A
            </span>
            <ng-template #salaryKnown>
                {{jobItem.salary_min | salaryView}} - {{jobItem.salary_max | salaryView}}
            </ng-template>
        </span>
        <ng-template #salaryNegotiable>
            Negotiable
        </ng-template>
    </div>
    <div>Education: {{enums.EducationTypes[jobItem.education]}}
      <span *ngIf="jobItem.education_strict">(strict)</span>
    </div>
    <div>Clearance: {{enums.ClearanceTypes[jobItem.clearance]}}</div>
    <div>Travel: {{enums.TravelOpportunities[jobItem.travel]}}</div>
    <div>Benefits: {{enums.Benefits[jobItem.benefits]}}</div>
    <div>Experience: {{enums.ExperienceTypes[jobItem.experience]}}</div>
    <div *ngIf="jobItem.questions && jobItem.questions.length > 0">
      <span *ngIf="!jobItem.applied_at" class="marker">
        <mat-icon matPrefix>not_listed_location</mat-icon>
        Questionnaire required
      </span>
      <span *ngIf="jobItem.applied_at" (click)="viewAnsweredQuestionnaire.emit(jobItem)" class="marker">
        <mat-icon matPrefix>remove_red_eye</mat-icon>
        Answered questionnaire
      </span>
    </div>
    <div *ngIf="jobItem.is_cover_letter_required">
      <span class="marker">
        <mat-icon matPrefix>contact_mail</mat-icon>
        Cover letter required
      </span>
    </div>
  `,
  styles: [`
    .marker {
      display: flex;
      align-items: center;
    }

    div {
      margin-bottom: 10px;
      margin-right: 15px;
    }
  `],
})
export class JobMetadataComponent {
  @Input() jobItem: any;
  @Input() enums: Enums;
  @Output() viewAnsweredQuestionnaire = new EventEmitter<any>();
}
