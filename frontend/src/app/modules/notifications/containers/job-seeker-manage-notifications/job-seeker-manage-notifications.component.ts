import { Component, OnDestroy } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { ManageNotificationsActions } from '../../actions';
import { NotificationsTypesModel } from '../../models/notifications-types.model';
import { ManageNotificationState } from '../../states/manage-notification.state';


@Component({
  selector: 'app-job-seeker-manage-notifications',
  templateUrl: './job-seeker-manage-notifications.component.html',
  styleUrls: ['./job-seeker-manage-notifications.component.scss']
})
export class JobSeekerManageNotificationsComponent implements OnDestroy {
  @Select(ManageNotificationState.notificationsTypes) notificationsTypes$: Observable<NotificationsTypesModel>;
  @Select(ManageNotificationState.notificationsTypeNames) notificationsTypeNames$: Observable<string[]>;

  constructor(private store: Store) {
  }

  ngOnDestroy() {
    this.store.dispatch(new ManageNotificationsActions.ResetState());
  }

  changeNotification(notificationId: number) {
    this.store.dispatch(new ManageNotificationsActions.ChangeUserNotification(notificationId));
  }

  saveNotificationsSettings() {
    this.store.dispatch(new ManageNotificationsActions.SaveNotificationsSettings());
  }
}
