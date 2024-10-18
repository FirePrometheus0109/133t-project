import { Injectable } from '@angular/core';
import { NotificationsShortModel } from '../models/notifications-short.model';


@Injectable({
  providedIn: 'root'
})
export class ShortNotificationsService {
  private static clickableTitle = 'clickabletitle';
  private static linkToDashboard = 'linktodashboard';

  public static prepareNotificationMessage(description: string) {
    if (description.includes(ShortNotificationsService.clickableTitle)) {
      return ShortNotificationsService.splitNotificationMessage(description, ShortNotificationsService.clickableTitle);
    } else if (description.includes(ShortNotificationsService.linkToDashboard)) {
      return ShortNotificationsService.splitNotificationMessage(description, ShortNotificationsService.linkToDashboard);
    }
  }

  public static isAutoApplyNotification(notificationItem: NotificationsShortModel) {
    return notificationItem && notificationItem.data && notificationItem.data.hasOwnProperty('autoapply');
  }

  public static isSubscriptionNotification(notificationItem: NotificationsShortModel) {
    return notificationItem && notificationItem.data && notificationItem.data.hasOwnProperty('subscription');
  }

  public static isPlanWithLinkNotification(notificationItem: NotificationsShortModel) {
    return notificationItem && notificationItem.data && notificationItem.data.hasOwnProperty('plan') &&
      notificationItem.description.includes(ShortNotificationsService.linkToDashboard);
  }

  private static splitNotificationMessage(message: string, splitter: string) {
    const arr = message.split(splitter);
    return {
      firstPart: arr[0],
      lastPart: arr[1],
    };
  }
}
