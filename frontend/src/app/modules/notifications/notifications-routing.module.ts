import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../auth/services/auth-guard.service';
import { NotificationRoute } from '../shared/constants/routes/notifications-routes';
import { NotificationsListComponent } from './containers/notifications-list/notifications-list.component';
import { NotificationListResolver } from './resolvers/notification-list.resolver';

const routes: Routes = [
  {
    path: NotificationRoute.notificationsList,
    component: NotificationsListComponent,
    canActivate: [AuthGuard],
    resolve: {profileData: NotificationListResolver},
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NotificationsRoutingModule {
}
