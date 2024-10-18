import { Injectable } from '@angular/core';
import { ClickableNotificationTypes, FullNotificationTypes } from '../../shared/constants/full-notification-types';
import { EventNotificationModel } from '../models/event-notification.model';


@Injectable({
  providedIn: 'root'
})
export class FullNotificationsService {

  public static detectNotificationType(notification: object) {
    if (notification['data'].hasOwnProperty(FullNotificationTypes.autoApply)) {
      return FullNotificationTypes.autoApply;
    } else if (notification['data'].hasOwnProperty(FullNotificationTypes.subscription)) {
      return FullNotificationTypes.subscription;
    } else if (notification['data'].hasOwnProperty(FullNotificationTypes.plan)) {
      return FullNotificationTypes.plan;
    } else if (notification['data'].hasOwnProperty(FullNotificationTypes.event)) {
      return FullNotificationTypes.event;
    }
  }

  public static isClickableNotification(notification: object, notificationType: string) {
    const description = notification['data'][notificationType].description;
    if (description) {
      const values: any[] = this.getClickableValues();
      return values.some((item) => {
        return description.includes(item);
      });
    } else {
      return false;
    }
  }

  public static isEventNotification(notification: object) {
    return notification['data'].hasOwnProperty(FullNotificationTypes.event);
  }

  public static prepareNotificationMessage(description: string) {
    const values = this.getClickableValues();
    const currentSplitter = values.find(item => description.includes(item));
    if (currentSplitter) {
      return FullNotificationsService.splitNotificationMessage(description, currentSplitter);
    }
    return null;
  }

  public static isEventActionNotification(eventNotification: EventNotificationModel) {
    return eventNotification.hasOwnProperty('attendee_id');
  }

  private static getClickableValues(): any[] {
    return Object.keys(ClickableNotificationTypes).map(key => ClickableNotificationTypes[key]);
  }

  private static splitNotificationMessage(message: string, splitter: string): object {
    const arr = message.split(splitter);
    return {
      firstPart: arr[0],
      lastPart: arr[1],
    };
  }
}
