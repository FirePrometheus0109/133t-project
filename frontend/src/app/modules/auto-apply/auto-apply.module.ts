// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxsModule } from '@ngxs/store';
import { MaterialModule } from '../material';
import { SharedModule } from '../shared';
import { SurveyModule } from '../survey/survey.module';
import { AutoApplyRoutingModule } from './auto-apply-routing.module';

// Components
import { ViewJobPreviewComponent } from '../company/components/view-job-preview.component';
import { ConfirmationDialogComponent } from '../shared/components/confirmation-dialog.component';
import { ManageApplyRequirementsDialogComponent } from '../shared/components/manage-apply-requirements-dialog.component';
import { StopJobDialogComponent } from '../shared/components/stop-job-dialog.component';
import { AnswerQuestionsComponent } from '../survey/components/answers/answer-questions.component';
import { AutoApplyEditFormComponent } from './components/auto-apply-edit-form.component';
import { AutoApplyPreviewComponent } from './components/auto-apply-preview.component';
import { AutoApplyQueueItemPreviewComponent } from './components/auto-apply-queue-item-preview.component';
import { AutoApplySearchFormComponent } from './components/auto-apply-search-form.component';

// Containers
import { JsManageCoverLettersComponent } from '../shared/components/manage-cover-letters/js-manage-cover-letters.container';
import { AutoApplyEditComponent } from './containers/auto-apply-edit.container';
import { AutoApplyListComponent } from './containers/auto-apply-list.container';
import { AutoApplyResultComponent } from './containers/auto-apply-result.container';

// Resolvers
import { AutoApplyCreatePageResolver } from './resolvers/auto-apply-create-page.resolver';
import { AutoApplyEditPageResolver } from './resolvers/auto-apply-edit-page.resolver';
import { AutoApplyListPageResolver } from './resolvers/auto-apply-list-page.resolver';
import { AutoApplyResultPageResolver } from './resolvers/auto-apply-result-page.resolver';

// Services
import { JobService } from '../company/services/job.service';
import { CanDeactivateGuard } from '../shared/services/page-leaving-guard.service';
import { AutoApplyService } from './services/auto-apply.service';
import { JobMatchingService } from './services/job-matching.service';

// States
import { AutoApplyEditState } from './states/auto-apply-edit.state';
import { AutoApplyListState } from './states/auto-apply-list.state';
import { AutoApplyResultState } from './states/auto-apply-result.state';

export const AUTO_APPLY_COMPONENTS = [
  // containers
  AutoApplyListComponent,
  AutoApplyEditComponent,
  AutoApplyResultComponent,
  // components
  AutoApplyPreviewComponent,
  AutoApplySearchFormComponent,
  AutoApplyQueueItemPreviewComponent,
  AutoApplyEditFormComponent,
];


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MaterialModule,
    SharedModule,
    SurveyModule,
    AutoApplyRoutingModule,
    NgxsModule.forFeature([
      AutoApplyListState,
      AutoApplyEditState,
      AutoApplyResultState,
    ]),
  ],
  declarations: AUTO_APPLY_COMPONENTS,
  exports: AUTO_APPLY_COMPONENTS,
  providers: [
    AutoApplyListPageResolver,
    AutoApplyCreatePageResolver,
    AutoApplyEditPageResolver,
    AutoApplyResultPageResolver,
    AutoApplyService,
    JobService,
    JobMatchingService,
    CanDeactivateGuard
  ],
  entryComponents: [
    ViewJobPreviewComponent,
    ConfirmationDialogComponent,
    ManageApplyRequirementsDialogComponent,
    JsManageCoverLettersComponent,
    StopJobDialogComponent,
    AnswerQuestionsComponent
  ],
})
export class AutoApplyModule {
}
