// Modules
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Services
import { AuthGuard } from './modules/auth/services/auth-guard.service';

// Components
import { HomePageComponent } from './modules/core/containers/home-page.component';
import { NotFoundPageComponent } from './modules/core/containers/not-found-page.component';

// Constants
import { AutoApplyRoute } from './modules/shared/constants/routes/auto-apply-routes';
import { CandidateRoute } from './modules/shared/constants/routes/candidate-routes';
import { CompanyRoute } from './modules/shared/constants/routes/company-routes';
import { JobSeekerRoute } from './modules/shared/constants/routes/job-seeker-routes';
import { NotificationRoute } from './modules/shared/constants/routes/notifications-routes';
import { SubscriptionRoute } from './modules/shared/constants/routes/subscription-routes';
import { SurveyRoute } from './modules/shared/constants/routes/survey-routes';

export const routes: Routes = [
  {path: '', component: HomePageComponent},
  {
    path: JobSeekerRoute.rootRoute,
    loadChildren: './modules/job-seeker/job-seeker.module#JobSeekerModule',
  },
  {
    path: CompanyRoute.rootRoute,
    loadChildren: './modules/company/company.module#CompanyModule',
  },
  {
    path: AutoApplyRoute.rootRoute,
    loadChildren: './modules/auto-apply/auto-apply.module#AutoApplyModule',
    canActivate: [AuthGuard],
  },
  {
    path: CandidateRoute.rootRoute,
    loadChildren: './modules/candidate/candidate.module#CandidateModule',
    canActivate: [AuthGuard],
  },
  {
    path: SurveyRoute.rootRoute,
    loadChildren: './modules/survey/survey.module#SurveyModule',
    canActivate: [AuthGuard],
  },
  {
    path: SubscriptionRoute.rootRoute,
    loadChildren: './modules/subscription/subscription.module#SubscriptionModule',
    canActivate: [AuthGuard]
  },
  {
    path: NotificationRoute.rootRoute,
    loadChildren: './modules/notifications/notifications.module#NotificationsModule',
    canActivate: [AuthGuard]
  },
  {path: '**', component: NotFoundPageComponent},
];


@NgModule({
  imports: [RouterModule.forRoot(routes, {useHash: true})],
  exports: [RouterModule],
})
export class AppRoutingModule {
}
