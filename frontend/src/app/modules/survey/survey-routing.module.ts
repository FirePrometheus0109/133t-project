// Modules
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Guards
import { AuthGuard } from '../auth/services/auth-guard.service';

// Constants
import { SurveyRoute } from '../shared/constants/routes/survey-routes';

// Components
import { DefaultQuestionsComponent } from './containers/default-questions.container';
import { SavedQuestionsComponent } from './containers/saved-questions.container';
import { SurveyListComponent } from './containers/survey-list.container';
import { SurveyComponent } from './containers/survey.container';

// Resolvers
import { DefaultQuestionsPageResolver } from './resolvers/default-questions-page.resolver';
import { SavedQuestionsPageResolver } from './resolvers/saved-questions-page.resolver';
import { SurveyListPageResolver } from './resolvers/survey-list-page.resolver';

const SurveyRoutes: Routes = [
  {
    path: '',
    component: SurveyComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: SurveyRoute.defaultQuestionsRoute,
        component: DefaultQuestionsComponent,
        canActivate: [AuthGuard],
        resolve: {
          data: DefaultQuestionsPageResolver
        }
      },
      {
        path: SurveyRoute.savedQuestionsRoute,
        component: SavedQuestionsComponent,
        canActivate: [AuthGuard],
        resolve: {
          data: SavedQuestionsPageResolver
        }
      },
      {
        path: SurveyRoute.questionListRoute,
        component: SurveyListComponent,
        canActivate: [AuthGuard],
        resolve: {
          data: SurveyListPageResolver
        }
      },
    ],
  },
];


@NgModule({
  imports: [
    RouterModule.forChild(SurveyRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class SurveyRoutingModule {
}
