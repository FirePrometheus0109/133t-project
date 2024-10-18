import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../../core/services/navigation.service';
import { NotificationsShortModel } from '../../models/notifications-short.model';
import { NotificationsShortState } from '../../states/notifications-short.state';


@Component({
  selector: 'app-notifications-short',
  templateUrl: './notifications-short.component.html',
  styleUrls: ['./notifications-short.component.scss']
})
export class NotificationsShortComponent {
  @Select(NotificationsShortState.shortNotificationList) shortNotificationList$: Observable<NotificationsShortModel[]>;
  @Select(NotificationsShortState.shortNotificationCount) shortNotificationCount$: Observable<number>;

  constructor(private navigationService: NavigationService) {
  }

  navigateToNotifications() {
    this.navigationService.goToNotificationListPage();
  }

  navigateToAutoApply(autoApplyId: number) {
    this.navigationService.goToAutoApplyResultPage(autoApplyId.toString());
  }

  navigateToDashboard() {
    this.navigationService.goToCompanyDashboardPage();
  }
}
