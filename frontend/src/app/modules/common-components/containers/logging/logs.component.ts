import { Component, OnInit } from '@angular/core';
import { MatDialog, PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../../core/services/navigation.service';
import { GridViewHelper } from '../../../shared/helpers/grid-view.helper';
import { LogsActions } from '../../actions';
import { ViewDeletedCommentComponent } from '../../components/comments/view-deleted-comment/view-deleted-comment.component';
import { LogItem } from '../../models/log.model';
import { LogsState } from '../../states/logs.state';


@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.scss']
})
export class LogsComponent implements OnInit {
  @Select(LogsState.count) count$: Observable<number>;
  @Select(LogsState.pageSize) pageSize$: Observable<number>;
  @Select(LogsState.pageSizeOptions) pageSizeOptions$: Observable<number[]>;
  @Select(LogsState.logs) logs$: Observable<number[]>;

  public params = {};

  constructor(private store: Store, private dialog: MatDialog, private navigationService: NavigationService) {
  }

  ngOnInit() {
  }

  onPageChanged(event: PageEvent) {
    GridViewHelper.updatePageParams(this.params, event);
    this.store.dispatch(new LogsActions.SetCurrentPagination(this.params));
  }

  deleteLog(logId) {
    this.store.dispatch(new LogsActions.DeleteLog(logId));
  }

  viewDeletedComment(logItem: LogItem) {
    const dialogRef = this.dialog.open(ViewDeletedCommentComponent, {
      width: '60%',
      data: logItem.other_info.deleted_comment
    });
    dialogRef.componentInstance.navigateToUser.subscribe((userId) => {
      this.navigationService.goToCompanyUserViewPage(userId);
      dialogRef.close();
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.componentInstance.navigateToUser.unsubscribe();
      dialogRef.close();
    });
  }
}
