import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NavigationService } from '../../core/services/navigation.service';
import { DateTimeHelper } from '../../shared/helpers/date-time.helper';
import { CandidateStatusEnum, Enums } from '../../shared/models/enums.model';


@Component({
  selector: 'app-view-candidate-item',
  template: `
    <mat-card class="content-container" *ngxPermissionsOnly="['view_candidate']">
      <div *ngIf="editable" class="checkbox-container">
        <mat-checkbox value="{{candidateItem.id}}" [name]="checkBoxName"></mat-checkbox>
      </div>
      <div class="candidate-container">
        <mat-card-content class="candidate-main-container">
          <div class="candidate-meta-items">
            <h4 class="candidate-title">
              <button mat-button (click)="goToCandidateProfilePage(candidateItem.id)">
                <span class="link">
                  {{candidateItem.job_seeker.user.first_name}} {{candidateItem.job_seeker.user.last_name}}
                </span>
              </button>
            </h4>
            <div>
              <button mat-button matTooltip="Quick view" (click)="provideQuickView.emit(index)">
                <mat-icon>search</mat-icon>
              </button>
            </div>
            <app-workflow-candidate [candidate]="candidateItem" [enums]="enums"
                                    (change)="onChangeCandidateWorkflow($event)"></app-workflow-candidate>
          </div>
          <div class="candidate-action-items">
            <app-assign-candidate-button [assignedUser]="[candidateItem.job_seeker]" [isCandidate]="true">
            </app-assign-candidate-button>
            <div>
              <ng-template [ngxPermissionsOnly]="['view_jobseekercomment']">
                <button mat-button (click)="commentCandidate.emit(candidateItem.job_seeker.id)">
                  <mat-icon matSuffix>comment</mat-icon>
                </button>
              </ng-template>
            </div>
            <app-rate-candidate [candidate]="candidateItem" [scoreValue]="candidateItem.rating.rating"
                                [forDisplay]="true"></app-rate-candidate>
          </div>
        </mat-card-content>
        <mat-card-content class="candidate-detail-container">
          <div>Applied on {{candidateItem.applied_date | date }}</div>
          <div *ngIf="!isJobMode">
            <button mat-button (click)="goToJobPostingPage(candidateItem.job.id)"><u>{{candidateItem.job.title}}</u></button>
          </div>
          <div *ngIf="candidateItem.is_applied_after_assignment">
            <mat-icon matSuffix [matTooltip]="getTooltipMessage(candidateItem)" matTooltipPosition="above"> warning</mat-icon>
          </div>
        </mat-card-content>
        <mat-card-content class="candidate-detail-container">
          <div>Updated on {{candidateItem.job_seeker.modified_at | date}}</div>
          <div *ngIf="candidateItem.is_disqualified_for_questionnaire"> Is Disqualified For Questionnaire</div>
          <div *ngIf="candidateItem.is_disqualified_for_skills"> Is Disqualified For Skills</div>
          <div *ngIf="candidateItem.job_seeker.is_deleted"> DELETED account</div>
        </mat-card-content>
      </div>
    </mat-card>`,
  styles: [`
    .content-container {
      display: flex;
      flex-direction: row;
    }

    .candidate-container {
      border-top: 3px solid rgba(0, 0, 0, 0.42);
      padding: 20px 50px 20px 30px;
      width: 75%;
    }

    .candidate-main-container {
      display: flex;
      flex-flow: row wrap;
      justify-content: space-between;
    }

    .candidate-detail-container {
      display: flex;
      flex-flow: row wrap;
    }

    .candidate-detail-container div {
      margin-right: 10px;
    }

    .candidate-detail-container button {
      line-height: 16px;
    }

    .candidate-action-items {
      display: flex;
    }

    .candidate-meta-items {
      display: flex;
    }

    h4 {
      margin-block-end: 0;
      margin-block-start: 0;
    }
  `]
})
export class ViewCandidateItemComponent {
  @Input() enums: Enums;
  @Input() candidateItem: any;
  @Input() checkBoxName: string;
  @Input() candidateStatus: CandidateStatusEnum;
  @Input() editable = true;
  @Input() index: number;
  @Input() isJobMode = false;
  @Output() commentCandidate = new EventEmitter<number>();
  @Output() provideQuickView = new EventEmitter<number>();
  @Output() change = new EventEmitter<number>();

  constructor(private navigationService: NavigationService) {
  }

  goToJobPostingPage(id: string) {
    this.navigationService.goToCompanyJobViewDetailsPage(id, true);
  }

  goToCandidateProfilePage(id: string) {
    this.navigationService.goToCandidateProfileViewPage(id, true);
  }

  getTooltipMessage(candidateItem) {
    return `Candidate already applied for this
    job posting on ${DateTimeHelper.getDate(candidateItem.created_at)}.`;
  }

  onChangeCandidateWorkflow(data) {
    this.change.emit(data);
  }
}
