import { Component, EventEmitter, Inject, Input, OnInit, Output } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { Enums } from '../../shared/models/enums.model';


@Component({
  selector: 'app-view-job-preview',
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>
          <h4>{{jobItem.title}}</h4>
        </mat-card-title>
      </mat-card-header>
      <mat-dialog-content [ngClass]="{'not-modal': !isModal}">
        <mat-card-content>
          <div>Company name:
            <span class="link" (click)="navigateToCompany.emit(jobItem.company.id)">
              {{jobItem.company.name}}
            </span>
          </div>
          <div>Location: {{jobItem.location.city.name}} ({{jobItem.location.city.state.abbreviation}})</div>
          <div>{{jobItem.publish_date | postedDate}}</div>
          <div *ngIf="jobItem.owner">Created by: {{jobItem.owner?.name}}</div>
          <div>Created: {{jobItem.created_at | date}}</div>
          <div *ngIf="jobItem.applied_at">Applied At {{jobItem.applied_at | date}}</div>
          <div *ngIf="jobItem.closing_date">Active till {{jobItem.closing_date | date}}</div>
          <div *ngIf="jobItem.status">Status: {{enums.JobStatusEnum[jobItem.status]}}</div>
        </mat-card-content>
        <mat-card-header>
          <mat-card-title>
            <h4>Job details</h4>
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <app-job-metadata [jobItem]="jobItem" [enums]="enums">
          </app-job-metadata>
        </mat-card-content>
        <mat-card-header>
          <mat-card-title>
            <h4>Description</h4>
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <p>{{jobItem.description}}</p>
        </mat-card-content>
        <app-view-job-skill-component [jobItem]="jobItem" [isMatchMode]="matchMode">
        </app-view-job-skill-component>
        <button mat-button *ngIf="isJobVerified()"
                (click)="reapplyForJob.emit(jobItem.id)">
          <mat-icon matSuffix>present_to_all</mat-icon>
          Reapply
        </button>
      </mat-dialog-content>
      <mat-card-actions *ngIf="!matchMode && isEditable">
        <button mat-button (click)="editJob()">
          <mat-icon matSuffix>edit</mat-icon>
          Edit
        </button>
        <button mat-button (click)="goBack()">
          <mat-icon matSuffix>arrow_back_ios</mat-icon>
          Back
        </button>
      </mat-card-actions>
      <mat-card-actions *ngIf="matchMode && isEditable">
        <button mat-button (click)="dialogRef.close(true)">
          <mat-icon matSuffix>save</mat-icon>
          Save
        </button>
        <button mat-button (click)="dialogRef.close(false)">
          <mat-icon matSuffix>edit</mat-icon>
          Back to edit
        </button>
      </mat-card-actions>
      <mat-card-actions *ngIf="isViewDetailsAsJS" style="display: flex">
        <app-manual-apply-button [jobData]="jobItem" (manualApplyItem)="goBack()"></app-manual-apply-button>
        <button mat-button (click)="goBack()">
          <mat-icon matSuffix>close</mat-icon>
          Close
        </button>
        <app-job-favorite-toggle [jobId]="jobItem.id"></app-job-favorite-toggle>
        <app-share-job-control [id]="jobItem.id"
                               [uid]="jobItem.guid">
        </app-share-job-control>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [`
    div {
      margin-bottom: 10px;
    }

    .not-modal {
      display: initial;
    }

    .mat-card-content {
      text-align: left
    }
  `],
})
export class ViewJobPreviewComponent implements OnInit {
  @Input() jobItem: any;
  @Input() enums: Enums;
  @Input() isEditable = true;
  @Input() isViewDetailsAsJS: boolean;
  @Input() matchMode: boolean;
  @Output() cancel = new EventEmitter<any>();
  @Output() editJobItem = new EventEmitter<any>();
  @Output() applyForJob = new EventEmitter<any>();
  @Output() reapplyForJob = new EventEmitter<number>();
  @Output() navigateToCompany = new EventEmitter<number>();

  public isModal: boolean;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>) {
  }

  ngOnInit() {
    if (this.modalData && this.modalData.jobItem) {
      this.jobItem = this.modalData.jobItem;
      this.enums = this.modalData.enums;
      this.isEditable = this.modalData.isEditable;
      this.matchMode = true;
      this.isModal = true;
    }
  }

  public goBack() {
    this.cancel.emit();
  }

  public editJob() {
    this.editJobItem.emit(this.jobItem);
  }

  public isJobVerified() {
    return this.modalData && this.modalData.isJobVerified;
  }
}
