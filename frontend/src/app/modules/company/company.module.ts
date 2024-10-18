// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgxsModule } from '@ngxs/store';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { CommonComponentsModule } from '../common-components';
import { ManualApplyModule } from '../manual-apply';
import { MaterialModule } from '../material';
import { SharedModule } from '../shared';
import { SurveyModule } from '../survey';
import { CompanyRoutingModule } from './company-routing.module';
import {DummyJobsComponent} from './containers/dummy-jobs.container';
import { CompanyCalendarModule } from './modules/company-calendar';

// Components
import { ManualApplyButtonComponent } from '../manual-apply/components/manual-apply-button.component';
import { SelectSurveyDialogComponent } from '../survey/components/select-survey-dialog.component';
import { AppFilterJobComponent } from './components/app-filter-job.component';
import { CandidateActivityItemComponent } from './components/candidate-activity-item/candidate-activity-item.component';
import { CandidatePageButtonComponent } from './components/candidate-page-button.component';
import { CompanyProfileInfoFormComponent } from './components/company-profile-info-form.component';
import { CompanyReportsGraphComponent } from './components/company-reports-graph/company-reports-graph.component';
import { CompanyUserFormComponent } from './components/company-user/company-user-form.component';
import { CompanyUserPermissionGroupComponent } from './components/company-user/company-user-permission-group.component';
import { CompanyUserPermissionComponent } from './components/company-user/company-user-permissions.component';
import { CompanyUserPreviewComponent } from './components/company-user/company-user-preview.component';
import { CompanyUserShortcutInfoComponent } from './components/company-user/company-user-shortcut-info.component';
import { DashboardWrappedCalendarComponent } from './components/dashboard-wrapped-calendar.component';
import { JobCoverLetterRequiredFormComponent } from './components/job-forms/job-cover-letter-required-form.component';
import { JobDateFormComponent } from './components/job-forms/job-date-form.component';
import { JobDescriptionFormComponent } from './components/job-forms/job-description-form.component';
import { JobStatusFormComponent } from './components/job-forms/job-status-form.component';
import { JobTitleFormComponent } from './components/job-forms/job-title-form.component';
import { JobPreviewComponent } from './components/job-preview.component';
import { LetterTemplateFromComponent } from './components/letter-templates/letter-template-from/letter-template-from.component';
import {
  LetterTemplateItemComponent
} from './components/letter-templates/letter-template-list-item/letter-template-list-item.component';
import { LetterTemplateViewComponent } from './components/letter-templates/letter-template-view/letter-template-view.component';
import {
  SelectLetterTemplateEventTypeComponent
} from './components/letter-templates/select-letter-template-event-type/select-letter-template-event-type.component';
import { SearchJobListJobViewComponent } from './components/search-job-list-job-view.component';
import { ViewCompanyProfileComponent } from './components/view-company-profile.component';
import { ViewJobPreviewComponent } from './components/view-job-preview.component';
import { ViewJobViewersComponent } from './components/view-job-viewers.component';
import { EditJobPageComponent } from './containers/edit-job-page/edit-job-page.component';
import { SearchJobListPageComponent } from './containers/search-job-list-page/search-job-list-page.component';

// Containers
import { CommentsComponent } from '../common-components/containers/comments.container';
import { CompanyReportsComponent } from './containers/company-reports/company-reports.component';
import { CompanyUserListComponent } from './containers/company-user/company-user-list.container';
import { CompanyUserManageComponent } from './containers/company-user/company-user-manage.container';
import { CreateJobPageComponent } from './containers/create-job-page.container';
import {
  DashboardCandidatesActivityComponent
} from './containers/dashboard/dashboard-candidates-activity/dashboard-candidates-activity.component';
import { DashboardNewestJobsComponent } from './containers/dashboard/dashboard-newest-jobs/dashboard-newest-jobs.component';
import { EditCompanyProfilePageComponent } from './containers/edit-company-profile-page.container';
import { EditJobListComponent } from './containers/edit-job-list.container';
import { LetterTemplateManageComponent } from './containers/letter-templates/letter-template-manage/letter-template-manage.component';
import { LetterTemplatesListComponent } from './containers/letter-templates/letter-templates-list/letter-templates-list.component';
import { ShareJobControlComponent } from './containers/share-job-control/share-job-control.component';
import { ShareJobDialogComponent } from './containers/share-job-control/share-job-dialog.component';
import { ViewCompanyListPageComponent } from './containers/view-company-list.container';
import { ViewCompanyProfilePageComponent } from './containers/view-company-profile-page.container';
import { ViewJobDetailsJsComponent } from './containers/view-job-details-js.container';
import { ViewJobListPageComponent } from './containers/view-job-list.container';

// Resolvers
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

// Services
import { CompanyLetterTemplatesService } from './services/company-letter-templates.service';
import { CompanyUserService } from './services/company-user.service';
import { CompanyService } from './services/company.service';
import { JobService } from './services/job.service';

// States
import { SubscriptionModule } from '../subscription/subscription.module';
import { RecruiterActivityWidgetComponent } from './components/recruiter-activity-widget/recruiter-activity-widget.component';
import { WorkflowStatsWidgetComponent } from './components/workflow-stats-widget/workflow-stats-widget.component';
import { CompanyDashboardComponent } from './containers/dashboard/company-dashboard/company-dashboard.component';
import { ScoreCardStatsComponent } from './containers/dashboard/score-card-stats/score-card-stats.component';
import { ViewCompanyDashboardPageResolver } from './resolvers/company-dashboard.resolver';
import { CompanyReportsResolver } from './resolvers/company-reports.resolver';
import { CompanyDashboardState } from './states/company-dashboard.state';
import { CompanyProfilePageState } from './states/company-profile-page.state';
import { CompanyReportsState } from './states/company-reports.state';
import { CompanyUserListPageState } from './states/company-user-list-page.state';
import { CompanyUserManagePageState } from './states/company-user-manage-page.state';
import { CreateJobPageState } from './states/create-job-page.state';
import { EditJobPageState } from './states/edit-job-page.state';
import { LetterTemplateManagePageState } from './states/letter-templates/letter-template-manage-page.state';
import { LetterTemplatesListState } from './states/letter-templates/letter-templates-list-page.state';
import { SearchJobListPageState } from './states/search-job-list-page.state';
import { ViewCompanyListPageState } from './states/view-company-list-page.state';
import { ViewJobDetailsJsPageState } from './states/view-job-details-js-page.state';
import { ViewJobListPageState } from './states/view-job-list-page.state';
import { ViewJobViewerPageState } from './states/view-job-viewers.state';

export const COMPANY_COMPONENTS = [
  // containers
  CreateJobPageComponent,
  EditCompanyProfilePageComponent,
  EditJobListComponent,
  ViewCompanyProfilePageComponent,
  ViewJobListPageComponent,
  EditJobPageComponent,
  ViewCompanyListPageComponent,
  SearchJobListPageComponent,
  CompanyUserListComponent,
  CompanyUserManageComponent,
  CompanyReportsComponent,
  DashboardCandidatesActivityComponent,
  DashboardNewestJobsComponent,
  LetterTemplatesListComponent,
  LetterTemplateManageComponent,
  ShareJobControlComponent,
  DummyJobsComponent,
  // components
  CompanyProfileInfoFormComponent,
  ViewJobPreviewComponent,
  JobPreviewComponent,
  ViewCompanyProfileComponent,
  JobDateFormComponent,
  JobDescriptionFormComponent,
  JobTitleFormComponent,
  JobStatusFormComponent,
  SearchJobListJobViewComponent,
  ViewJobDetailsJsComponent,
  CandidatePageButtonComponent,
  AppFilterJobComponent,
  ViewJobViewersComponent,
  CompanyUserPreviewComponent,
  CompanyUserFormComponent,
  CompanyUserPermissionComponent,
  CompanyUserPermissionGroupComponent,
  CompanyUserShortcutInfoComponent,
  JobCoverLetterRequiredFormComponent,
  CompanyDashboardComponent,
  CompanyReportsGraphComponent,
  RecruiterActivityWidgetComponent,
  WorkflowStatsWidgetComponent,
  CandidateActivityItemComponent,
  ShareJobDialogComponent,
  ScoreCardStatsComponent,
  LetterTemplateItemComponent,
  LetterTemplateFromComponent,
  SelectLetterTemplateEventTypeComponent,
  LetterTemplateViewComponent,
  DashboardWrappedCalendarComponent
];


@NgModule({
  imports: [
    FormsModule,
    CommonModule,
    ReactiveFormsModule,
    MaterialModule,
    SharedModule,
    CompanyRoutingModule,
    FlexLayoutModule,
    SurveyModule,
    SubscriptionModule,
    ManualApplyModule,
    CommonComponentsModule,
    NgxChartsModule,
    NgxsModule.forFeature([
      CompanyProfilePageState,
      CreateJobPageState,
      ViewJobListPageState,
      EditJobPageState,
      ViewCompanyListPageState,
      SearchJobListPageState,
      ViewJobDetailsJsPageState,
      ViewJobViewerPageState,
      CompanyUserListPageState,
      CompanyUserManagePageState,
      CompanyDashboardState,
      CompanyReportsState,
      LetterTemplatesListState,
      LetterTemplateManagePageState,
    ]),
    // Company calendar module with state and all logic
    CompanyCalendarModule
  ],
  declarations: COMPANY_COMPONENTS,
  exports: COMPANY_COMPONENTS,
  providers: [
    CompanyService,
    JobService,
    CompanyUserService,
    CompanyLetterTemplatesService,
    EditCompanyProfilePageResolver,
    EditJobPageResolver,
    CreateJobPageResolver,
    ViewJobListPageResolver,
    ViewCompanyListPageResolver,
    ViewCompanyProfilePageResolver,
    SearchJobListPageResolver,
    ViewJobDetailsJsPageResolver,
    ViewJobDetailsJsPublicPageResolver,
    CompanyUserListPageResolver,
    CompanyUserInvitePageResolver,
    CompanyUserViewPageResolver,
    CompanyUserEditPageResolver,
    ViewCompanyDashboardPageResolver,
    CompanyReportsResolver,
    LetterTemplatesListPageResolver,
    LetterTemplateCreatePageResolver,
    LetterTemplateViewPageResolver,
    LetterTemplateEditPageResolver
  ],
  entryComponents: [
    ViewJobPreviewComponent,
    SelectSurveyDialogComponent,
    ViewJobViewersComponent,
    ManualApplyButtonComponent,
    CommentsComponent,
    SelectLetterTemplateEventTypeComponent,
    ShareJobDialogComponent
  ],
})
export class CompanyModule {
}
