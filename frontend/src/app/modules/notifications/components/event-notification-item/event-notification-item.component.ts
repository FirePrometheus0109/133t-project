import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Select } from '@ngxs/store';
import * as moment from 'moment';
import { Observable } from 'rxjs';
import { AuthState } from '../../../auth/states/auth.state';
import {
  EventNotificationModel,
  EventNotificationResponseModel,
  EventNotificationStatus
} from '../../models/event-notification.model';
import { EventResponseStatusEnum } from '../../models/event-response-status.enum';
import { FullNotificationsService } from '../../services/full-notifications.service';
import { NotificationListState } from '../../states/notification-list.state';


@Component({
  selector: 'app-event-notification-item',
  templateUrl: './event-notification-item.component.html',
  styleUrls: ['./event-notification-item.component.scss']
})
export class EventNotificationItemComponent {
  @Select(AuthState.isCompanyUser) isCompanyUser$: Observable<boolean>;
  @Select(NotificationListState.isPending) pending$: Observable<boolean>;

  @Input() eventNotification: EventNotificationModel;
  @Output() respondToInvitation = new EventEmitter<EventNotificationResponseModel>();

  EventResponseStatusEnum = EventResponseStatusEnum;

  provideAnswer(status: string) {
    this.respondToInvitation.emit({
      id: this.eventNotification.attendee_id,
      status: status
    });
  }

  isActionNotification() {
    return FullNotificationsService.isEventActionNotification(this.eventNotification);
  }

  areActionsEnabled() {
    return this.eventNotification.status !== EventNotificationStatus.REJECTED
      && this.eventNotification.status !== EventNotificationStatus.ACCEPTED
      && !this.eventNotification.cancelled;
  }

  get timeInformation() {
    return `${moment(this.eventNotification.time_from).format('LT')} - ${moment(this.eventNotification.time_to).format('LT')}`;
  }
}
