import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FullNotificationTypes } from '../../../shared/constants/full-notification-types';
import { DateTimeHelper } from '../../../shared/helpers/date-time.helper';
import { EventNotificationResponseModel } from '../../models/event-notification.model';
import { FullNotificationsService } from '../../services/full-notifications.service';


@Component({
  selector: 'app-full-notification-item',
  templateUrl: './full-notification-item.component.html',
  styleUrls: ['./full-notification-item.component.scss']
})
export class FullNotificationItemComponent implements OnInit {
  @Input() fullItem: any;
  @Output() navigateToAutoApply = new EventEmitter<number>();
  @Output() navigateToDashboard = new EventEmitter<any>();
  @Output() respondToInvitation = new EventEmitter<EventNotificationResponseModel>();

  public notificationType: string;
  public date: string;
  public messageParts: any;
  public FullNotificationTypes = FullNotificationTypes;

  ngOnInit() {
    this.date = DateTimeHelper.getDate(this.fullItem.timestamp);
    this.notificationType = FullNotificationsService.detectNotificationType(this.fullItem);
    if (this.isClickableNotification()) {
      this.messageParts = FullNotificationsService.prepareNotificationMessage(this.fullItem.data[this.notificationType].description);
    }
  }

  isClickableNotification() {
    return FullNotificationsService.isClickableNotification(this.fullItem, this.notificationType);
  }

  isEventNotification() {
    return FullNotificationsService.isEventNotification(this.fullItem);
  }
}
