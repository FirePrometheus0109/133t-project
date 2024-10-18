import { Injectable } from '@angular/core';
import { NotificationsTypesModel, NotificationTypeItemModel } from '../models/notifications-types.model';


@Injectable({
  providedIn: 'root'
})
export class ManageNotificationsService {

  public static prepareInitialTypes(initialTypes: NotificationsTypesModel) {
    return Object.values(initialTypes).forEach((type: NotificationTypeItemModel[]) => {
      type.map((typeItem: NotificationTypeItemModel) => {
        typeItem.checked = false;
      });
    });
  }

  public static getNotificationsTypeNames(initialTypes: NotificationsTypesModel) {
    const notificationsTypeNames = [];
    Object.values(initialTypes).forEach((type: NotificationTypeItemModel[]) => {
      type.forEach((typeItem: NotificationTypeItemModel) => {
        typeItem.checked = false;
        if (!notificationsTypeNames.includes(typeItem.name)) {
          notificationsTypeNames.push(typeItem.name);
        }
      });
    });
    return notificationsTypeNames;
  }

  public static setUserNotificationsTypes(initialTypes: NotificationsTypesModel, userTypes: NotificationsTypesModel) {
    return Object.values(initialTypes).forEach((type: NotificationTypeItemModel[]) => {
      type.map((typeItem: NotificationTypeItemModel) => {
        Object.values(userTypes).forEach((userType: NotificationTypeItemModel[]) => {
          userType.forEach((userTypeItem: NotificationTypeItemModel) => {
            if (typeItem.id === userTypeItem.id) {
              typeItem.checked = true;
            }
          });
        });
      });
    });
  }

  public static setSelectedNotifications(notificationsTypes: NotificationsTypesModel) {
    const selectedIds = [];
    Object.values(notificationsTypes).forEach((type: NotificationTypeItemModel[]) => {
      type.forEach((typeItem: NotificationTypeItemModel) => {
        if (typeItem.checked) {
          selectedIds.push(typeItem.id);
        }
      });
    });
    return selectedIds;
  }
}
