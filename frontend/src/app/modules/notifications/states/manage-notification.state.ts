import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { ManageNotificationsActions } from '../actions';
import { NotificationsTypesModel } from '../models/notifications-types.model';
import { ManageNotificationsService } from '../services/manage-notifications.service';
import { NotificationsService } from '../services/notifications.service';


class ManageNotificationsStateModel {
  status: string;
  errors: object;
  notificationsTypes: NotificationsTypesModel;
  notificationsTypeNames: string[];
  selectedUserNotificationsIds: number[];
}


export const DEFAULT_MANAGE_NOTIFICATIONS_STATE = {
  status: '',
  errors: null,
  notificationsTypes: null,
  notificationsTypeNames: [],
  selectedUserNotificationsIds: [],
};


@State<ManageNotificationsStateModel>({
  name: 'ManageNotificationsState',
  defaults: DEFAULT_MANAGE_NOTIFICATIONS_STATE,
})

export class ManageNotificationState extends BaseBlockablePageState {

  @Selector()
  static notificationsTypes(state: ManageNotificationsStateModel): NotificationsTypesModel {
    return state.notificationsTypes;
  }

  @Selector()
  static notificationsTypeNames(state: ManageNotificationsStateModel): string[] {
    return state.notificationsTypeNames;
  }

  @Selector()
  static selectedUserNotificationsIds(state: ManageNotificationsStateModel): number[] {
    return state.selectedUserNotificationsIds;
  }

  constructor(private notificationsService: NotificationsService) {
    super();
  }

  @Action(ManageNotificationsActions.GetNotificationsTypes)
  getNotificationsTypes(ctx: StateContext<ManageNotificationsStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.notificationsService.getNotificationsTypes().pipe(
      tap((result: NotificationsTypesModel) => {
        ManageNotificationsService.prepareInitialTypes(result);
        const notificationsTypeNames = ManageNotificationsService.getNotificationsTypeNames(result);
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          notificationsTypes: result,
          notificationsTypeNames
        });
        return ctx.dispatch(new ManageNotificationsActions.GetUserNotifications());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          notificationsTypes: null,
        }));
      }),
    );
  }

  @Action(ManageNotificationsActions.GetUserNotifications)
  getUserNotifications(ctx: StateContext<ManageNotificationsStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.notificationsService.getUsersNotificationsTypes().pipe(
      tap((result: NotificationsTypesModel) => {
        state = ctx.getState();
        ManageNotificationsService.setUserNotificationsTypes(state.notificationsTypes, result);
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          selectedUserNotificationsIds: ManageNotificationsService.setSelectedNotifications(state.notificationsTypes)
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(ManageNotificationsActions.ChangeUserNotification)
  changeUserNotification(ctx: StateContext<ManageNotificationsStateModel>,
                         {notificationId}: ManageNotificationsActions.ChangeUserNotification) {
    const state = ctx.getState();
    const selectedIndex = state.selectedUserNotificationsIds.findIndex(item => item === notificationId);
    (selectedIndex > -1) ? state.selectedUserNotificationsIds.splice(selectedIndex, 1) :
      state.selectedUserNotificationsIds.push(notificationId);
    ctx.setState({
      ...state,
    });
  }

  @Action(ManageNotificationsActions.SaveNotificationsSettings)
  saveNotificationsSettings(ctx: StateContext<ManageNotificationsStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.notificationsService.saveUsersNotifications(state.selectedUserNotificationsIds).pipe(
      tap(() => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error
        }));
      }),
    );
  }

  @Action(ManageNotificationsActions.ResetState)
  resetState(ctx: StateContext<ManageNotificationsStateModel>) {
    return ctx.setState({
      ...DEFAULT_MANAGE_NOTIFICATIONS_STATE,
    });
  }
}
