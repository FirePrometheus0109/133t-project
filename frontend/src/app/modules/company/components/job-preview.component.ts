import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatDialog } from '@angular/material';
import { Store } from '@ngxs/store';
import { Enums } from '../../shared/models/enums.model';
import { ViewJobViewerActions } from '../actions';
import { JobItem } from '../models/job.model';
import { ViewJobViewersComponent } from './view-job-viewers.component';


@Component({
  selector: 'app-job-preview',
  template: `
    <mat-card class="content-container" [ngClass]="{'prevent-card': isDashboard}">
      <div *ngIf="editable" class="checkbox-container">
        <mat-checkbox value="{{jobItem.id}}" [name]="checkBoxName"></mat-checkbox>
      </div>
      <div class="job-container">
        <mat-card>
          <mat-card-header>
            <mat-card-title>
              <span (click)="goToDetails.emit(jobItem.id)" class="link">{{jobItem.title}}</span>
            </mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <div>Location: {{jobItem.location.city.name}} ({{jobItem.location.city.state.abbreviation}})</div>
            <div *ngIf="jobItem.owner">Author: {{jobItem?.owner?.name}}</div>
            <div> {{jobItem.publish_date | postedDate}}</div>
            <div *ngIf="jobItem.closing_date">Active till {{jobItem.closing_date | date}}</div>
            <div (click)="openJobViewModal()"> {{jobItem.views_count}} Views</div>
            <app-candidate-page-button *ngIf="isCompanyUser && !isDashboard"
                                       [candidatesCount]="jobItem.candidates_count?.all"
                                       [jobId]="jobItem.id">
            </app-candidate-page-button>
          </mat-card-content>
          <mat-card-header *ngIf="!isDashboard">
            <mat-card-title>
              <h3>Details</h3>
            </mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <app-job-metadata [jobItem]="jobItem" [enums]="enums" [ngClass]="{'short-detail': isDashboard}">
            </app-job-metadata>
            <div *ngIf="isCompanyUser">Status: {{enums.JobStatusEnum[jobItem.status]}}</div>
            <div *ngIf="isCompanyUser && jobItem.is_deleted && !isDashboard">
              <div>Deleted: {{jobItem.deleted_at | date}}</div>
              <button mat-button (click)="restoreJob()">
                <mat-icon matSuffix>restore_from_trash</mat-icon>
              </button>
            </div>
          </mat-card-content>
          <mat-card-actions *ngIf="editable">
            <button mat-button (click)="editJob()">
              <mat-icon matSuffix>edit</mat-icon>
            </button>
            <button *ngIf="!jobItem.is_deleted" mat-button (click)="deleteJob()">
              <mat-icon matSuffix>delete</mat-icon>
            </button>
            <ng-template [ngxPermissionsOnly]="['view_jobcomment']">
              <button mat-button (click)="commentJob()">
                <mat-icon matSuffix>comment</mat-icon>
              </button>
            </ng-template>
            <app-share-job-control [id]="jobItem.id"
                                   [uid]="jobItem.guid">
            </app-share-job-control>
          </mat-card-actions>
        </mat-card>
      </div>
    </mat-card>
  `,
  styles: [`
    div {
      margin-bottom: 10px;
      margin-right: 20px;
    }

    mat-card-content {
      display: flex;
      flex-flow: row wrap;
      justify-content: space-between;
    }

    .content-container {
      display: flex;
      flex-direction: row;
    }

    .job-container {
      width: 100%;
      margin-right: 0;
    }

    .short-detail {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      justify-content: space-between;
    }

    .prevent-card {
      box-shadow: none;
      padding: 0;
    }
  `],
})
export class JobPreviewComponent {
  @Input() jobItem: JobItem;
  @Input() enums: Enums;
  @Input() statuses: object;
  @Input() editable = false;
  @Input() canViewDetails: boolean;
  @Input() checkBoxName: string;
  @Input() isCompanyUser: boolean;
  @Input() isDashboard: boolean;
  @Output() editJobItem = new EventEmitter<JobItem>();
  @Output() commentJobItem = new EventEmitter<number>();
  @Output() deleteJobItem = new EventEmitter<number>();
  @Output() goToDetails = new EventEmitter<number>();
  @Output() restoreJobItem = new EventEmitter<number>();

  constructor(public dialog: MatDialog,
              private store: Store) {
  }

  public editJob() {
    this.editJobItem.emit(this.jobItem);
  }

  public deleteJob() {
    this.deleteJobItem.emit(this.jobItem.id);
  }

  public commentJob() {
    this.commentJobItem.emit(this.jobItem.id);
  }

  public restoreJob() {
    this.restoreJobItem.emit(this.jobItem.id);
  }

  openJobViewModal() {
    this.store.dispatch(new ViewJobViewerActions.LoadJobViewers(this.jobItem.id));

    const dialogRef = this.dialog.open(ViewJobViewersComponent, {
      width: '80%',
      data: {
        jobId: this.jobItem.id
      }
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.close();
    });
  }
}
