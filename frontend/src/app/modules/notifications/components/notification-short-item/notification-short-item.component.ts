import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { NotificationsShortModel } from '../../models/notifications-short.model';
import { ShortNotificationsService } from '../../services/short-notifications.service';


@Component({
  selector: 'app-notification-short-item',
  templateUrl: './notification-short-item.component.html',
  styleUrls: ['./notification-short-item.component.scss']
})
export class NotificationShortItemComponent implements OnInit {
  @Input() notificationItem: NotificationsShortModel;
  @Output() navigateToAutoApply = new EventEmitter<number>();
  @Output() navigateToDashboard = new EventEmitter<any>();

  public messageParts: object;

  ngOnInit() {
    this.messageParts = ShortNotificationsService.prepareNotificationMessage(this.notificationItem.description);
  }

  public get isAutoApplyNotification() {
    return ShortNotificationsService.isAutoApplyNotification(this.notificationItem);
  }

  public get isPlanWithLinkNotification() {
    return ShortNotificationsService.isPlanWithLinkNotification(this.notificationItem);
  }
}
