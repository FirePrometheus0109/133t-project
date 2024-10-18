import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { concat, Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { CommentsActions, LogsActions } from '../../common-components/actions';
import { CommentType } from '../../common-components/models/comment.model';
import { LogType } from '../../common-components/models/log.model';
import { ViewJobDetailsJSPageActions } from '../actions';

import { DEFAULT_PAGINATED_OPTIONS } from '../../shared/models/paginated-data.model';


@Injectable()
export class ViewJobDetailsJsPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    const isCompanyUser = this.store.selectSnapshot(AuthState.isCompanyUser);
    const fireInitialAction = () => this.store.dispatch(new ViewJobDetailsJSPageActions.LoadJobData(route.params.jobId));
    const fireLogsInitialActions = () => concat(
      this.store.dispatch(new LogsActions.SetLogType(LogType.JobLog)),
      this.store.dispatch(new LogsActions.LoadLogsData(route.params.jobId, DEFAULT_PAGINATED_OPTIONS))
    );
    const fireCommentsInitialActions = () => concat(
      this.store.dispatch(new CommentsActions.SetCommentType(CommentType.JobComment)),
      this.store.dispatch(new CommentsActions.LoadCommentsData(route.params.jobId, DEFAULT_PAGINATED_OPTIONS)),
    );
    if (isCompanyUser) {
      return concat(
        fireInitialAction(),
        fireLogsInitialActions(),
        fireCommentsInitialActions()
      );
    }
    return fireInitialAction();
  }
}
