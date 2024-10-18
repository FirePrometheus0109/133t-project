import { Component, Inject, Input, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material';
import * as moment from 'moment';
import { NavigationService } from '../../core/services/navigation.service';
import { Enums } from '../../shared/models/enums.model';


@Component({
  selector: 'app-search-job-list-job-view',
  template: `
    <mat-card>
      <div class="job-container">
        <div fxFlexFill fxLayoutAlign="end">
          <app-share-job-control [uid]="jobItem.guid"
                                 [id]="jobItem.id">
          </app-share-job-control>
        </div>
        <div class="job-header">
          <mat-card-title class="job-title">
            <span class="link" (click)="goToJobView(jobItem.id)">{{jobItem.title}}</span>
            <app-job-favorite-toggle [jobId]="jobItem.id"></app-job-favorite-toggle>
          </mat-card-title>
          <mat-icon *ngIf="jobItem?.applied_at" matTooltip="{{appliedDateTooltip}}">check_box</mat-icon>
          <div>{{jobItem.matching_percent | number:'1.0-0'}}% match</div>
        </div>
        <mat-card-content class="job-company-container">
          <div class="company-title">
            <div class="link" (click)="goToCompanyView(jobItem.company.id)">{{jobItem.company?.name}}</div>
            <div>{{jobItem.location.city.name}} ({{jobItem.location.city.state.abbreviation}})</div>
          </div>
          <div>Posted: {{jobItem.publish_date | date}}</div>
          <div *ngIf="jobItem.closing_date">Active till {{jobItem.closing_date | date}}</div>
        </mat-card-content>
        <mat-card-header>
          <mat-card-title>
            <span>Details</span>
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div>
            <app-job-metadata class="job-detail-container"
                              [jobItem]="jobItem"
                              [enums]="enums">
            </app-job-metadata>
          </div>
        </mat-card-content>
      </div>
    </mat-card>
  `,
  styles: [`
    .job-container {
      border-top: 3px solid rgba(0, 0, 0, 0.42);
      padding: 20px 50px 20px 30px;
      width: 75%;
    }

    .job-company-container {
      display: flex;
      flex-direction: row;
    }

    .job-detail-container {
      display: flex;
      flex-flow: row wrap;
      justify-content: space-between;
    }

    .job-detail-container div {
      margin-right: 15px;
    }

    .job-header {
      align-items: center;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }

    .job-title {
      margin-right: 10rem;
    }

    .company-title {
      margin-right: 20rem;
    }
  `],
})

export class SearchJobListJobViewComponent implements OnInit {
  @Input() jobItem: any;
  @Input() enums: Enums;
  @Input() statuses: object;
  @Input() isEditable = true;

  public modalMode = false;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              private navigationService: NavigationService) {
  }

  ngOnInit() {
    if (this.modalData && this.modalData.jobItem) {
      this.jobItem = this.modalData.jobItem;
      this.enums = this.modalData.enums;
      this.modalMode = true;
    }
  }

  goToJobView(jobId) {
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }

  goToCompanyView(companyId: number) {
    this.navigationService.goToCompanyProfileViewPage(companyId.toString());
  }

  get appliedDateTooltip() {
    return `Applied on ${moment(this.jobItem.applied_at).format('L')}`;
  }
}
