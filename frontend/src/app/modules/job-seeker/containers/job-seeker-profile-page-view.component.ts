import { Component, Inject, Input } from '@angular/core';
import { MatDialog } from '@angular/material';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { CandidateItem } from '../../candidate/models/candidate-item.model';
import { CommentsState } from '../../common-components/states/comments.state';
import { LogsState } from '../../common-components/states/logs.state';
import { NavigationService } from '../../core/services/navigation.service';
import { CoreState } from '../../core/states/core.state';
import { Enums } from '../../shared/models/enums.model';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { ViewAnswerComponent } from '../../survey/components/answers/view-answer.component';
import { JobSeekerProfilePageActions } from '../actions';
import { JSNameAndId } from '../models';
import { JSPPageState } from '../states/jsp-page.state';


@Component({
  selector: 'app-job-seeker-profile-page-view',
  template: `
    <div class="removed-from-print">
      <h4 mat-dialog-title *ngIf="isModal">Profile preview mode</h4>
      <h3 *ngIf="!shouldDisplayData()">Profile is hidden</h3>
      <mat-dialog-content *ngIf="shouldDisplayData()" [ngClass]="{'not-modal': !isModal}">
        <div class="container">
          <div>
            <mat-card class="info-with-buttons">
              <div>
                <img *ngIf="!isPrinting" mat-card-avatar class="big-avatar" [src]="(initialData$ | async)?.photo?.original">
                <mat-card-title>{{ (initialData$ | async)?.user.first_name }} {{ (initialData$ | async)?.user.last_name }}
                </mat-card-title>
                <app-vjsp-experience-detail
                    [experience]="experience$ | async"
                    [enums]="enums$ | async"
                    [short]="true"
                    [currentWork]="true">
                </app-vjsp-experience-detail>
                <div *ngIf="!(initialData$ | async)?.is_applied">
                  <app-purchase-profile-button *ngxPermissionsOnly="['is_company_user']"
                                               [id]="(NameAndId$ | async)?.id"
                                               [first_name]="(NameAndId$ | async)?.first_name"
                                               [last_name]="(NameAndId$ | async)?.last_name"
                                               [compactMode]="false"
                                               (purchaseComplete)="reloadUser($event)">
                  </app-purchase-profile-button>
                </div>
                <mat-card-subtitle>
                  <app-vjsp-shortcut-info [experience]="experience$ | async"
                                          [addressData]="(initialData$ | async)?.address"></app-vjsp-shortcut-info>
                </mat-card-subtitle>
                <div class="contacts" *ngIf="(initialData$ | async)?.is_purchased ||
              (initialData$ | async)?.is_applied || (isJobSeeker$ | async)">
                  <mat-card-subtitle>
                    Email: {{ (initialData$ | async)?.user.email }}
                  </mat-card-subtitle>
                  <mat-card-subtitle>
                    Phone: {{ (initialData$ | async)?.phone }}
                  </mat-card-subtitle>
                </div>
                <mat-card-subtitle>
                  <app-profile-address-view [addressData]="(initialData$ | async)?.address"></app-profile-address-view>
                </mat-card-subtitle>
              </div>
              <div class="info-with-buttons" *ngIf="!isModal">
                <div *ngIf="isAssignAvailable((initialData$ | async))">
                  <app-assign-candidate-button [assignedUser]="[initialData$ | async]"
                                               [isCandidate]="currentCandidate$ | async">
                  </app-assign-candidate-button>
                </div>
                <app-jsp-print-control [iconOnly]="true"
                                       [pending]="pending$ | async">
                </app-jsp-print-control>
                <div *ngIf="!isPublic && !hideFavorite">
                  <app-job-seeker-favorites-button *ngIf="!(currentCandidate$ | async)"
                                                   [id]="(initialData$ | async)?.id"
                                                   [isFavorite]="(initialData$ | async)?.saved_at"
                                                   (savedSuccessfully)="reloadUser()">
                  </app-job-seeker-favorites-button>
                </div>
              </div>
            </mat-card>

            <mat-card>
              <mat-card-title>
                About
              </mat-card-title>
              <mat-card-content>
                {{(initialData$ | async)?.about || '-'}}
              </mat-card-content>
            </mat-card>

            <mat-card>
              <mat-card-title>
                Profile details
              </mat-card-title>
              <div class="profile-details">
                <div class="column">
                  <app-vjsp-profile-detail-value
                      [profileDetailName]="'Position type'"
                      [profileDetailValue]="(enums$ | async).PositionTypes[(initialData$ | async)?.position_type]">
                  </app-vjsp-profile-detail-value>
                  <app-vjsp-profile-detail-value
                      [profileDetailName]="'Education'"
                      [profileDetailValue]="(enums$ | async).EducationTypes[(initialData$ | async)?.education]">
                  </app-vjsp-profile-detail-value>
                  <app-vjsp-profile-detail-value
                      [profileDetailName]="'Years of experience'"
                      [profileDetailValue]="(enums$ | async).ExperienceTypes[(initialData$ | async)?.experience]">
                  </app-vjsp-profile-detail-value>
                  <app-vjsp-profile-detail-value
                      [profileDetailName]="'Travel opportunities'"
                      [profileDetailValue]="(enums$ | async).JSTravelOpportunities[(initialData$ | async)?.travel]">
                  </app-vjsp-profile-detail-value>
                </div>
                <div class="column">
                  <app-vjsp-profile-detail-value
                      [profileDetailName]="'Salary'"
                      [profileDetailValue]="
                      ((initialData$ | async)?.salary_min | salaryView) +
                      ' - ' +
                      ((initialData$ | async)?.salary_max | salaryView)">
                  </app-vjsp-profile-detail-value>
                  <app-vjsp-profile-detail-value
                      [profileDetailName]="'Clearance'"
                      [profileDetailValue]="(enums$ | async).ClearanceTypes[(initialData$ | async)?.clearance]">
                  </app-vjsp-profile-detail-value>
                  <app-vjsp-profile-detail-value
                      [profileDetailName]="'Benefits'"
                      [profileDetailValue]="(enums$ | async).Benefits[(initialData$ | async)?.benefits]">
                  </app-vjsp-profile-detail-value>
                </div>
              </div>
            </mat-card>

            <mat-card *ngIf="(initialData$ | async)?.skills.length">
              <mat-card-title>Skills</mat-card-title>
              <mat-chip-list>
                <mat-chip *ngFor="let skill of (initialData$ | async)?.skills">{{ skill.name }}</mat-chip>
              </mat-chip-list>
            </mat-card>

            <mat-card *ngIf="(educationAndCertificationData$ | async)?.length">
              <mat-card-title>Education details</mat-card-title>
              <app-vjsp-education-detail [educationAndCertificationData]="educationAndCertificationData$ | async"
                                         [enums]="enums$ | async">
              </app-vjsp-education-detail>
            </mat-card>

            <mat-card *ngIf="(experience$ | async)?.length">
              <mat-card-title>Experience</mat-card-title>
              <app-vjsp-experience-detail [experience]="experience$ | async" [enums]="enums$ | async">
              </app-vjsp-experience-detail>
            </mat-card>

            <ng-template [ngxPermissionsOnly]="['view_jobseekercomment']">
              <mat-card>
                <mat-accordion>
                  <mat-expansion-panel>
                    <mat-expansion-panel-header>
                      <mat-panel-title>
                        <div>
                          Comments
                        </div>
                        <div matBadge="{{(commentsCount$ | async)}}" [matBadgeColor]="'accent'">
                          <mat-icon>comment</mat-icon>
                        </div>
                      </mat-panel-title>
                    </mat-expansion-panel-header>
                    <app-comments></app-comments>
                  </mat-expansion-panel>
                </mat-accordion>
              </mat-card>
            </ng-template>
            <ng-template [ngxPermissionsOnly]="['view_log']">
              <mat-card>
                <mat-accordion>
                  <mat-expansion-panel>
                    <mat-expansion-panel-header>
                      <mat-panel-title>
                        <div>
                          Logs
                        </div>
                        <div matBadge="{{(logsCount$ | async)}}" [matBadgeColor]="'accent'">
                          <mat-icon>history</mat-icon>
                        </div>
                      </mat-panel-title>
                    </mat-expansion-panel-header>
                    <app-logs></app-logs>
                  </mat-expansion-panel>
                </mat-accordion>
              </mat-card>
            </ng-template>
          </div>

          <div *ngxPermissionsOnly="['is_company_user']">
            <app-job-seeker-profile-manage-widget *ngIf="currentCandidate$ | async">
              <ng-container ngProjectAs="body">
                <div>
                  <app-rate-candidate [candidate]="currentCandidate$ | async" [scoreValue]="(currentCandidate$ | async)?.rating.rating">
                  </app-rate-candidate>
                  <div class="detail-section">
                    <span class="link" (click)="goToCandidateJob()">
                      {{(currentCandidate$ | async)?.job?.title}}
                    </span>
                  </div>
                  <div class="detail-section">Applied on {{(currentCandidate$ | async)?.applied_date | date}}</div>
                  <app-workflow-candidate [candidate]="currentCandidate$ | async" [enums]="enums$ |async">
                  </app-workflow-candidate>
                  <div class="detail-section" *ngIf="(answeredQuestionnaire$ | async)?.length">
                    <span class="link" (click)="viewAnsweredQuestionnaire()">
                      Answered questionnaire
                    </span>
                  </div>

                  <div class="detail-section" *ngIf="(currentCandidate$ | async)?.cover_letter">
                    <span class="link" (click)="viewCoverLetter()">
                      View Cover Letter
                    </span>
                  </div>
                </div>
                <div class="detail-section">
                  <cc-event-creator></cc-event-creator>
                </div>
              </ng-container>
            </app-job-seeker-profile-manage-widget>
          </div>
        </div>
      </mat-dialog-content>
      <mat-dialog-actions align="end" *ngIf="isModal">
        <button mat-raised-button color="accent" [matDialogClose]>
          <mat-icon matSuffix>close</mat-icon>
          Close
        </button>
      </mat-dialog-actions>
    </div>
    <router-outlet name="print"></router-outlet>
  `,
  styles: [`
    @media print {
      :host {
        text-align: unset !important;
      }
    }

    .container {
      display: flex;
    }

    :host {
      text-align: center;
    }

    .profile-details {
      display: flex;
      flex-direction: row;
    }

    .column {
      align-items: center;
      display: flex;
      flex-direction: column;
      width: 50%;
    }

    .avatar {
      object-fit: cover;
      margin-bottom: 30px;
    }

    .avatar.big-avatar {
      height: 200px;
      width: 200px;
    }

    mat-panel-title {
      flex-direction: column;
    }

    .not-modal {
      display: initial;
    }

    .info-with-buttons {
      display: flex;
      justify-content: space-around;
    }

    .detail-section {
      margin: 15px 0;
    }
  `],
})
export class JobSeekerProfilePageViewComponent {
  @Select(JSPPageState.NameAndId) NameAndId$: Observable<JSNameAndId>;
  @Select(JSPPageState.initialData) initialData$: Observable<any>;
  @Select(JSPPageState.experience) experience$: Observable<any>;
  @Select(JSPPageState.errors) errors$: Observable<any>;
  @Select(JSPPageState.educationAndCertificationData) educationAndCertificationData$: Observable<any>;
  @Select(JSPPageState.currentCandidate) currentCandidate$: Observable<CandidateItem>;
  @Select(JSPPageState.answeredQuestionnaire) answeredQuestionnaire$: Observable<any>;
  @Select(CoreState.enums) enums$: Observable<Enums>;
  @Select(CommentsState.commentsCount) commentsCount$: Observable<number>;
  @Select(LogsState.logsCount) logsCount$: Observable<number>;
  @Select(AuthState.isJobSeeker) isJobSeeker$: Observable<boolean>;

  @Input() hideFavorite = false;
  @Input() isPrinting = false;

  public isPublic: boolean;

  constructor(@Inject(MAT_DIALOG_DATA) public dialogData: any,
              private dialog: MatDialog,
              private store: Store,
              private navigationService: NavigationService,
              private messageDialog: ConfirmationDialogService,
              private route: ActivatedRoute) {
    this.isPublic = this.route.snapshot.data.public;
  }

  reloadUser() {
    const currentJobSeeker = this.store.selectSnapshot(JSPPageState.initialData);
    const currentCandidate = this.store.selectSnapshot(JSPPageState.currentCandidate);
    currentCandidate
      ? this.store.dispatch(new JobSeekerProfilePageActions.LoadJobSeekerAsCandidate(currentCandidate.id))
      : this.store.dispatch(new JobSeekerProfilePageActions.LoadCurrentJobSeeker(currentJobSeeker.id));
  }

  isAssignAvailable(data) {
    return data.is_applied || data.is_purchased;
  }

  public shouldDisplayData() {
    const initialLoadingErrorsState = this.store.selectSnapshot(JSPPageState.errors);
    return !(this.isPublic && initialLoadingErrorsState);
  }

  public goToCandidateJob() {
    const jobId = this.store.selectSnapshot(JSPPageState.currentCandidate).job.id;
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }

  public viewAnsweredQuestionnaire() {
    this.showAnswerModal();
  }

  public viewCoverLetter() {
    const currentCandidate = this.store.selectSnapshot(JSPPageState.currentCandidate);
    const coverLetter = currentCandidate.cover_letter;
    const title = `Cover letter ${coverLetter.title} for ${currentCandidate.job.title}
    ${currentCandidate.job_seeker.user.first_name}
       ${currentCandidate.job_seeker.user.last_name}`;
    const args = {message: coverLetter.body, title: title};
    this.messageDialog.openConfirmationDialog(args);
  }

  public get isModal() {
    return this.dialogData && this.dialogData.isModal;
  }

  private showAnswerModal() {
    const dialogRef = this.dialog.open(ViewAnswerComponent, {
      width: '60%',
      data: {
        answers: this.store.selectSnapshot(JSPPageState.answeredQuestionnaire)
      },
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.close();
    });
  }
}
