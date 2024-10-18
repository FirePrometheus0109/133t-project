// Modules
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Services
import { AuthGuard } from '../auth/services/auth-guard.service';
import { IsSubsctiptionPurchased } from '../subscription/services/subscription-guard.sevice';
import { IsJobSeekerGuard } from './services/job-seeker-guard.service';
import { JSPMyGuard } from './services/jsp-my-guard.service';

// Constants
import { JobSeekerRoute } from '../shared/constants/routes/job-seeker-routes';

// Components
import { SettingsComponent } from '../common-components/components/settings.container';
import { JobSeekerDashboardComponent } from './containers/dashboard/job-seeker-dashboard/job-seeker-dashboard.component';
import { JobSeekerAppliedListComponent } from './containers/job-seeker-applied-list-view.container';
import { JobSeekerPrintViewComponent } from './containers/job-seeker-print-view/job-seeker-print-view.component';
import { JobSeekerProfilePageViewComponent } from './containers/job-seeker-profile-page-view.component';
import { JobSeekerProfilePageComponent } from './containers/job-seeker-profile-page.component';
import { JobSeekerSavedJobsListComponent } from './containers/job-seeker-saved-jobs-list/job-seeker-saved-jobs-list.component';
import { ViewJobSeekerListComponent } from './containers/view-job-seeker-list/view-job-seeker-list.component';

// Resolvers
import { AppliedJobsListPageResolver } from './resolvers/applied-jobs-list-page.resolver';
import { JobSeekerProfilePublicPageResolver } from './resolvers/job-seaker-profile-public-page.resolver';
import { JobSeekerAsCandidatePageResolver } from './resolvers/job-seeker-as-candidate-page.resolver';
import { JobSeekerDashboardPageResolver } from './resolvers/job-seeker-dashboard-page.resolver';
import { JobSeekerProfilePageResolver } from './resolvers/job-seeker-profile-page.resolver';
import { JobSeekerSettingsPageResolver } from './resolvers/job-seeker-settings-page.resolver';
import { ViewPurchasedJobSeekersListResolver } from './resolvers/js-purchased-list.resolver';
import { ViewSavedJobSeekersListResolver } from './resolvers/js-saved-list.resolver';
import { ViewJobSeekersListResolver } from './resolvers/view-job-seeker-list.resolver';

const JobSeekerRoutes: Routes = [
  {
    path: JobSeekerRoute.jobSeekerProfileEditRoute,
    component: JobSeekerProfilePageComponent,
    canActivate: [JSPMyGuard, AuthGuard],
    resolve: {
      profileData: JobSeekerProfilePageResolver,
    },
    children: [
      {
        path: JobSeekerRoute.jobSeekerPrintProfile,
        outlet: JobSeekerRoute.printOutletName,
        component: JobSeekerPrintViewComponent
      }
    ]
  },
  {
    path: JobSeekerRoute.jobSeekerPublicProfile,
    component: JobSeekerProfilePageViewComponent,
    resolve: {profileData: JobSeekerProfilePublicPageResolver},
    data: {public: true}
  },
  {
    path: JobSeekerRoute.jobSeekerProfileViewRoute,
    component: JobSeekerProfilePageViewComponent,
    canActivate: [JSPMyGuard, AuthGuard],
    resolve: {
      profileData: JobSeekerProfilePageResolver,
    },
    children: [
      {
        path: JobSeekerRoute.jobSeekerPrintProfile,
        outlet: JobSeekerRoute.printOutletName,
        component: JobSeekerPrintViewComponent
      }
    ]
  },
  {
    path: JobSeekerRoute.jobSeekerAppliedJobs,
    component: JobSeekerAppliedListComponent,
    canActivate: [JSPMyGuard, AuthGuard],
    resolve: {
      data: AppliedJobsListPageResolver
    },
  },
  {
    path: JobSeekerRoute.jobSeekerSavedJobs,
    component: JobSeekerSavedJobsListComponent,
    canActivate: [JSPMyGuard, AuthGuard],
    resolve: {},
  },
  {
    path: JobSeekerRoute.jobSeekerProfileSettings,
    component: SettingsComponent,
    canActivate: [JSPMyGuard, AuthGuard],
    resolve: {
      settingsData: JobSeekerSettingsPageResolver
    },
  },
  {
    path: JobSeekerRoute.jobSeekerList,
    component: ViewJobSeekerListComponent,
    canActivate: [AuthGuard],
    resolve: {profileData: ViewJobSeekersListResolver},
  },
  {
    path: JobSeekerRoute.jobSeekerPurchasedList,
    component: ViewJobSeekerListComponent,
    canActivate: [AuthGuard],
    resolve: {profileData: ViewPurchasedJobSeekersListResolver},
  },
  {
    path: JobSeekerRoute.jobSeekerSavedList,
    component: ViewJobSeekerListComponent,
    canActivate: [AuthGuard],
    resolve: {profileData: ViewSavedJobSeekersListResolver},
  },
  {
    path: JobSeekerRoute.jobSeekerAsCandidateProfilePage,
    component: JobSeekerProfilePageViewComponent,
    canActivate: [AuthGuard, IsSubsctiptionPurchased],
    resolve: {profileData: JobSeekerAsCandidatePageResolver},
    children: [
      {
        path: JobSeekerRoute.jobSeekerPrintProfile,
        outlet: JobSeekerRoute.printOutletName,
        component: JobSeekerPrintViewComponent
      }
    ]
  },
  {
    path: JobSeekerRoute.jobSeekerDashboardPage,
    component: JobSeekerDashboardComponent,
    canActivate: [AuthGuard, IsJobSeekerGuard],
    resolve: {profileData: JobSeekerDashboardPageResolver},
  },
];


@NgModule({
  imports: [
    RouterModule.forChild(JobSeekerRoutes),
  ],
  exports: [
    RouterModule,
  ],
})
export class JobSeekerRoutingModule {
}
