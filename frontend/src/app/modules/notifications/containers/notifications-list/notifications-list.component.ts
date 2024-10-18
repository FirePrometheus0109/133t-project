import { Component } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../../core/services/navigation.service';
import { GridViewHelper } from '../../../shared/helpers/grid-view.helper';
import { NotificationListActions } from '../../actions';
import { EventNotificationResponseModel } from '../../models/event-notification.model';
import { NotificationListState } from '../../states/notification-list.state';


@Component({
  selector: 'app-notifications-list',
  templateUrl: './notifications-list.component.html',
  styleUrls: ['./notifications-list.component.scss']
})
export class NotificationsListComponent {
  @Select(NotificationListState.count) count$: Observable<number>;
  @Select(NotificationListState.pageSize) pageSize$: Observable<number>;
  @Select(NotificationListState.pageSizeOptions) pageSizeOptions$: Observable<number[]>;
  @Select(NotificationListState.fullNotificationList) fullNotificationList$: Observable<any[]>;

  private params = {};

  constructor(private store: Store, private navigationService: NavigationService) {
  }

  onPageChanged(event: PageEvent) {
    GridViewHelper.updatePageParams(this.params, event);
    this.store.dispatch(new NotificationListActions.GetFullNotificationList(this.params));
  }

  navigateToAutoApply(autoApplyId: number) {
    this.navigationService.goToAutoApplyResultPage(autoApplyId.toString());
  }

  navigateToDashboard() {
    this.navigationService.goToCompanyDashboardPage();
  }

  respondToInvitation(responseObject: EventNotificationResponseModel) {
    this.store.dispatch(new NotificationListActions.RespondToInvitation(responseObject));
  }
}
