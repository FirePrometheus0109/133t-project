import { Injectable } from '@angular/core';
import { Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { AuthActions } from '../../auth/actions';
import { AuthState } from '../../auth/states/auth.state';
import { CoreActions } from '../../core/actions';
import { NotificationsShortActions } from '../../notifications/actions';

export const INITIAL_TASKS = [
  AuthActions.Initial,
  CoreActions.SetInitialSettings,
  CoreActions.SetCountries,
  CoreActions.LoadIndustryData,
  CoreActions.SetEnums
];


@Injectable({
  providedIn: 'root',
})
export class GeneralActionService {
  constructor(private store: Store) {
  }

  private getJobSeekerId(): number {
    return this.store.selectSnapshot(AuthState.jobseekerId);
  }

  private getCompanyId(): number {
    return this.store.selectSnapshot(AuthState.companyId);
  }

  private getIsAuthorized(): boolean {
    return this.store.selectSnapshot(AuthState.isAuthorized);
  }

  private isJobSeeker(): boolean {
    return this.store.selectSnapshot(AuthState.isJobSeeker);
  }

  private isCompanyUser(): boolean {
    return this.store.selectSnapshot(AuthState.isCompanyUser);
  }

  private isPurchasedJobSeekersForbidden(): boolean {
    return (this.store.selectSnapshot(AuthState.user).company.is_trial_available &&
      this.store.selectSnapshot(AuthState.isSubscriptionDeleted)) || this.store.selectSnapshot(AuthState.isSubscriptionExpired);
  }

  dispatchActionsOnInit() {
    /* tslint:disable */
    return forkJoin(...this.getTasksForAllUsers()).subscribe(() => {
      forkJoin(this.getTasksForAuthorizedUsers());
    }, () => {
    }, () => {
      forkJoin(
        ...this.getTasksForCompanyUsers(),
        ...this.getTasksForJSUsers(),
      );
    });
    /* tslint:enable */
  }

  getTasksForAllUsers(): Array<Observable<any>> {
    const tasks$ = [];
    INITIAL_TASKS.forEach(task => tasks$.push(this.store.dispatch(new task())));
    return tasks$;
  }

  getTasksForAuthorizedUsers(): Array<Observable<any>> {
    const tasks$ = [];
    const isAuthorized = this.getIsAuthorized();
    if (isAuthorized) {
      tasks$.push(this.store.dispatch(new AuthActions.ReloadUserPermissions()));
      tasks$.push(this.store.dispatch(new AuthActions.ReloadAllPermissions()));
      tasks$.push(this.store.dispatch(new NotificationsShortActions.GetShortNotificationList()));
    }
    return tasks$;
  }

  getTasksForCompanyUsers(): Array<Observable<any>> {
    const tasks$ = [];
    const isCompanyUser = this.isCompanyUser();
    if (isCompanyUser) {
      const companyId = this.getCompanyId();
      if (companyId) {
        tasks$.push(this.store.dispatch(new CoreActions.GetCandidateStatuses()));
        if (!this.isPurchasedJobSeekersForbidden()) {
          tasks$.push(this.store.dispatch(new CoreActions.LoadPurchasedJobSeekers()));
        }
      }
    }
    return tasks$;
  }

  getTasksForJSUsers(): Array<Observable<any>> {
    const tasks$ = [];
    const isJobSeeker = this.isJobSeeker();
    if (isJobSeeker) {
      const jobseekerId = this.getJobSeekerId();
      if (jobseekerId) {
        tasks$.push(this.store.dispatch(new CoreActions.ListFavoriteJobs(jobseekerId)));
        tasks$.push(this.store.dispatch(new CoreActions.LoadAppliedJobs()));
      }
    }
    return tasks$;
  }
}
