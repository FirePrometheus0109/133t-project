import {BaseRoute} from './base-routes';

export class SurveyRoute extends BaseRoute {
  public static readonly rootRoute = 'survey';
  public static readonly questionListRoute = `${BaseRoute.questions}-${BaseRoute.list}`;
  public static readonly defaultQuestionsRoute = `${BaseRoute.default}-${BaseRoute.questions}`;
  public static readonly savedQuestionsRoute = `${BaseRoute.saved}-${BaseRoute.questions}`;
}
