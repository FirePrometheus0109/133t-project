// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NgxsModule } from '@ngxs/store';
import { MaterialModule } from '../material/material.module';
import { SharedModule } from '../shared/shared.module';
import { NotificationsRoutingModule } from './notifications-routing.module';

// Components
import { EventNotificationItemComponent } from './components/event-notification-item/event-notification-item.component';
import { FullNotificationItemComponent } from './components/full-notification-item/full-notification-item.component';
import { NotificationShortItemComponent } from './components/notification-short-item/notification-short-item.component';
import {
  JobSeekerManageNotificationsComponent
} from './containers/job-seeker-manage-notifications/job-seeker-manage-notifications.component';
import { NotificationsListComponent } from './containers/notifications-list/notifications-list.component';
import { NotificationsShortComponent } from './containers/notifications-short/notifications-short.component';

// Services
import { NotificationListResolver } from './resolvers/notification-list.resolver';
import { FullNotificationsService } from './services/full-notifications.service';
import { ManageNotificationsService } from './services/manage-notifications.service';
import { NotificationsService } from './services/notifications.service';

// States
import { ManageNotificationState } from './states/manage-notification.state';
import { NotificationListState } from './states/notification-list.state';
import { NotificationsShortState } from './states/notifications-short.state';

export const NOTIFICATIONS_COMPONENTS = [
  JobSeekerManageNotificationsComponent,
  NotificationsShortComponent,
  NotificationShortItemComponent,
  NotificationsListComponent,
  FullNotificationItemComponent,
  EventNotificationItemComponent
];


@NgModule({
  imports: [
    CommonModule,
    MaterialModule,
    SharedModule,
    NotificationsRoutingModule,
    NgxsModule.forFeature([
      ManageNotificationState,
      NotificationsShortState,
      NotificationListState
    ])
  ],
  declarations: NOTIFICATIONS_COMPONENTS,
  exports: NOTIFICATIONS_COMPONENTS,
  providers: [
    NotificationsService,
    ManageNotificationsService,
    FullNotificationsService,
    NotificationListResolver
  ],
  entryComponents: [],
})
export class NotificationsModule {
}
