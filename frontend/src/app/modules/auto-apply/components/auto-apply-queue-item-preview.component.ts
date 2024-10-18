import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NavigationService } from '../../core/services/navigation.service';
import { Enums } from '../../shared/models/enums.model';
import { JobMatchingService } from '../services/job-matching.service';


@Component({
  selector: 'app-auto-apply-queue-item-preview',
  template: `
    <div class="queue-item-preview"
         [ngClass]="{'colored': checkIsJobApplicable(), 'new': checkIsJobNew()}">
      <mat-card>
        <mat-card-actions>
          <div *ngIf="!autoApplyResult && isJobInApplyingProcess()">
            <button mat-button *ngIf="checkIsJobStopped()" (click)="startJob()">
              <mat-icon matSuffix>play_circle_filled_white</mat-icon>
            </button>
            <button mat-button *ngIf="!checkIsJobStopped()" (click)="stopJob()">
              <mat-icon matSuffix>stop</mat-icon>
            </button>
          </div>
          <div *ngIf="autoApplyResult">
            <mat-icon matSuffix
                      *ngIf="enums.ApplyStatusEnum[autoApplyResult.apply_job_status] === enums.ApplyStatusEnum.APPLIED"
                      matTooltip="Applied on {{autoApplyResult.created_at | date}}">check_circle
            </mat-icon>
            <mat-icon matSuffix
                      *ngIf="!checkIsJobMatch()"
                      matTooltipClass="jsp-profile-validation-tooltip"
                      matTooltip="{{jobMatchingService.getValidationMessage(autoApplyQueueItem)}}">info
            </mat-icon>
            <mat-icon matSuffix
                      *ngIf="!checkQuestionnaireAnswers()"
                      matTooltip="Answer questionnaire"
                      (mouseover)="offerAnswerQuestions.emit(autoApplyResult)">
              live_help
            </mat-icon>
            <button mat-button *ngIf="enums.ApplyStatusEnum[autoApplyResult.apply_job_status] !== enums.ApplyStatusEnum.APPLIED &&
            checkIsJobMatch()" (click)="applyForNewJob.emit(autoApplyQueueItem.id)">
              <mat-icon matSuffix>present_to_all</mat-icon>
              Apply
            </button>
            <div *ngIf="isAppliedSection">
              <button mat-button *ngIf="isAppliedSection"
                      [disabled]="!checkIsJobMatch()"
                      (click)="reapplyForJob.emit(autoApplyQueueItem.id)">
                <mat-icon matSuffix>present_to_all</mat-icon>
                Reapply
              </button>
            </div>
          </div>
          <mat-icon matSuffix *ngIf="editMode && jobMatchingService.getValidationMessage(autoApplyQueueItem)"
                    matTooltipClass="jsp-profile-validation-tooltip"
                    matTooltip="{{jobMatchingService.getValidationMessage(autoApplyQueueItem)}}">
            info
          </mat-icon>
          <div *ngIf="isAppliedSection && autoApplyQueueItem.applied_at">Applied on {{autoApplyQueueItem.applied_at | date}}</div>
        </mat-card-actions>
        <mat-card-header>
          <mat-card-title>
            <h3>{{autoApplyQueueItem.title}}</h3>
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div>Company: <span class="link" (click)="goToCompanyProfile()">{{autoApplyQueueItem.company.name}}</span></div>
          <div>Location: {{autoApplyQueueItem.location.city.name}} ({{autoApplyQueueItem.location.city.state.abbreviation}})</div>
          <div>Match: {{autoApplyQueueItem.matching_percent | number:'1.0-0'}}%</div>
          <div>Posted: {{autoApplyQueueItem.created_at | date}}</div>
        </mat-card-content>
      </mat-card>
      <mat-card>
        <mat-card-header>
          <mat-card-title>
            <h3>Details</h3>
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <app-job-metadata [jobItem]="autoApplyQueueItem"
                            [enums]="enums">
          </app-job-metadata>
        </mat-card-content>
        <mat-card-actions align="center">
          <button mat-button (click)="viewJobItemDetails()"
                  matTooltip="View job's details">
            <mat-icon matSuffix>remove_red_eye</mat-icon>
          </button>
          <button mat-button *ngIf="!autoApplyResult" (click)="deleteJobFromList()">
            <mat-icon matSuffix>delete</mat-icon>
          </button>
          <button mat-button *ngIf="checkIsJobNew()" (click)="applyForNewJob.emit(autoApplyQueueItem.id)">
            <mat-icon matSuffix>present_to_all</mat-icon>
            Apply
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
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

    .colored {
      border: 2px solid #ffA500;
    }

    .new {
      border: 2px solid #008000;
    }
  `],
})
export class AutoApplyQueueItemPreviewComponent {
  @Input() autoApplyQueueItem: any;
  @Input() autoApplyResult: any;
  @Input() enums: Enums;
  @Input() index: number;
  @Input() specifyNumber: number;
  @Input() stopped_jobs: any;
  @Input() applied_jobs: any;
  @Input() editMode: boolean;
  @Input() isAppliedSection: boolean;
  @Output() deleteJobItem = new EventEmitter<number>();
  @Output() viewJobItem = new EventEmitter<any>();
  @Output() startJobItem = new EventEmitter<number>();
  @Output() stopJobItem = new EventEmitter<number>();
  @Output() applyForNewJob = new EventEmitter<number>();
  @Output() reapplyForJob = new EventEmitter<number>();
  @Output() offerAnswerQuestions = new EventEmitter<any>();
  @Output() provideCoverLetter = new EventEmitter<any>();

  constructor(public jobMatchingService: JobMatchingService,
              private navigationService: NavigationService) {
  }

  public checkIsJobStopped() {
    if (this.stopped_jobs) {
      return this.stopped_jobs.find(id => id === +this.autoApplyQueueItem.id);
    }
  }

  public checkIsJobApplicable() {
    if (this.applied_jobs) {
      return this.applied_jobs.find(id => id === +this.autoApplyQueueItem.id);
    }
  }

  public checkIsJobNew() {
    return this.enums.ApplyStatusEnum[this.autoApplyQueueItem.apply_job_status] === this.enums.ApplyStatusEnum.NEW;
  }

  public deleteJobFromList() {
    this.deleteJobItem.emit(this.autoApplyQueueItem.id);
  }

  public viewJobItemDetails() {
    this.viewJobItem.emit(this.prepareDataForView());
  }

  public startJob() {
    this.startJobItem.emit(this.autoApplyQueueItem.id);
  }

  public stopJob() {
    this.stopJobItem.emit(this.autoApplyQueueItem.id);
  }

  public goToCompanyProfile() {
    this.navigationService.goToCompanyProfileViewPage(this.autoApplyQueueItem.company.id.toString());
  }

  checkQuestionnaireAnswers() {
    return this.autoApplyResult.is_questionnaire_answered;
  }

  checkCoverLetter() {
    return ((this.autoApplyResult.is_cover_letter_required && this.autoApplyResult.is_cover_letter_provided) ||
      (!this.autoApplyResult.is_cover_letter_required && !this.autoApplyResult.is_cover_letter_provided));
  }

  checkIsJobMatch() {
    return this.autoApplyResult.is_required_skills_match &&
      this.autoApplyResult.is_clearance_match && this.autoApplyResult.is_education_match &&
      this.checkCoverLetter() && this.checkQuestionnaireAnswers();
  }

  private prepareDataForView() {
    if (this.autoApplyResult) {
      return {
        isJobVerified: this.checkIsJobMatch() &&
        this.enums.ApplyStatusEnum[this.autoApplyResult.apply_job_status] === this.enums.ApplyStatusEnum.APPLIED,
        jobId: this.autoApplyResult.id
      };
    } else {
      return {jobId: this.autoApplyQueueItem.id};
    }
  }

  isJobInApplyingProcess() {
    return this.applied_jobs.find(id => id === +this.autoApplyQueueItem.id) ||
      this.stopped_jobs.find(id => id === +this.autoApplyQueueItem.id);
  }
}
