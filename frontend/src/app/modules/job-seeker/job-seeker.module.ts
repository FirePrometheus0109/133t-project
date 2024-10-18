// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxsModule } from '@ngxs/store';
import { CandidateModule } from '../candidate/candidate.module';
import { CommonComponentsModule } from '../common-components';
import { MaterialModule } from '../material';
import { SharedModule } from '../shared';
import { JobSeekerRoutingModule } from './job-seeker-routing.module';

import { CompanyCalendarModule } from '../company/modules/company-calendar';

// Services
import { ConfirmationDialogService } from '../shared/services/confirmation-dialog.service';
import { SurveyService } from '../survey/services/survey.service';

// Components
import { AssignCandidateComponent } from '../candidate/containers/assign-candidate.container';
import { ConfirmationDialogComponent } from '../shared/components/confirmation-dialog.component';
import { AnswerQuestionsComponent } from '../survey/components/answers/answer-questions.component';
import { ViewAnswerComponent } from '../survey/components/answers/view-answer.component';
import { AppliedJobComponent } from './components/applied-job.component';
import { JspCertificationComponent } from './components/education/jsp-certification.component';
import { JspEducationListComponent } from './components/education/jsp-education-list.component';
import { JspEducationComponent } from './components/education/jsp-education.component';
import { JspExperienceFormComponent } from './components/experience/jsp-exerience-form.component';
import { JspExperienceListComponent } from './components/experience/jsp-experience-list.component';
import {
  JobSeekerAutoApplyProgressItemComponent
} from './components/job-seeker-auto-apply-progress-item/job-seeker-auto-apply-progress-item.component';
import { JobSeekerItemComponent } from './components/job-seeker-item/job-seeker-item.component';
import { JspAboutViewComponent } from './components/job-seeker-profile-views/jsp-about-view/jsp-about-view.component';
import { JspAddressViewComponent } from './components/job-seeker-profile-views/jsp-address-view/jsp-address-view.component';
import { JspMainInfoViewComponent } from './components/job-seeker-profile-views/jsp-main-info-view/jsp-main-info-view.component';
import {
  JspProfileDetailsViewComponent
} from './components/job-seeker-profile-views/jsp-profile-details-view/jsp-profile-details-view.component';
import { JspSkillsViewComponent } from './components/job-seeker-profile-views/jsp-skills-view/jsp-skills-view.component';
import { JspAboutComponent } from './components/jsp-about.component';
import { JSPMainInfoFormComponent } from './components/jsp-main-info-form.component';
import { JspPrintControlComponent } from './components/jsp-print-control.component';
import { JspPublishProfileComponent } from './components/jsp-publish-profile.component';
import { JspShareLinkAccessControlComponent } from './components/jsp-share-link-access-control.component';
import { LastViewItemComponent } from './components/last-view-item/last-view-item.component';
import { ProfileCompletionViewComponent } from './components/profile-completion-view/profile-completion-view.component';
import { VjspEducationDetailComponent } from './components/profile-detail/vjsp-education-detail.component';
import { VjspExperienceDetailComponent } from './components/profile-detail/vjsp-experience-detail-container.component';
import { SavedJobComponent } from './components/saved-job/saved-job.component';
import {
  JobSeekerAutoApplyProgressComponent
} from './containers/dashboard/job-seeker-auto-apply-progress/job-seeker-auto-apply-progress.component';
import { JobSeekerDashboardComponent } from './containers/dashboard/job-seeker-dashboard/job-seeker-dashboard.component';
import {
  JobSeekerLastViewsListComponent
} from './containers/dashboard/job-seeker-last-views-list/job-seeker-last-views-list.component';
import { JobSeekerAppliedListComponent } from './containers/job-seeker-applied-list-view.container';
import { JobSeekerPrintViewComponent } from './containers/job-seeker-print-view/job-seeker-print-view.component';
import { JobSeekerProfileManageWidgetComponent } from './containers/job-seeker-profile-manage-widget';
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
import { ViewJobSeekersListResolver } from './resolvers/view-job-seeker-list.resolver';

// States
import { ViewSavedJobSeekersListResolver } from './resolvers/js-saved-list.resolver';
import { ViewAppliedJobListPageState } from './states/job-seeker-applied-list-view.states';
import { JobSeekerDashboardState } from './states/job-seeker-dashboard.state';
import { JSPPageState } from './states/jsp-page.state';
import { ViewJobSeekerListState } from './states/view-job-seeker-list.state';

export const JOB_SEEKER_COMPONENTS = [
  JspPrintControlComponent,
  JobSeekerPrintViewComponent,
  JSPMainInfoFormComponent,
  JobSeekerProfilePageComponent,
  JspAboutComponent,
  JspEducationListComponent,
  JspEducationComponent,
  JspCertificationComponent,
  JspExperienceFormComponent,
  JspExperienceListComponent,
  JobSeekerProfilePageViewComponent,
  VjspExperienceDetailComponent,
  AppliedJobComponent,
  JobSeekerAppliedListComponent,
  JspPublishProfileComponent,
  VjspEducationDetailComponent,
  JobSeekerProfileManageWidgetComponent,
  JobSeekerItemComponent,
  ViewJobSeekerListComponent,
  ProfileCompletionViewComponent,
  JobSeekerSavedJobsListComponent,
  SavedJobComponent,
  JspMainInfoViewComponent,
  JspAddressViewComponent,
  JspAboutViewComponent,
  JspProfileDetailsViewComponent,
  JspSkillsViewComponent,
  JspShareLinkAccessControlComponent,
  JobSeekerDashboardComponent,
  JobSeekerLastViewsListComponent,
  LastViewItemComponent,
  JobSeekerAutoApplyProgressComponent,
  JobSeekerAutoApplyProgressItemComponent,
];


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MaterialModule,
    SharedModule,
    JobSeekerRoutingModule,
    CommonComponentsModule,
    CandidateModule,
    CompanyCalendarModule,
    NgxsModule.forFeature([
      JSPPageState,
      ViewAppliedJobListPageState,
      ViewJobSeekerListState,
      JobSeekerDashboardState
    ]),
  ],
  declarations: JOB_SEEKER_COMPONENTS,
  exports: JOB_SEEKER_COMPONENTS,
  providers: [
    JobSeekerProfilePageResolver,
    JobSeekerProfilePublicPageResolver,
    ViewJobSeekersListResolver,
    JobSeekerAsCandidatePageResolver,
    ViewPurchasedJobSeekersListResolver,
    ViewSavedJobSeekersListResolver,
    JobSeekerDashboardPageResolver,
    JobSeekerSettingsPageResolver,
    AppliedJobsListPageResolver,
    SurveyService,
    ConfirmationDialogService,
  ],
  entryComponents: [
    ConfirmationDialogComponent,
    ViewAnswerComponent,
    AnswerQuestionsComponent,
    AssignCandidateComponent
  ],
})
export class JobSeekerModule {
}
