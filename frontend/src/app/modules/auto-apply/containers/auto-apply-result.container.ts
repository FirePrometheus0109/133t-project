import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { ViewJobPreviewComponent } from '../../company/components/view-job-preview.component';
import { NavigationService } from '../../core/services/navigation.service';
import { CoreState } from '../../core/states/core.state';
import { JobSeekerProfilePageActions } from '../../job-seeker/actions';
import { ManualApplyActions } from '../../manual-apply/actions';
import { ManageApplyRequirementsDialogComponent } from '../../shared/components/manage-apply-requirements-dialog.component';
import { JsManageCoverLettersComponent } from '../../shared/components/manage-cover-letters/js-manage-cover-letters.container';
import { StatesStatuses } from '../../shared/enums/states-statuses';
import { CoverLetterApplyData } from '../../shared/models/cover-letter.model';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { AnswerQuestionsComponent } from '../../survey/components/answers/answer-questions.component';
import { AutoApplyEditActions, AutoApplyResultActions } from '../actions';
import { AutoApply, Job } from '../models/auto-apply.model';
import { AutoApplyService } from '../services/auto-apply.service';
import { AutoApplyResultState } from '../states/auto-apply-result.state';


@Component({
  selector: 'app-auto-apply-result-page',
  template: `
    <mat-card class="auto-apply">
      <mat-card-header>
        <mat-card-title>
          {{(autoApply$ | async).title}}
          <button *ngIf="checkIsAutoApplyStopped()"
                  type="button" mat-raised-button color="primary"
                  (click)="goToEdit()">Edit
            <mat-icon matSuffix>edit</mat-icon>
          </button>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div>
          <p>Status: {{(enums$ | async).AutoapplyStatusEnum[(autoApply$ | async).status]}}</p>
          <p *ngIf="(autoApply$ | async).days_to_completion">
            Days to completion: {{(autoApply$ | async).days_to_completion}}
          </p>
          <p>Search options: {{(queryParams$ | async) || 'none'}}</p>
          <p>Specify number of applications: {{(autoApply$ | async).number}}</p>
        </div>
      </mat-card-content>
    </mat-card>
    <div>
      <button *ngIf="checkIsAutoApplyInProgress()"
              type="button" mat-raised-button color="primary"
              (click)="stopAutoApply()">
        Stop applying process
        <mat-icon matSuffix>stop</mat-icon>
      </button>
      <button *ngIf="checkIsAutoApplyStopped() || checkIsAutoApplyFinished()"
              type="button" mat-raised-button color="primary"
              (click)="restartAutoApply()">
        Restart auto apply
        <mat-icon matSuffix>restore</mat-icon>
      </button>
      <button type="button" mat-raised-button color="primary"
              (click)="copyAutoApply()">
        Copy to new auto apply
        <mat-icon matSuffix>file_copy</mat-icon>
      </button>
      <mat-icon matSuffix
                matTooltip="Create new auto apply based on the current search criteria.
You will be able to edit any of the search criteria.">
        info
      </mat-icon>
    </div>
    <div>Queue</div>
    <mat-tab-group>
      <mat-tab label="All">
        <ng-template mat-tab-label>
          <span *ngIf="(autoApplyResultNewJobs$ | async).length === 0">All</span>
          <span *ngIf="(autoApplyResultNewJobs$ | async).length > 0"
                matBadge="{{(autoApplyResultNewJobs$ | async).length}}"
                matBadgeOverlap="false" matBadgeColor="warn">All</span>
        </ng-template>
        <ng-template matTabContent>
          <div *ngFor="let queueItem of (autoApplyResult$ | async)">
            <app-auto-apply-queue-item-preview *ngIf="!queueItem.is_deleted"
                                               [enums]="enums$ | async"
                                               [autoApplyQueueItem]="queueItem"
                                               [autoApplyResult]="queueItem"
                                               (applyForNewJob)="applyForNewJob($event)"
                                               (viewJobItem)="viewJobItemDetails($event)">
            </app-auto-apply-queue-item-preview>
            <app-deleted-job-view *ngIf="queueItem.is_deleted" [deletedJob]="queueItem">
            </app-deleted-job-view>
          </div>
        </ng-template>
      </mat-tab>
      <mat-tab>
        <ng-template mat-tab-label>
          <span matBadge="{{(autoApplyResultApplied$ | async).length}}"
                matBadgeOverlap="false" matBadgeColor="accent">Applied</span>
        </ng-template>
        <ng-template matTabContent>
          <app-auto-apply-queue-item-preview *ngFor="let queueItem of (autoApplyResultApplied$ | async)"
                                             [enums]="enums$ | async"
                                             [autoApplyQueueItem]="queueItem"
                                             [autoApplyResult]="queueItem"
                                             [isAppliedSection]="true"
                                             (reapplyForJob)="reapplyForJob($event)"
                                             (viewJobItem)="viewJobItemDetails($event)">
          </app-auto-apply-queue-item-preview>
        </ng-template>
      </mat-tab>
      <mat-tab>
        <ng-template mat-tab-label>
          <span matBadge="{{(autoApplyResultNeedReview$ | async).length}}"
                matBadgeOverlap="false" matBadgeColor="warn">Need review</span>
        </ng-template>
        <ng-template matTabContent>
          <app-auto-apply-queue-item-preview *ngFor="let queueItem of (autoApplyResultNeedReview$ | async)"
                                             [enums]="enums$ | async"
                                             [autoApplyQueueItem]="queueItem"
                                             [autoApplyResult]="queueItem"
                                             (offerAnswerQuestions)="offerAnswerQuestions($event)"
                                             (applyForNewJob)="applyForNewJob($event)"
                                             (provideCoverLetter)="provideCoverLetter($event)"
                                             (viewJobItem)="viewJobItemDetails($event)">
          </app-auto-apply-queue-item-preview>
        </ng-template>
      </mat-tab>
    </mat-tab-group>
  `,
  styles: [`
    .auto-apply {
      width: 40%;
    }
  `],
})
export class AutoApplyResultComponent implements OnInit {
  @Select(CoreState.enums) enums$: Observable<object>;
  @Select(CoreState.autoApplyEnums) autoApplyEnums$: Observable<object>;
  @Select(AutoApplyResultState.autoApply) autoApply$: Observable<AutoApply>;
  @Select(AutoApplyResultState.autoApplyResult) autoApplyResult$: Observable<AutoApply>;
  @Select(AutoApplyResultState.autoApplyResultApplied) autoApplyResultApplied$: Observable<Array<Job>>;
  @Select(AutoApplyResultState.autoApplyResultNeedReview) autoApplyResultNeedReview$: Observable<Array<Job>>;
  @Select(AutoApplyResultState.autoApplyResultNewJobs) autoApplyResultNewJobs$: Observable<Array<Job>>;
  @Select(AutoApplyResultState.queryParams) queryParams$: Observable<any>;

  private autoApplyId: number;
  private answerQuestionsConfirmationText = 'You need to answer questionnaire to apply for this job';
  public answerConfirmButtonText = 'Answer questionnaire';

  constructor(private store: Store,
              private autoApplyService: AutoApplyService,
              private route: ActivatedRoute,
              private navigationService: NavigationService,
              public dialog: MatDialog,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.autoApplyId = params.id;
    });
  }

  viewJobItemDetails(jobData: any) {
    this.store.dispatch(new AutoApplyResultActions.GetSelectedJob(jobData.jobId)).subscribe((state) => {
      const dialogRef = this.dialog.open(ViewJobPreviewComponent, {
        width: '80%',
        data: {
          jobItem: state.AutoApplyResult.selectedJobDetail,
          enums: state.core.enums,
          skillsToMatch: state.auth.user.job_seeker.skills,
          ...jobData
        },
      });
      dialogRef.componentInstance.reapplyForJob.subscribe((jobId: number) => {
        this.reapplyForJob(jobId);
        dialogRef.close();
      });
      dialogRef.afterClosed().subscribe(() => {
        dialogRef.componentInstance.reapplyForJob.unsubscribe();
        dialogRef.close();
      });
    });
  }

  offerAnswerQuestions(jobItem: Job) {
    this.store.dispatch(new AutoApplyResultActions.GetSelectedJob(jobItem.id)).subscribe(() => {
      const currentJob = this.store.selectSnapshot(AutoApplyResultState.selectedJobDetail);
      this.confirmationDialogService.openConfirmationDialog({
          message: `${this.answerQuestionsConfirmationText}`,
          callback: this.provideAnswerDialog.bind(this),
          arg: currentJob,
          confirmationText: `${this.answerConfirmButtonText}`,
          dismissible: true
        },
      );
    });
  }

  provideAnswerDialog(currentJob) {
    const answerDialogRef = this.dialog.open(AnswerQuestionsComponent, {
      width: '60%',
      data: {
        questions: currentJob.questions,
        jobData: currentJob,
      },
    });
    answerDialogRef.componentInstance.submittedResult.subscribe((response) => {
      if (response === StatesStatuses.DONE) {
        answerDialogRef.close();
        const currentAutoApply = this.store.selectSnapshot(AutoApplyResultState.autoApply);
        this.store.dispatch(new AutoApplyResultActions.GetAutoApplyResult(currentAutoApply.id));
      }
    });
    answerDialogRef.afterClosed().subscribe(() => {
      answerDialogRef.componentInstance.submittedResult.unsubscribe();
      answerDialogRef.close();
    });
  }

  provideCoverLetter(jobItem: Job) {
    this.store.dispatch(new JobSeekerProfilePageActions.LoadCoverLetterData(this.jsId));
    const provideCoverLetterDialogRef = this.dialog.open(ManageApplyRequirementsDialogComponent, {
      width: '60%',
      data: {
        is_questionnaire_answered: true,
        is_cover_letter_required: true
      },
    });
    provideCoverLetterDialogRef.componentInstance.manageCoverLetters.subscribe(() => {
      const dialogManageRef = this.dialog.open(JsManageCoverLettersComponent, {
        width: '40%',
        data: {
          isModal: true
        }
      });
      dialogManageRef.afterClosed().subscribe(() => {
        dialogManageRef.close();
      });
    });
    provideCoverLetterDialogRef.componentInstance.applyResult.subscribe((coverLetterData: CoverLetterApplyData) => {
      const currentAutoApply = this.store.selectSnapshot(AutoApplyResultState.autoApply);
      this.store.dispatch(new AutoApplyResultActions.SetCoverLetterForApply(currentAutoApply.id, jobItem.id, coverLetterData));
      provideCoverLetterDialogRef.close();
    });
    provideCoverLetterDialogRef.afterClosed().subscribe(() => {
      provideCoverLetterDialogRef.componentInstance.applyResult.unsubscribe();
      provideCoverLetterDialogRef.close();
    });
  }

  goToEdit() {
    this.navigationService.goToAutoApplyEditPage(this.autoApplyId.toString());
  }

  checkIsAutoApplyInProgress() {
    return this.autoApplyEnums.IN_PROGRESS === this.autoApplyEnums[this.autoApply.status];
  }

  checkIsAutoApplyFinished() {
    return this.autoApplyEnums.FINISHED === this.autoApplyEnums[this.autoApply.status];
  }

  checkIsAutoApplyStopped() {
    return this.autoApplyEnums.STOPPED === this.autoApplyEnums[this.autoApply.status];
  }

  stopAutoApply() {
    this.store.dispatch(new AutoApplyResultActions.StopAutoApply(this.autoApply.id));
  }

  restartAutoApply() {
    this.store.dispatch(new AutoApplyResultActions.RestartAutoApply(this.autoApply.id));
  }

  applyForNewJob(jobId) {
    this.store.dispatch(new AutoApplyResultActions.ApplyForNewJob(this.autoApply.id, jobId));
  }

  reapplyForJob(jobId: number) {
    this.store.dispatch(new ManualApplyActions.ReapplyForJob(jobId));
  }

  copyAutoApply() {
    this.store.dispatch(new AutoApplyEditActions.CreateAutoApplyFromId(this.autoApplyId));
  }

  get autoApply() {
    return this.store.selectSnapshot(AutoApplyResultState.autoApply);
  }

  get autoApplyEnums() {
    return this.store.selectSnapshot(CoreState.autoApplyEnums);
  }

  get jsId() {
    return this.store.selectSnapshot(AuthState.jobseekerId);
  }
}
