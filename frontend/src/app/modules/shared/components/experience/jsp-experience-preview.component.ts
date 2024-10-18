import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Enums } from '../../models/enums.model';
import { JobItem } from '../../models/experience.model';


@Component({
  selector: 'app-jsp-experience-preview',
  template: `
    <mat-card>
      <mat-card-title>
        <div class="job-title"><span>{{jobItem.job_title}}</span></div>
      </mat-card-title>
      <mat-card-content>
        <div>{{jobItem.company}}</div>
        <div>{{jobItem.description}}</div>
        <div>{{jobItem.date_from | date}}</div>
        <div>{{jobItem.date_to | date}}</div>
        <div>{{enums.Employment[jobItem.employment]}}</div>
      </mat-card-content>
      <mat-card-actions *ngIf="!onlyView">
        <button mat-button (click)="editJob()">
          <mat-icon matSuffix>edit</mat-icon>
        </button>
        <button mat-button (click)="deleteJob()">
          <mat-icon matSuffix>delete</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [`
    .job-title {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 20em;
    }
  `],
})
export class JspExperiencePreviewComponent {
  @Input() enums: Enums;
  @Input() jobItem: any;
  @Input() onlyView: boolean;
  @Output() deleteItem = new EventEmitter<number>();
  @Output() editItem = new EventEmitter<JobItem>();

  public deleteJob() {
    this.deleteItem.emit(this.jobItem.id);
  }

  public editJob() {
    this.editItem.emit(this.jobItem);
  }
}
