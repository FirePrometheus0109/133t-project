import { BaseRoute } from './base-routes';


export class CandidateRoute extends BaseRoute {
  public static readonly rootRoute = 'candidate';
  public static readonly answer = 'answer';
  public static readonly companyJobCandidateRoute = `${BaseRoute.job}/${BaseRoute.jobId}/${BaseRoute.list}`;
  public static readonly candidateAnswersRoute = `${BaseRoute.job}/${BaseRoute.jobId}/${CandidateRoute.answer}
  /${BaseRoute.jobSeekerId}/${BaseRoute.list}`;
  public static readonly candidateList = `${BaseRoute.list}`;

  public static getFullCandidateAnswerRoute(jobId: string, jobSeekerId: string) {
    return `${this.rootRoute}/${CandidateRoute.candidateAnswersRoute}`
      .replace(this.jobId, jobId).replace(this.jobSeekerId, jobSeekerId);
  }
}
