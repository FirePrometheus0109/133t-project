export class BaseRoute {
  public static rootRoute = '';
  public static readonly public = 'public';
  public static readonly view = 'view';
  public static readonly edit = 'edit';
  public static readonly create = 'create';
  public static readonly invite = 'invite';
  public static readonly list = 'list';
  public static readonly result = 'result';
  public static readonly profile = 'profile';
  public static readonly job = 'job';
  public static readonly search = 'search';
  public static readonly viewList = 'viewList';
  public static readonly candidate = 'candidate';
  public static readonly details = 'details';
  public static readonly settings = 'settings';
  public static readonly users = 'users';
  public static readonly questions = 'questions';
  public static readonly default = 'default';
  public static readonly saved = 'saved';
  public static readonly dashboard = 'dashboard';
  // ids
  public static readonly id = ':id';
  public static readonly jobId = ':jobId';
  public static readonly token = ':token';
  public static readonly jobSeekerId = ':jobSeekerId';
  public static readonly user = ':user';
  public static readonly uid = ':uid';
  // not found
  public static readonly notFoundRoute = '404';

  public static getFullRoute(postfix: string): string {
    return `${this.rootRoute}/${postfix}`;
  }

  public static getFullRouteWithId(postfix: string, idString: string, id: string) {
    return `${this.rootRoute}/${postfix}`.replace(idString, id);
  }
}
