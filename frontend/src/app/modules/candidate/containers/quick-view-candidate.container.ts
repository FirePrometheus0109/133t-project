import { Component, Inject } from '@angular/core';
import { MatDialogRef } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { NavigationService } from '../../core/services/navigation.service';
import { CoreState } from '../../core/states/core.state';
import { Enums } from '../../shared/models/enums.model';
import { SalaryViewPipe } from '../../shared/pipes/salary-view.pipe';
import { QuickViewCandidateActions } from '../actions';
import { CandidateItem } from '../models/candidate-item.model';
import { QuickViewCandidateState } from '../states/quick-view-candidate.state';


// TODO: create new component in shared module to reuse common details sections here and in JS profile view
@Component({
  selector: 'app-quick-view-candidate',
  template: `
    <h3 mat-dialog-title>Quick View</h3>
    <mat-dialog-content>
      <div class="container">
        <div class="navigate-section">
          <button mat-button class="navigate-button" [disabled]="!(previous$ | async)" (click)="previousCandidate()">
            <mat-icon>navigate_before</mat-icon>
          </button>
        </div>
        <div class="candidate-view">
          <mat-card>
            <mat-card-header>
              <mat-card-title>{{(currentCandidate$ | async)?.job.title}}</mat-card-title>
            </mat-card-header>
            <mat-card-header>
              <div class="quick-view-header">
                <div class="info">
                  <img mat-card-avatar class="big-avatar" [src]="(currentCandidate$ | async)?.job_seeker?.photo?.original">
                  <mat-card-title>
                    <span class="navigate-link" (click)="goToCandidatePage()">
                      {{(currentCandidate$ | async)?.job_seeker?.user.first_name}}
                      {{(currentCandidate$ | async)?.job_seeker?.user.last_name}}
                    </span>
                  </mat-card-title>
                  <mat-card-subtitle>
                    Last updated date: {{(currentCandidate$ | async)?.job_seeker?.modified_at | date}}
                    <app-vjsp-shortcut-info [experience]="(currentCandidate$ | async)?.job_seeker?.job_experience"
                                            [addressData]="(currentCandidate$ | async)?.job_seeker?.address">
                    </app-vjsp-shortcut-info>
                  </mat-card-subtitle>
                </div>
                <div class="actions">
                  <app-rate-candidate [candidate]="(currentCandidate$ | async)?.job_seeker"
                                      [candidateId]="(currentCandidate$ | async)?.id"
                                      [scoreValue]="(currentCandidate$ | async)?.rating.rating">
                  </app-rate-candidate>
                  <app-workflow-candidate [candidate]="(currentCandidate$ | async)?.job_seeker"
                                          [candidateId]="(currentCandidate$ | async)?.id"
                                          [quickViewMode]="true"
                                          [candidateStatus]="(currentCandidate$ | async)?.status"
                                          [enums]="enums$ | async"
                                          (change)="candidateStatusChanged()">
                  </app-workflow-candidate>
                </div>
              </div>
            </mat-card-header>
            <mat-card-content>
              <div class="section">
                <div class="contacts" *ngIf="(currentCandidate$ | async)?.job_seeker?.is_purchased ||
                (currentCandidate$ | async)?.job_seeker?.is_applied">
                  <div>
                    Email: {{ (currentCandidate$ | async)?.job_seeker?.user.email }}
                  </div>
                  <div>
                    Phone: {{ (currentCandidate$ | async)?.job_seeker?.phone }}
                  </div>
                </div>
                <div>
                  <app-profile-address-view [addressData]="(currentCandidate$ | async)?.job_seeker?.address">
                  </app-profile-address-view>
                </div>
              </div>
              <div class="section">
                <mat-card-title>Profile details</mat-card-title>
                <div class="profile-details">
                  <div class="column">
                    <app-vjsp-profile-detail-value
                        [profileDetailName]="'Position type'"
                        [profileDetailValue]="(enums$ | async).PositionTypes[(currentCandidate$ | async)?.job_seeker?.position_type]">
                    </app-vjsp-profile-detail-value>
                    <app-vjsp-profile-detail-value
                        [profileDetailName]="'Education'"
                        [profileDetailValue]="(enums$ | async).EducationTypes[(currentCandidate$ | async)?.job_seeker?.education]">
                    </app-vjsp-profile-detail-value>
                    <app-vjsp-profile-detail-value
                        [profileDetailName]="'Years of experience'"
                        [profileDetailValue]="(enums$ | async).ExperienceTypes[(currentCandidate$ | async)?.job_seeker?.experience]">
                    </app-vjsp-profile-detail-value>
                    <app-vjsp-profile-detail-value
                        [profileDetailName]="'Travel opportunities'"
                        [profileDetailValue]="(enums$ | async).JSTravelOpportunities[(currentCandidate$ | async)?.job_seeker?.travel]">
                    </app-vjsp-profile-detail-value>
                  </div>
                  <div class="column">
                    <app-vjsp-profile-detail-value
                        [profileDetailName]="'Salary'"
                        [profileDetailValue]="salaryInfo">
                    </app-vjsp-profile-detail-value>
                    <app-vjsp-profile-detail-value
                        [profileDetailName]="'Clearance'"
                        [profileDetailValue]="(enums$ | async).ClearanceTypes[(currentCandidate$ | async)?.job_seeker?.clearance]">
                    </app-vjsp-profile-detail-value>
                    <app-vjsp-profile-detail-value
                        [profileDetailName]="'Benefits'"
                        [profileDetailValue]="(enums$ | async).Benefits[(currentCandidate$ | async)?.job_seeker?.benefits]">
                    </app-vjsp-profile-detail-value>
                  </div>
                </div>
              </div>
              <div class="section">
                <mat-card-title>About</mat-card-title>
                <mat-chip-list>
                  {{(currentCandidate$ | async)?.job_seeker?.about || '-'}}
                </mat-chip-list>
              </div>
              <div class="section">
                <mat-card-title>Skills</mat-card-title>
                <mat-chip-list>
                  <mat-chip *ngFor="let skill of (currentCandidate$ | async)?.job_seeker?.skills">{{ skill.name }}
                  </mat-chip>
                </mat-chip-list>
              </div>
              <div class="section">
                <mat-card-title>Education details</mat-card-title>
                <div *ngFor="let item of (currentCandidate$ | async)?.job_seeker?.educations">
                  <app-jsp-education-preview [educationItem]="item" [enums]="enums$ | async">
                  </app-jsp-education-preview>
                </div>
                <div *ngFor="let item of (currentCandidate$ | async)?.job_seeker?.certifications">
                  <app-jsp-certification-preview [certificationItem]="item">
                  </app-jsp-certification-preview>
                </div>
              </div>
              <div class="section">
                <mat-card-title>Experience</mat-card-title>
                <div *ngFor="let item of (currentCandidate$ | async)?.job_seeker?.job_experience">
                  <app-jsp-experience-preview [jobItem]="item"
                                              [onlyView]="true"
                                              [enums]="enums$ | async">
                  </app-jsp-experience-preview>
                </div>
              </div>
            </mat-card-content>
          </mat-card>
        </div>
        <div class="navigate-section">
          <button mat-button class="navigate-button" [disabled]="!(next$ | async)" (click)="nextCandidate()">
            <mat-icon>navigate_next</mat-icon>
          </button>
        </div>
      </div>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button [mat-dialog-close]>Close</button>
    </mat-dialog-actions>
  `,
  styles: [`
    .container {
      display: flex;
      flex-direction: row;
      width: 100%;
      height: 100%;
      justify-content: space-between;
      align-items: stretch;
    }

    .candidate-view {
      width: 90%;
    }

    .navigate-link {
      cursor: pointer;
    }

    .navigate-button {
      cursor: pointer;
      height: 100%;
    }

    .section {
      margin-bottom: 10px;
    }

    .profile-details {
      display: flex;
      flex-direction: row;
    }

    .quick-view-header {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
      width: 100%;
    }
  `],
})
export class QuickViewCandidateComponent {
  @Select(CoreState.enums) enums$: Observable<Enums>;
  @Select(QuickViewCandidateState.currentCandidate) currentCandidate$: Observable<CandidateItem>;
  @Select(QuickViewCandidateState.next) next$: Observable<any>;
  @Select(QuickViewCandidateState.previous) previous$: Observable<any>;

  constructor(private store: Store,
              private navigationService: NavigationService,
              private salaryViewPipe: SalaryViewPipe,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>) {
  }

  public goToCandidatePage() {
    this.navigationService.goToCandidateProfileViewPage(this.currentCandidate.id.toString(), true);
    this.dialogRef.close();
  }

  public nextCandidate() {
    this.store.dispatch(new QuickViewCandidateActions.ChangeCandidate(this.prepareQueryData(this.offset + 1)));
  }

  public previousCandidate() {
    this.store.dispatch(new QuickViewCandidateActions.ChangeCandidate(this.prepareQueryData(this.offset - 1)));
  }

  public get salaryInfo() {
    const {
      salary_min,
      salary_max,
    } = this.currentCandidate.job_seeker;
    return `${
      this.salaryViewPipe.transform(salary_min)
    } - ${
      this.salaryViewPipe.transform(salary_max)
    }`;
  }

  public candidateStatusChanged() {
    this.store.dispatch(new QuickViewCandidateActions.ChangeCandidate(this.prepareQueryData(this.offset)));
  }

  private prepareQueryData(newOffset: number) {
    const queryData = {
      limit: environment.quickViewLimit,
      offset: newOffset
    };
    if (this.currentSortingField) {
      Object.assign(queryData, {ordering: this.currentSortingField});
    }
    return queryData;
  }

  private get currentSortingField() {
    return this.store.selectSnapshot(QuickViewCandidateState.currentSortingField);
  }

  private get offset() {
    return this.store.selectSnapshot(QuickViewCandidateState.offset);
  }

  private get currentCandidate() {
    return this.store.selectSnapshot(QuickViewCandidateState.currentCandidate);
  }
}
