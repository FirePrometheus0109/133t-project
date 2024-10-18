import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { NavigationService } from '../../core/services/navigation.service';
import { CoreState } from '../../core/states/core.state';
import { CompanyProfilePageState } from '../states/company-profile-page.state';


@Component({
  selector: 'app-view-company-profile-page',
  template: `
    <app-view-company-profile [companyData]="companyData$ | async">
    </app-view-company-profile>
    <mat-card>
      <mat-card-title>Job list</mat-card-title>
      <app-job-preview *ngFor="let jobItem of jobData$ | async"
                       [jobItem]="jobItem"
                       [statuses]="JobStatusEnum$ | async"
                       [enums]="enums$ | async"
                       [canViewDetails]="true"
                       [isCompanyUser]="isCompanyUser$ | async"
                       (goToDetails)="goToDetails($event)">
      </app-job-preview>
    </mat-card>
  `,
  styles: [`
    :host {
      text-align: center;
    }
  `],
})
export class ViewCompanyProfilePageComponent {
  @Select(CompanyProfilePageState.initialData) companyData$: Observable<any>;
  @Select(CompanyProfilePageState.jobs) jobData$: Observable<any>;
  @Select(CoreState.enums) enums$: Observable<object>;
  @Select(CoreState.JobStatusEnum) JobStatusEnum$: Observable<object>;
  @Select(AuthState.isCompanyUser) isCompanyUser$: Observable<boolean>;

  constructor(private navigationService: NavigationService) {
  }

  goToDetails(jobId: number) {
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }
}
