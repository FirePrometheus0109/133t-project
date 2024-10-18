import { EventNotificationResponseModel } from '../models/event-notification.model';


export enum NotificationListActionsTypes {
  GetFullNotificationList = '[Notification List] GetFullNotificationList',
  ResetState = '[Notification List] ResetState',
  RespondToInvitation = '[Notification List] RespondToInvitation',
}


export class GetFullNotificationList {
  static readonly type = NotificationListActionsTypes.GetFullNotificationList;

  constructor(public params?: object) {
  }
}


export class RespondToInvitation {
  static readonly type = NotificationListActionsTypes.RespondToInvitation;

  constructor(public responseObject: EventNotificationResponseModel) {
  }
}


export class ResetState {
  static readonly type = NotificationListActionsTypes.ResetState;
}


export type NotificationListActionsUnion =
  | RespondToInvitation
  | ResetState
  | GetFullNotificationList;
