import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { NotificationListActions } from '../actions';
import { NotificationsService } from '../services/notifications.service';


class NotificationListStateModel extends BasePaginatedPageStateModel {
  errors: object;
  notificationList: any[];
}


export const DEFAULT_NOTIFICATION_LIST_STATE = Object.assign({
  errors: null,
  notificationList: [],
}, DEFAULT_PAGINATED_STATE);


@State<NotificationListStateModel>({
  name: 'NotificationListState',
  defaults: DEFAULT_NOTIFICATION_LIST_STATE,
})

export class NotificationListState {

  @Selector()
  static fullNotificationList(state: NotificationListStateModel): any[] {
    return state.notificationList;
  }

  @Selector()
  static count(state: NotificationListStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: NotificationListStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: NotificationListStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static isPending(state: NotificationListStateModel): boolean {
    return state.status === 'pending';
  }

  constructor(private notificationsService: NotificationsService) {
  }

  @Action(NotificationListActions.GetFullNotificationList)
  getNotificationsTypes(ctx: StateContext<NotificationListStateModel>,
                        {params}: NotificationListActions.GetFullNotificationList) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.notificationsService.getFullNotificationList(params).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          notificationList: result.results,
          count: result.count
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          notificationList: [],
        }));
      }),
    );
  }

  @Action(NotificationListActions.RespondToInvitation)
  respondToInvitation(ctx: StateContext<NotificationListStateModel>,
                      {responseObject}: NotificationListActions.RespondToInvitation) {
    ctx.patchState({
      status: 'pending',
    });
    return this.notificationsService.respondToInvitation(responseObject.id, responseObject.status).pipe(
      tap(() => {
        ctx.patchState({
          status: 'done',
          errors: null
        });
        return ctx.dispatch(new NotificationListActions.GetFullNotificationList());
      }),
      catchError(error => {
        return of(ctx.patchState({
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(NotificationListActions.ResetState)
  resetState(ctx: StateContext<NotificationListStateModel>) {
    return ctx.setState({
      ...DEFAULT_NOTIFICATION_LIST_STATE,
    });
  }
}
