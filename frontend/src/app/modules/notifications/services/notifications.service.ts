import { Injectable } from '@angular/core';
import { ApiService } from '../../shared/services/api.service';


@Injectable({
  providedIn: 'root'
})
export class NotificationsService {
  route = 'notification';
  notifications = 'notifications';
  types = 'types';
  user = 'user';
  short = 'short';
  attendees = 'attendees';

  constructor(private api: ApiService) {
  }

  getNotificationsTypes() {
    return this.api.get(`${this.route}-${this.types}`);
  }

  getUsersNotificationsTypes() {
    return this.api.get(`${this.user}-${this.route}-${this.types}`);
  }

  saveUsersNotifications(userNotifications: number[]) {
    return this.api.put(`${this.user}-${this.route}-${this.types}`, {notification_types: userNotifications});
  }

  getShortNotificationList() {
    return this.api.get(`${this.notifications}/${this.short}`);
  }

  getFullNotificationList(params?: object) {
    return this.api.get(`${this.notifications}`, params);
  }

  respondToInvitation(attendeeId: number, status: string) {
    return this.api.putById(`${this.attendees}`, attendeeId, {status});
  }
}
