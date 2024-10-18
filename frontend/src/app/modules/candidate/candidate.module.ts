// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxsModule } from '@ngxs/store';
import { CommonComponentsModule } from '../common-components';
import { MaterialModule } from '../material';
import { SharedModule } from '../shared';
import { CandidateRoutingModule } from './candidate.routing.module';

// Services
import { CompanyService } from '../company/services/company.service';
import { JobService } from '../company/services/job.service';

// Components
import { AssignCandidateButtonComponent } from './components/assign-candidate-button.component';
import { QuickListItemComponent } from './components/quick-list-item/quick-list-item.component';
import { RateCadidateComponent } from './components/rate-candidate.component';
import { ViewCandidateAnswerComponent } from './components/view-answer.component';
import { ViewCandidateItemComponent } from './components/view-candidate-list-item.component';
import { AppliedUserComponent } from './components/view-candidate.component';
import { WorkflowCandidateComponent } from './components/workflow-candidate.component';

// Containers
import { CommentsComponent } from '../common-components/containers/comments.container';
import { AssignCandidateComponent } from './containers/assign-candidate.container';
import { CandidatesQuickListComponent } from './containers/candidates-quick-list/candidates-quick-list.component';
import { QuickViewCandidateComponent } from './containers/quick-view-candidate.container';
import { ViewAnsweredQuestionnaireComponent } from './containers/view-answered-questionnaire.container';
import { ViewCandidatesListPageComponent } from './containers/view-candidates-list/view-candidates-list.component';

// Resolvers
import { ViewAnsweredQuestionnaireResolver } from './resolvers/view-answered-questionnaire.resolver';
import { ViewCandidatesListResolver } from './resolvers/view-candidates-list.resolver';
import { ViewJobCandidatesResolver } from './resolvers/view-candidates-page.resolver';

// States
import { AssignCandidateState } from './states/assign-candidate.state';
import { CandidatesQuickListState } from './states/candidates-quick-list.state';
import { QuickViewCandidateState } from './states/quick-view-candidate.state';
import { ViewAnsweredQuestionnaireState } from './states/view-answered-questionnaire.state';
import { ViewCandidatesListPageState } from './states/view-candidates-list.states';

export const CANDIDATE_COMPONENTS = [
  AppliedUserComponent,
  ViewAnsweredQuestionnaireComponent,
  ViewCandidateAnswerComponent,
  AssignCandidateComponent,
  AssignCandidateButtonComponent,
  ViewCandidatesListPageComponent,
  ViewCandidateItemComponent,
  RateCadidateComponent,
  WorkflowCandidateComponent,
  QuickViewCandidateComponent,
  QuickViewCandidateComponent,
  CandidatesQuickListComponent,
  QuickListItemComponent
];


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MaterialModule,
    SharedModule,
    CandidateRoutingModule,
    CommonComponentsModule,
    NgxsModule.forFeature([
      ViewAnsweredQuestionnaireState,
      AssignCandidateState,
      ViewCandidatesListPageState,
      QuickViewCandidateState,
      CandidatesQuickListState
    ])
  ],
  declarations: CANDIDATE_COMPONENTS,
  exports: CANDIDATE_COMPONENTS,
  providers: [
    JobService,
    CompanyService,
    ViewJobCandidatesResolver,
    ViewAnsweredQuestionnaireResolver,
    ViewCandidatesListResolver
  ],
  entryComponents: [
    AssignCandidateComponent,
    CommentsComponent,
    QuickViewCandidateComponent,
  ]
})
export class CandidateModule {
}
