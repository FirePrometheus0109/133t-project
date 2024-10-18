// Modules
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Guards
import { NgxPermissionsGuard } from 'ngx-permissions';
import { AuthGuard } from '../auth/services/auth-guard.service';
import { IsSubsctiptionPurchased } from '../subscription/services/subscription-guard.sevice';
import {DummyJobsComponent} from './containers/dummy-jobs.container';
import { EditJobPageComponent } from './containers/edit-job-page/edit-job-page.component';
import { CompanyGuard } from './services/company-guard.service';
import { CompanyMyGuard } from './services/company-my-guard.service';
import { CompanySubscriptionGuardService } from './services/company-subscription-guard.service';

// Constants
import { CompanyRoute } from '../shared/constants/routes/company-routes';

// Components
import { DashboardWrappedCalendarComponent } from './components/dashboard-wrapped-calendar.component';
import { CompanyUserListComponent } from './containers/company-user/company-user-list.container';
import { CompanyUserManageComponent } from './containers/company-user/company-user-manage.container';
import { CreateJobPageComponent } from './containers/create-job-page.container';
import { EditCompanyProfilePageComponent } from './containers/edit-company-profile-page.container';
import { EditJobListComponent } from './containers/edit-job-list.container';
import { LetterTemplateManageComponent } from './containers/letter-templates/letter-template-manage/letter-template-manage.component';
import { LetterTemplatesListComponent } from './containers/letter-templates/letter-templates-list/letter-templates-list.component';
import { SearchJobListPageComponent } from './containers/search-job-list-page/search-job-list-page.component';
import { ViewCompanyListPageComponent } from './containers/view-company-list.container';
import { ViewCompanyProfilePageComponent } from './containers/view-company-profile-page.container';
import { ViewJobDetailsJsComponent } from './containers/view-job-details-js.container';
import { ViewJobListPageComponent } from './containers/view-job-list.container';

// Resolvers
import { CompanyReportsComponent } from './containers/company-reports/company-reports.component';
import { CompanyDashboardComponent } from './containers/dashboard/company-dashboard/company-dashboard.component';
import { ViewCompanyDashboardPageResolver } from './resolvers/company-dashboard.resolver';
import { CompanyReportsResolver } from './resolvers/company-reports.resolver';
import { CompanyUserEditPageResolver } from './resolvers/company-user/company-user-edit-page.resolver';
import { CompanyUserInvitePageResolver } from './resolvers/company-user/company-user-invite-page.resolver';
import { CompanyUserListPageResolver } from './resolvers/company-user/company-user-list-page.resolver';
import { CompanyUserViewPageResolver } from './resolvers/company-user/company-user-view-page.resolver';
import { CreateJobPageResolver } from './resolvers/create-job-page.resolver';
import { EditCompanyProfilePageResolver } from './resolvers/edit-company-profile-page.resolver';
import { EditJobPageResolver } from './resolvers/edit-job-page.resolver';
import { LetterTemplateCreatePageResolver } from './resolvers/letter-templates/letter-template-create-page.resolver';
import { LetterTemplateEditPageResolver } from './resolvers/letter-templates/letter-template-edit-page.resolver';
import { LetterTemplateViewPageResolver } from './resolvers/letter-templates/letter-template-view-page.resolver';
import { LetterTemplatesListPageResolver } from './resolvers/letter-templates/letter-templates-list-page.resolver';
import { SearchJobListPageResolver } from './resolvers/search-job-list-page.resolver';
import { ViewCompanyListPageResolver } from './resolvers/view-company-list-page.resolver';
import { ViewCompanyProfilePageResolver } from './resolvers/view-company-profile-page.resolver';
import { ViewJobDetailsJsPageResolver } from './resolvers/view-job-details-js-page.resolver';
import { ViewJobDetailsJsPublicPageResolver } from './resolvers/view-job-details-js-public-page.resolver';
import { ViewJobListPageResolver } from './resolvers/view-job-list-page.resolver';

// CompanyCalendarModule for overriding route
import { CompanyCalendarPageResolver } from './modules/company-calendar/resolvers/calendar.resolver';
import { calendarRoute } from './modules/company-calendar/routes';

const CompanyRoutes: Routes = [
  // Public
  {
    path: CompanyRoute.companyListRoute,
    component: ViewCompanyListPageComponent,
    resolve: {companiesData: ViewCompanyListPageResolver},
  },
  {
    path: CompanyRoute.companyJobCreateRoute,
    component: CreateJobPageComponent,
    resolve: {profileData: CreateJobPageResolver},
  },
  {
    path: CompanyRoute.companyProfileViewRoute,
    component: ViewCompanyProfilePageComponent,
    resolve: {
      profileData: ViewCompanyProfilePageResolver,
    },
  },
  {
    path: CompanyRoute.companyJobSearchRoute,
    component: SearchJobListPageComponent,
    canActivate: [AuthGuard],
    resolve: {profileData: SearchJobListPageResolver},
  },
  {
    path: CompanyRoute.companyJobViewDetailsRoute,
    component: ViewJobDetailsJsComponent,
    canActivate: [AuthGuard],
    resolve: {data: ViewJobDetailsJsPageResolver},
  },
  {
    path: CompanyRoute.companyJobPublicViewDetailsRoute,
    component: ViewJobDetailsJsComponent,
    resolve: {data: ViewJobDetailsJsPublicPageResolver},
    data: {public: true}
  },
  {
    path: CompanyRoute.companyDashboard,
    component: CompanyDashboardComponent,
    canActivate: [AuthGuard],
    canDeactivate: [CompanySubscriptionGuardService],
    resolve: {data: ViewCompanyDashboardPageResolver},
  },
  {
    path: CompanyRoute.companyDummyJobsRoute,
    component: DummyJobsComponent,
  },
  // Non-Public
  {
    path: CompanyRoute.companyProfileEditRoute,
    component: EditCompanyProfilePageComponent,
    canActivate: [CompanyMyGuard, CompanyGuard, AuthGuard, IsSubsctiptionPurchased],
    resolve: {profileData: EditCompanyProfilePageResolver},
  },
  {
    path: CompanyRoute.companyJobEditRoute,
    component: EditJobPageComponent,
    canActivate: [CompanyGuard, AuthGuard, IsSubsctiptionPurchased],
    resolve: {profileData: EditJobPageResolver},
  },
  {
    path: CompanyRoute.companyJobViewListRoute,
    component: ViewJobListPageComponent,
    canActivate: [AuthGuard, IsSubsctiptionPurchased],
    resolve: {profileData: ViewJobListPageResolver},
  },
  {
    path: CompanyRoute.companyJobListRoute,
    component: EditJobListComponent,
    canActivate: [AuthGuard, IsSubsctiptionPurchased],
    resolve: {profileData: ViewJobListPageResolver},
  },
  // Company users
  {
    path: CompanyRoute.companyUsersListRoute,
    component: CompanyUserListComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased, NgxPermissionsGuard],
    resolve: {data: CompanyUserListPageResolver},
    data: {
      permissions: {
        only: ['view_companyuser', 'change_companyuser'],
      }
    }
  },
  {
    path: CompanyRoute.companyUserInviteRoute,
    component: CompanyUserManageComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased, NgxPermissionsGuard],
    resolve: {data: CompanyUserInvitePageResolver},
    data: {
      permissions: {
        only: ['add_companyuser'],
      }
    }
  },
  {
    path: CompanyRoute.companyUserViewRoute,
    component: CompanyUserManageComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased, NgxPermissionsGuard],
    resolve: {data: CompanyUserViewPageResolver},
    data: {
      permissions: {
        only: ['view_companyuser'],
      }
    }
  },
  {
    path: CompanyRoute.companyUserEditRoute,
    component: CompanyUserManageComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased, NgxPermissionsGuard],
    resolve: {data: CompanyUserEditPageResolver},
    data: {
      permissions: {
        only: ['change_companyuser'],
      }
    }
  },
  // Letter Templates
  {
    path: CompanyRoute.companyLetterTemplatesList,
    component: LetterTemplatesListComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased],
    resolve: {data: LetterTemplatesListPageResolver},
  },
  {
    path: CompanyRoute.companyLetterTemplateCreate,
    component: LetterTemplateManageComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased],
    resolve: {data: LetterTemplateCreatePageResolver},
  },
  {
    path: CompanyRoute.companyLetterTemplateView,
    component: LetterTemplateManageComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased],
    resolve: {data: LetterTemplateViewPageResolver},
  },
  {
    path: CompanyRoute.companyLetterTemplateEdit,
    component: LetterTemplateManageComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased],
    resolve: {data: LetterTemplateEditPageResolver},
  },
  {
    path: CompanyRoute.companyReports,
    component: CompanyReportsComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased],
    resolve: {data: CompanyReportsResolver}
  },
  // Override on "calendarRoute" of ./modules/company-calendar module
  {
    path: calendarRoute,
    component: DashboardWrappedCalendarComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased],
    resolve: {
      data: CompanyCalendarPageResolver,
      dashboarded: ViewCompanyDashboardPageResolver
    }
  },
];


@NgModule({
  imports: [
    RouterModule.forChild(CompanyRoutes),
  ],
  exports: [
    RouterModule,
  ],
})
export class CompanyRoutingModule {
}
