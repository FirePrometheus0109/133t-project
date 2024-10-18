// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { NgxsModule } from '@ngxs/store';
import { MaterialModule } from '../material';
import { NotificationsModule } from '../notifications/notifications.module';
import { SharedModule } from '../shared/shared.module';

// Components
import { CandidatesQuickListComponent } from '../candidate/containers/candidates-quick-list/candidates-quick-list.component';
import { ConfirmationDialogComponent } from '../shared/components/confirmation-dialog.component';
import { LayoutComponent } from './components/layout.component';
import { NavItemComponent } from './components/nav-item/nav-item.component';
import { ProgressSpinnerComponent } from './components/progress-spinner.component';
import { SidenavComponent } from './components/sidenav.component';
import { ToolbarComponent } from './components/toolbar.component';
import { AppComponent } from './containers/app.container';
import { HomePageComponent } from './containers/home-page.component';
import { NotFoundPageComponent } from './containers/not-found-page.component';

// Services
import { ErrorInterceptorProvider } from './services/error.interceptor';
import { LoaderInterceptorProvider } from './services/loader.interceptor';

// States
import { CoreState } from './states/core.state';
import { LayoutState } from './states/layout.states';

export const CORE_COMPONENTS = [
  AppComponent,
  NotFoundPageComponent,
  HomePageComponent,
  LayoutComponent,
  NavItemComponent,
  SidenavComponent,
  ToolbarComponent,
  ProgressSpinnerComponent,
];


@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    MaterialModule,
    FormsModule,
    SharedModule,
    NotificationsModule,
    NgxsModule.forFeature([
      CoreState,
      LayoutState,
    ]),
  ],
  declarations: CORE_COMPONENTS,
  exports: CORE_COMPONENTS,
  providers: [
    ErrorInterceptorProvider,
    LoaderInterceptorProvider,
  ],
  entryComponents: [ProgressSpinnerComponent, ConfirmationDialogComponent, CandidatesQuickListComponent],
})
export class CoreModule {
}
