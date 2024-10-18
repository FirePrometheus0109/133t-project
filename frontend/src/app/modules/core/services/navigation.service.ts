import { Injectable } from '@angular/core';
import { NavigationEnd, Params, Router } from '@angular/router';
import { Store } from '@ngxs/store';
import { BehaviorSubject } from 'rxjs';
import { AuthRoute } from '../../shared/constants/routes/auth-routes';
import { AutoApplyRoute } from '../../shared/constants/routes/auto-apply-routes';
import { BaseRoute } from '../../shared/constants/routes/base-routes';
import { CandidateRoute } from '../../shared/constants/routes/candidate-routes';
import { CompanyRoute } from '../../shared/constants/routes/company-routes';
import { JobSeekerRoute } from '../../shared/constants/routes/job-seeker-routes';
import { NotificationRoute } from '../../shared/constants/routes/notifications-routes';
import { SubscriptionRoute } from '../../shared/constants/routes/subscription-routes';
import { CoreActions } from '../actions';


@Injectable({
  providedIn: 'root',
})
export class NavigationService {
  public currentUrl = new BehaviorSubject<string>(undefined);

  constructor(private store: Store, private router: Router) {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.currentUrl.next(event.urlAfterRedirects);
      }
    });
  }

  // General
  public goToHomePage(isCompanyUser?: boolean) {
    if (isCompanyUser) {
      this.goToCompanyDashboardPage();
    } else {
      this.redirectTo('/');
    }
  }

  public goTo404() {
    this.redirectTo(BaseRoute.notFoundRoute);
  }

  // Auth
  public goToLoginPage() {
    this.redirectTo(AuthRoute.loginRoute);
  }

  public goToCompanySignUpPage() {
    this.redirectTo(AuthRoute.companySignupRoute);
  }

  public goToJobSeekerSignUpPage() {
    this.redirectTo(AuthRoute.jobSeekerSignupRoute);
  }

  public goToAccountPage() {
    this.redirectTo(AuthRoute.accountRoute);
  }

  public goToForgotPasswordPage() {
    this.redirectTo(AuthRoute.forgotPassword);
  }

  public goToSetPasswordPage() {
    this.redirectTo(AuthRoute.setPasswordForSocialLoginRoute);
  }

  // Job seeker
  public goToJobSeekerProfileEditPage(id: string) {
    this.redirectTo(JobSeekerRoute.getFullRouteWithId(JobSeekerRoute.jobSeekerProfileEditRoute, JobSeekerRoute.id, id));
  }

  public goToJobSeekerProfileViewPage(id: string) {
    this.redirectTo(JobSeekerRoute.getFullRouteWithId(JobSeekerRoute.jobSeekerProfileViewRoute, JobSeekerRoute.id, id));
  }

  public goToJobSeekerProfileSettings(id: any) {
    this.redirectTo(JobSeekerRoute.getFullRouteWithId(JobSeekerRoute.jobSeekerProfileSettings, JobSeekerRoute.id, id));
  }

  public goToJobSeekerSavedJobs() {
    this.redirectTo(JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerSavedJobs));
  }

  public goToJobSeekerList() {
    this.redirectTo(JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerList));
  }

  // Auto apply
  public goToAutoApplyListPage() {
    this.redirectTo(AutoApplyRoute.getFullRoute(AutoApplyRoute.autoApplyListRoute));
  }

  public goToAutoApplyEditPage(id: string) {
    this.redirectTo(AutoApplyRoute.getFullRouteWithId(AutoApplyRoute.autoApplyEditRoute, AutoApplyRoute.id, id));
  }

  public goToAutoApplyCreatePage() {
    this.redirectTo(AutoApplyRoute.getFullRoute(AutoApplyRoute.autoApplyCreateRoute));
  }

  public goToAutoApplyResultPage(id: string) {
    this.redirectTo(AutoApplyRoute.getFullRouteWithId(AutoApplyRoute.autoApplyResultRoute, AutoApplyRoute.id, id));
  }

  // Company
  public goToCompanyJobEditPage(jobId: string) {
    this.redirectTo(CompanyRoute.getFullRouteWithId(CompanyRoute.companyJobEditRoute, CompanyRoute.jobId, jobId));
  }

  public goToCompanyJobListPage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyJobListRoute));
  }

  public goToCompanyDashboardPage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.dashboard));
  }

  public goToCompanyProfileEditPage(id: string) {
    this.redirectTo(CompanyRoute.getFullRouteWithId(CompanyRoute.companyProfileEditRoute, CompanyRoute.id, id));
  }

  public goToCompanyProfileViewPage(id: string) {
    this.redirectTo(CompanyRoute.getFullRouteWithId(CompanyRoute.companyProfileViewRoute, CompanyRoute.id, id));
  }

  public goToCompanyJobViewDetailsPage(id: string, isBlank?: boolean) {
    this.redirectTo(CompanyRoute.getFullRouteWithId(CompanyRoute.companyJobViewDetailsRoute, CompanyRoute.jobId, id), isBlank);
  }

  public goToCompanyListPage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyListRoute));
  }

  public goToCompanyViewListPage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyJobViewListRoute));
  }

  public goToCompanyJobCreatePage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyJobCreateRoute));
  }

  public goToInviteCompanyUserPage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyUserInviteRoute));
  }

  public goToCompanyUserListPage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyUsersListRoute));
  }

  public goToCompanyUserViewPage(userId: string, isBlank?: boolean) {
    this.redirectTo(CompanyRoute.getFullRouteWithId(CompanyRoute.companyUserViewRoute, CompanyRoute.id, userId), isBlank);
  }

  public goToCompanyUserEditPage(userId: string) {
    this.redirectTo(CompanyRoute.getFullRouteWithId(CompanyRoute.companyUserEditRoute, CompanyRoute.id, userId));
  }

  public goToJobSearchPage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyJobSearchRoute));
  }

  // CandidateRoute
  public goToViewCandidatesPage(id: string) {
    this.redirectTo(CandidateRoute.getFullRouteWithId(CandidateRoute.companyJobCandidateRoute, CandidateRoute.jobId, id));
  }

  public goToCandidatesAnswerPage(jobId: string, jobSeekerId: string) {
    this.redirectTo(CandidateRoute.getFullCandidateAnswerRoute(jobId, jobSeekerId));
  }

  public goToCandidateProfileViewPage(id: string, isBlank?: boolean) {
    this.redirectTo(JobSeekerRoute.getFullRouteWithId(JobSeekerRoute.jobSeekerAsCandidateProfilePage, JobSeekerRoute.id, id), isBlank);
  }

  // SUBSCTIPTION
  public goToTrialPage() {
    this.redirectTo(SubscriptionRoute.getFullSetTrialPackageRoute());
  }

  public goToPaymentPage() {
    this.redirectTo(SubscriptionRoute.getFullPaymentRoute());
  }

  public goToSubsctiptionManagePage() {
    this.redirectTo(SubscriptionRoute.getFullRoute(SubscriptionRoute.manage));
  }

  public goToChangeBillingDataPage() {
    this.redirectTo(SubscriptionRoute.getFullRoute(SubscriptionRoute.changeBilling));
  }

  // NOTIFICATIONS
  public goToNotificationListPage() {
    this.redirectTo(NotificationRoute.getFullRoute(NotificationRoute.notificationsList));
  }

  private redirectTo(route: string, isBlank?: boolean, queryParams?: Params) {
    this.store.dispatch(new CoreActions.RedirectTo(route, isBlank, queryParams));
  }

  // Letter Templates
  public goToLetterTemplatesListPage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyLetterTemplatesList));
  }

  public goToLetterTemplateCreatePage() {
    this.redirectTo(CompanyRoute.getFullRoute(CompanyRoute.companyLetterTemplateCreate));
  }

  public goToLetterTemplateEditPage(letterTemplateId: string) {
    this.redirectTo(CompanyRoute.getFullRouteWithId(CompanyRoute.companyLetterTemplateEdit, CompanyRoute.id, letterTemplateId));
  }

  public goToLetterTemplateViewPage(letterTemplateId: string) {
    this.redirectTo(CompanyRoute.getFullRouteWithId(CompanyRoute.companyLetterTemplateView, CompanyRoute.id, letterTemplateId));
  }
}
