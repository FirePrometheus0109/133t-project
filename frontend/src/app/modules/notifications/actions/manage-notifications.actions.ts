export enum ManageNotificationsActionsTypes {
  GetNotificationsTypes = '[Manage Notifications] GetNotificationsTypes',
  GetUserNotifications = '[Manage Notifications] GetUserNotifications',
  ResetState = '[Manage Notifications] ResetState',
  ChangeUserNotification = '[Manage Notifications] ChangeUserNotification',
  SaveNotificationsSettings = '[Manage Notifications] SaveNotificationsSettings',
}


export class GetNotificationsTypes {
  static readonly type = ManageNotificationsActionsTypes.GetNotificationsTypes;
}


export class GetUserNotifications {
  static readonly type = ManageNotificationsActionsTypes.GetUserNotifications;
}


export class ChangeUserNotification {
  static readonly type = ManageNotificationsActionsTypes.ChangeUserNotification;

  constructor(public notificationId: number) {
  }
}


export class ResetState {
  static readonly type = ManageNotificationsActionsTypes.ResetState;
}


export class SaveNotificationsSettings {
  static readonly type = ManageNotificationsActionsTypes.SaveNotificationsSettings;
}


export type ManageNotificationsActionsUnion =
  | SaveNotificationsSettings
  | ChangeUserNotification
  | ResetState
  | GetUserNotifications
  | GetNotificationsTypes;
