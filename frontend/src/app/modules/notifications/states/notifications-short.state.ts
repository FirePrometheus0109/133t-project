import { Action, Selector, State, StateContext, Store } from '@ngxs/store';
import { EMPTY, of, timer } from 'rxjs';
import { switchMap } from 'rxjs/internal/operators';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { AuthState } from '../../auth/states/auth.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { NotificationsShortActions } from '../actions';
import { NotificationsShortModel } from '../models/notifications-short.model';
import { NotificationsService } from '../services/notifications.service';


class NotificationsShortStateModel {
  status: string;
  errors: object;
  shortNotificationList: NotificationsShortModel[];
}


export const DEFAULT_NOTIFICATIONS_SHORT_STATE = {
  status: '',
  errors: null,
  shortNotificationList: [],
};


@State<NotificationsShortStateModel>({
  name: 'NotificationsShortState',
  defaults: DEFAULT_NOTIFICATIONS_SHORT_STATE,
})

export class NotificationsShortState extends BaseBlockablePageState {

  @Selector()
  static shortNotificationList(state: NotificationsShortStateModel): NotificationsShortModel[] {
    return state.shortNotificationList;
  }

  @Selector()
  static shortNotificationCount(state: NotificationsShortStateModel): number {
    return state.shortNotificationList.length;
  }

  constructor(private notificationsService: NotificationsService, private store: Store) {
    super();
  }

  @Action(NotificationsShortActions.GetShortNotificationList)
  getNotificationsTypes(ctx: StateContext<NotificationsShortStateModel>,
    { }: NotificationsShortActions.GetShortNotificationList) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    // polling getting short notifications
    return timer(environment.shortNotificationsInterval.dueTime, environment.shortNotificationsInterval.period)
      .pipe(
        switchMap(() => {
          // Check for did user authorised
          const isAuthorized = this.store.selectSnapshot(AuthState.isAuthorized);

          if (isAuthorized) {
            return this.notificationsService.getShortNotificationList().pipe(
              tap((result: NotificationsShortModel[]) => {
                state = ctx.getState();
                return ctx.setState({
                  ...state,
                  status: 'done',
                  errors: null,
                  shortNotificationList: result
                });
              }),
              catchError(error => {
                state = ctx.getState();
                return of(ctx.setState({
                  ...state,
                  status: 'error',
                  errors: error.error,
                  shortNotificationList: [],
                }));
              }),
            );
          }

          return of(EMPTY);
        })
      );
  }

  @Action(NotificationsShortActions.ResetState)
  resetState(ctx: StateContext<NotificationsShortStateModel>) {
    return ctx.setState({
      ...DEFAULT_NOTIFICATIONS_SHORT_STATE,
    });
  }
}
