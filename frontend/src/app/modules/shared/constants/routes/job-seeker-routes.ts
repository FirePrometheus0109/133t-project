import { UtilsService } from '../../services/utils.service';
import { BaseRoute } from './base-routes';


export class JobSeekerRoute extends BaseRoute {
  public static readonly rootRoute = 'job-seeker';
  public static readonly jobSeekerAppliedJobs = 'applied-jobs';
  public static readonly jobSeekerSavedJobs = 'saved-jobs';
  public static readonly jobSeekerCandidate = 'candidate';
  public static readonly purchasedList = 'purchased';
  public static readonly savedList = 'saved';

  public static readonly jobSeekerPurchasedList = `${JobSeekerRoute.purchasedList}`;

  public static readonly jobSeekerSavedList = `${JobSeekerRoute.savedList}`;

  public static readonly jobSeekerList = `${BaseRoute.list}`;

  public static readonly jobSeekerProfileEditRoute = `${BaseRoute.profile}/${BaseRoute.id}/` +
    `${BaseRoute.edit}`;
  public static readonly jobSeekerProfileViewRoute = `${BaseRoute.profile}/${BaseRoute.id}/` +
    `${BaseRoute.view}`;
  public static readonly jobSeekerProfileSettings = `${BaseRoute.id}/${BaseRoute.settings}`;
  public static readonly jobSeekerAsCandidateProfilePage = `${JobSeekerRoute.jobSeekerCandidate}/${BaseRoute.profile}/${BaseRoute.id}`;
  public static readonly jobSeekerDashboardPage = `${BaseRoute.dashboard}`;
  public static readonly jobSeekerPublicProfile = `${BaseRoute.profile}/${BaseRoute.uid}/${BaseRoute.public}`;

  // outlet specific route
  public static readonly printOutletName = 'print';
  public static readonly jobSeekerPrintProfile = 'printjsp';

  public static getPublicProfileUrl(uid: string): string {
    const origin = UtilsService.nativeWindow.origin;
    const publicProfilePath = JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerPublicProfile);
    const publicProfileUrlTemplate = origin + '/#/' + publicProfilePath;
    return publicProfileUrlTemplate.replace(':uid', uid);
  }
}
