import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { CommentsActions, LogsActions } from '../../common-components/actions';
import { CommentType } from '../../common-components/models/comment.model';
import { LogType } from '../../common-components/models/log.model';
import { JobSeekerProfilePageActions } from '../actions';


@Injectable()
export class JobSeekerAsCandidatePageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    /* tslint:disable */
    return forkJoin(
      this.store.dispatch(new CommentsActions.SetCommentType(CommentType.JobSeekerComment)),
      this.store.dispatch(new LogsActions.SetLogType(LogType.JobSeekerLog)),
      this.store.dispatch(new JobSeekerProfilePageActions.LoadJobSeekerAsCandidate(route.params.id)),
    );
    /* tslint:enable */
  }
}
