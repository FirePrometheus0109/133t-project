export enum NotificationsShortActionsTypes {
  GetShortNotificationList = '[Short Notifications] GetShortNotificationList',
  ResetState = '[Short Notifications] ResetState',
}


export class GetShortNotificationList {
  static readonly type = NotificationsShortActionsTypes.GetShortNotificationList;
}


export class ResetState {
  static readonly type = NotificationsShortActionsTypes.ResetState;
}


export type NotificationsShortActionsUnion =
  | ResetState
  | GetShortNotificationList;
