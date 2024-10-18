// Modules
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Guards
import { AuthGuard } from '../auth/services/auth-guard.service';
import { IsSubsctiptionPurchased } from '../subscription/services/subscription-guard.sevice';

// Constants
import { CandidateRoute } from '../shared/constants/routes/candidate-routes';

// Components
import { ViewAnsweredQuestionnaireComponent } from './containers/view-answered-questionnaire.container';
import { ViewCandidatesListPageComponent } from './containers/view-candidates-list/view-candidates-list.component';

// Resolvers
import { ViewAnsweredQuestionnaireResolver } from './resolvers/view-answered-questionnaire.resolver';
import { ViewCandidatesListResolver } from './resolvers/view-candidates-list.resolver';
import { ViewJobCandidatesResolver } from './resolvers/view-candidates-page.resolver';

const CandidateRoutes: Routes = [
  {
    path: CandidateRoute.companyJobCandidateRoute,
    component: ViewCandidatesListPageComponent,
    canActivate: [AuthGuard, IsSubsctiptionPurchased],
    resolve: {profileData: ViewJobCandidatesResolver},
  },
  {
    path: CandidateRoute.candidateAnswersRoute,
    component: ViewAnsweredQuestionnaireComponent,
    canActivate: [AuthGuard, IsSubsctiptionPurchased],
    resolve: {profileData: ViewAnsweredQuestionnaireResolver},
  },
  {
    path: CandidateRoute.candidateList,
    component: ViewCandidatesListPageComponent,
    canActivate: [AuthGuard, IsSubsctiptionPurchased],
    resolve: {profileData: ViewCandidatesListResolver},
  }
];


@NgModule({
  imports: [
    RouterModule.forChild(CandidateRoutes),
  ],
  exports: [
    RouterModule,
  ],
})
export class CandidateRoutingModule {
}
