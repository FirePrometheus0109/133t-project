import { Component, EventEmitter, Input, Output } from '@angular/core';


@Component({
  selector: 'app-applied-job',
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>
          <h3 class="link" (click)="goToJobView.emit(jobItem.id)">{{jobItem.title}}</h3>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div>Company name: <span class="link" (click)="goToCompanyProfile.emit(jobItem.company.id)">{{jobItem.company.name}}</span></div>
        <div>Location: {{jobItem.location.city.name}} ({{jobItem.location.city.state.abbreviation}})</div>
        <div>Posted: {{jobItem.publish_date | date}}</div>
        <div *ngIf="isAppliedShow">Applied: {{jobItem.applied_at | date}}</div>
      </mat-card-content>
      <mat-card-header>
        <mat-card-title>
          <h3>Job Details</h3>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <app-job-metadata [jobItem]="jobItem"
                          [enums]="enums"
                          (viewAnsweredQuestionnaire)="viewAnsweredQuestionnaire.emit($event)">
        </app-job-metadata>
      </mat-card-content>
    </mat-card>
  `,
  styles: []
})
export class AppliedJobComponent {
  @Input() jobItem: any;
  @Input() enums: object;
  @Input() isAppliedShow: boolean;
  @Output() viewAnsweredQuestionnaire = new EventEmitter<any>();
  @Output() goToCompanyProfile = new EventEmitter<number>();
  @Output() goToJobView = new EventEmitter<number>();
}
