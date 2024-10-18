import { BaseRoute } from './base-routes';


export class AutoApplyRoute extends BaseRoute {
  public static readonly rootRoute = 'auto-apply';
  public static readonly autoApplyListRoute = BaseRoute.list;
  public static readonly autoApplyCreateRoute = BaseRoute.create;
  public static readonly autoApplyEditRoute = `${BaseRoute.edit}/${BaseRoute.id}`;
  public static readonly autoApplyResultRoute = `${BaseRoute.result}/${BaseRoute.id}`;
}
