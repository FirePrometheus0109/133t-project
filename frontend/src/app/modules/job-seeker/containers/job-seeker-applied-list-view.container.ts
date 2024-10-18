import { Component } from '@angular/core';
import { MatDialog } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { NavigationService } from '../../core/services/navigation.service';
import { CoreState } from '../../core/states/core.state';
import { ViewAnswerComponent } from '../../survey/components/answers/view-answer.component';
import { JobSeekerAppliedListActions } from '../actions';
import { ViewAppliedJobListPageState } from '../states/job-seeker-applied-list-view.states';


@Component({
  selector: 'app-job-seeker-applied-list-view',
  template: `
    <div *ngFor="let jobItem of (jobData$ |async)">
      <app-applied-job *ngIf="!jobItem.is_deleted"
                       [jobItem]="jobItem"
                       [enums]="enums$ | async"
                       [isAppliedShow]="true"
                       (goToCompanyProfile)="goToCompanyProfile($event)"
                       (viewAnsweredQuestionnaire)="viewAnsweredQuestionnaire($event)"
                       (goToJobView)="goToJobView($event)">
      </app-applied-job>
      <app-deleted-job-view *ngIf="jobItem.is_deleted" [deletedJob]="jobItem">
      </app-deleted-job-view>
    </div>
  `,
  styles: [],
})
export class JobSeekerAppliedListComponent {
  @Select(CoreState.appliedJobData) jobData$: Observable<any>;
  @Select(CoreState.enums) enums$: Observable<object>;

  constructor(private store: Store,
              private navigationService: NavigationService,
              private dialog: MatDialog) {
  }

  viewAnsweredQuestionnaire(job) {
    const currentJSId = this.store.selectSnapshot(AuthState.jobseekerId);
    this.store.dispatch(new JobSeekerAppliedListActions.LoadAnswersForJob(job.id, currentJSId)).subscribe(() => {
      this.showAnswerModal();
    });
  }

  goToCompanyProfile(companyId: number) {
    this.navigationService.goToCompanyProfileViewPage(companyId.toString());
  }

  goToJobView(jobId: number) {
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }

  private showAnswerModal() {
    const dialogRef = this.dialog.open(ViewAnswerComponent, {
      width: '60%',
      data: {
        answers: this.store.selectSnapshot(ViewAppliedJobListPageState.answersForJob)
      },
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.close();
    });
  }
}
