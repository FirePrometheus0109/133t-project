import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { CommentsActions, LogsActions } from '../../common-components/actions';
import { CommentType } from '../../common-components/models/comment.model';
import { LogType } from '../../common-components/models/log.model';
import { DEFAULT_PAGINATED_OPTIONS } from '../../shared/models/paginated-data.model';
import { JobSeekerProfilePageActions } from '../actions';

export const INITIAL_TASKS_FOR_JS = [
  JobSeekerProfilePageActions.LoadInitialData,
  JobSeekerProfilePageActions.LoadEducationData,
  JobSeekerProfilePageActions.LoadCertificationData,
  JobSeekerProfilePageActions.LoadExperienceData,
  JobSeekerProfilePageActions.LoadCoverLetterData,
];


@Injectable()
export class JobSeekerProfilePageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    const tasks$ = [];
    if (this.store.selectSnapshot(AuthState.isJobSeeker)) {
      INITIAL_TASKS_FOR_JS.forEach(task => tasks$.push(this.store.dispatch(new task(route.params.id))));
      /* tslint:disable */
      return forkJoin(...tasks$);
      /* tslint:enable */
    } else {
      /* tslint:disable */
      return forkJoin(
        this.store.dispatch(new JobSeekerProfilePageActions.LoadCurrentJobSeeker(route.params.id)),
        this.store.dispatch(new CommentsActions.SetCommentType(CommentType.JobSeekerComment)),
        this.store.dispatch(new CommentsActions.LoadCommentsData(route.params.id, DEFAULT_PAGINATED_OPTIONS)),
        this.store.dispatch(new LogsActions.SetLogType(LogType.JobSeekerLog)),
        this.store.dispatch(new LogsActions.LoadLogsData(route.params.id, DEFAULT_PAGINATED_OPTIONS)),
      );
      /* tslint:enable */
    }
  }
}
