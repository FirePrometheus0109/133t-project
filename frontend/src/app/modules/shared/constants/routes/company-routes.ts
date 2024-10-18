import { UtilsService } from '../../services/utils.service';
import { BaseRoute } from './base-routes';

export class CompanyRoute extends BaseRoute {
  public static readonly rootRoute = 'company';
  public static readonly reports = 'reports';
  public static readonly calendar = 'calendar';
  public static readonly letterTemplates = 'letter-templates';
  public static readonly dummyData = 'dummy-jobs';

  public static readonly companyListRoute = `${BaseRoute.list}`;
  public static readonly companyProfileViewRoute = `${BaseRoute.profile}/${BaseRoute.id}/${BaseRoute.view}`;
  public static readonly companyJobSearchRoute = `${BaseRoute.job}/${BaseRoute.search}`;
  public static readonly companyProfileEditRoute = `${BaseRoute.profile}/${BaseRoute.id}/${BaseRoute.edit}`;
  public static readonly companyJobCreateRoute = `${BaseRoute.job}/${BaseRoute.create}`;
  public static readonly companyJobViewDetailsRoute = `${BaseRoute.job}/${BaseRoute.jobId}/${BaseRoute.details}`;
  public static readonly companyJobPublicViewDetailsRoute = `${BaseRoute.job}/${BaseRoute.uid}/${BaseRoute.details}/${BaseRoute.public}`;
  public static readonly companyJobEditRoute = `${BaseRoute.job}/${BaseRoute.jobId}/${BaseRoute.edit}`;
  public static readonly companyJobViewListRoute = `${BaseRoute.job}/${BaseRoute.viewList}`;
  public static readonly companyJobListRoute = `${BaseRoute.job}/${BaseRoute.list}`;
  public static readonly companyUsersListRoute = `${BaseRoute.users}/${BaseRoute.list}`;
  public static readonly companyUserInviteRoute = `${BaseRoute.users}/${BaseRoute.invite}`;
  public static readonly companyUserViewRoute = `${BaseRoute.users}/${BaseRoute.id}/${BaseRoute.view}`;
  public static readonly companyUserEditRoute = `${BaseRoute.users}/${BaseRoute.id}/${BaseRoute.edit}`;
  public static readonly companyDummyJobsRoute = `${CompanyRoute.dummyData}`;
  // I also define route in module it self. I left it here for compability with other modules.
  // But i think that it is a miss. Module should define its routes and provide api to work with it like service.
  // TODO: make service for interacting with company-calendar routing
  public static readonly companyCalendarRoute = `${CompanyRoute.calendar}`;
  public static readonly companyDashboard = `${BaseRoute.dashboard}`;
  public static readonly companyReports = `${CompanyRoute.reports}`;
  public static readonly companyLetterTemplatesList = `${CompanyRoute.letterTemplates}/${BaseRoute.list}`;
  public static readonly companyLetterTemplateCreate = `${CompanyRoute.letterTemplates}/${BaseRoute.create}`;
  public static readonly companyLetterTemplateView = `${CompanyRoute.letterTemplates}/${BaseRoute.view}/${BaseRoute.id}`;
  public static readonly companyLetterTemplateEdit = `${CompanyRoute.letterTemplates}/${BaseRoute.edit}/${BaseRoute.id}`;

  public static getPublicJobUrl(uid: string): string {
    const origin = UtilsService.nativeWindow.origin;
    const publicJobPath = CompanyRoute.getFullRoute(CompanyRoute.companyJobPublicViewDetailsRoute);
    const publicJobUrlTemplate = origin + '/#/' + publicJobPath;
    return publicJobUrlTemplate.replace(':uid', uid);
  }
}
