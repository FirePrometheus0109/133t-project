import { BaseRoute } from './base-routes';


export class NotificationRoute extends BaseRoute {
  public static readonly rootRoute = 'notification';
  public static readonly notificationsList = `${BaseRoute.list}`;
}
