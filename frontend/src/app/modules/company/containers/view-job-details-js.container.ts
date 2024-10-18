import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { ViewCandidateListPageActions } from '../../candidate/actions';
import { CommentsState } from '../../common-components/states/comments.state';
import { LogsState } from '../../common-components/states/logs.state';
import { NavigationService } from '../../core/services/navigation.service';
import { CoreState } from '../../core/states/core.state';
import { ViewJobDetailsJSPageActions } from '../actions';
import { ViewJobDetailsJsPageState } from '../states/view-job-details-js-page.state';


@Component({
  selector: 'app-view-job-details-page',
  template: `
    <app-candidate-statistic-panel *ngIf="!(isJobSeeker$ | async)"
                                   [panelData]="(jobData$ | async)?.candidates_count"
                                   (navigateToCandidates)="goToCandidatesPage($event)">
    </app-candidate-statistic-panel>
    <app-view-job-preview [jobItem]="jobData$ | async"
                          [enums]="enums$ | async"
                          [isViewDetailsAsJS]="!isPublic && isJobSeeker$ | async"
                          [isEditable]="false"
                          [matchMode]="!isPublic && isJobSeeker$ | async"
                          (cancel)="goToFindJobListPage()"
                          (applyForJob)="applyForJob($event)"
                          (navigateToCompany)="navigateToCompany($event)">
    </app-view-job-preview>
    <ng-template *ngIf="!isPublic" [ngxPermissionsOnly]="['view_jobseekercomment']">
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
    <ng-template *ngIf="!isPublic" [ngxPermissionsOnly]="['view_log']">
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
  `,
  styles: [`
    :host {
      text-align: center;
    }

    mat-panel-title {
      flex-direction: column;
    }
  `],
})
export class ViewJobDetailsJsComponent implements OnInit {
  @Select(ViewJobDetailsJsPageState.jobData) jobData$: Observable<any>;
  @Select(CoreState.enums) enums$: Observable<object>;
  @Select(AuthState.isJobSeeker) isJobSeeker$: Observable<boolean>;
  @Select(CommentsState.commentsCount) commentsCount$: Observable<number>;
  @Select(LogsState.logsCount) logsCount$: Observable<number>;

  private jobId: number;
  public isPublic: boolean;

  constructor(private route: ActivatedRoute,
              private store: Store,
              private navigationService: NavigationService) {
    this.isPublic = this.route.snapshot.data.public;
  }

  ngOnInit() {
    this.jobId = this.route.snapshot.params['jobId'];
  }

  goToFindJobListPage() {
    this.navigationService.goToJobSearchPage();
  }

  applyForJob(jobItem) {
    this.store.dispatch(new ViewJobDetailsJSPageActions.ApplyForJob(jobItem.id));
  }

  goToCandidatesPage(item) {
    const status = this.store.selectSnapshot(CoreState.CandidateStatuses).find(candidateStatus =>
      candidateStatus.name.toLowerCase() === item.key);
    this.store.dispatch(new ViewCandidateListPageActions.InitJobCandidateList(status));
    this.navigationService.goToViewCandidatesPage(this.jobId.toString());
  }

  navigateToCompany(companyId: number) {
    this.navigationService.goToCompanyProfileViewPage(companyId.toString());
  }
}
