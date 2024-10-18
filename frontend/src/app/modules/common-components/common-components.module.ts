// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { NgxsModule } from '@ngxs/store';
import { AuthModule } from '../auth/auth.module';
import { MaterialModule } from '../material';
import { NotificationsModule } from '../notifications/notifications.module';
import { SharedModule } from '../shared';

// Components
import { DeleteAccountDialogComponent } from '../shared/components/delete-account-dialog.component';
import { CommentEditFormComponent } from './components/comments/comment-edit-form.component';
import { CommentPreviewComponent } from './components/comments/comment-preview.component';
import { ViewDeletedCommentComponent } from './components/comments/view-deleted-comment/view-deleted-comment.component';
import { LogItemComponent } from './components/log-item/log-item.component';
import { SettingsComponent } from './components/settings.container';
import { CommentsComponent } from './containers/comments.container';
import { LogsComponent } from './containers/logging/logs.component';

// Service
import { CommentsService } from './services/comments.service';
import { LogsService } from './services/logs.service';

// States
import { CommentsState } from './states/comments.state';
import { LogsState } from './states/logs.state';

// TODO: this module should contains global common components for company and job seeker
export const COMMON_COMPONENTS = [
  SettingsComponent,
  CommentsComponent,
  CommentEditFormComponent,
  CommentPreviewComponent,
  LogsComponent,
  LogItemComponent,
  ViewDeletedCommentComponent
];


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MaterialModule,
    SharedModule,
    AuthModule,
    NotificationsModule,
    NgxsModule.forFeature([
      CommentsState,
      LogsState,
    ]),
  ],
  declarations: COMMON_COMPONENTS,
  exports: COMMON_COMPONENTS,
  providers: [
    CommentsService,
    LogsService
  ],
  entryComponents: [DeleteAccountDialogComponent, ViewDeletedCommentComponent]
})
export class CommonComponentsModule {
}
