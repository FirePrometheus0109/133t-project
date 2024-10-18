import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Store} from '@ngxs/store';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {AuthState} from '../../auth/states/auth.state';
import {CoreActions} from '../../core/actions';
import {CoreState} from '../../core/states/core.state';

@Component({
  selector: 'app-job-favorite-toggle',
  template: `
    <button mat-icon-button color="accent" (click)="toggleJobFavorite()"
            [matTooltip]="(jobInFavorites$ | async)? 'Remove from favorites': 'Add to favorites'">
      <mat-icon *ngIf="!(jobInFavorites$ | async)">star_border</mat-icon>
      <mat-icon *ngIf="(jobInFavorites$ | async)">star</mat-icon>
    </button>
  `,
  styles: [],
})
export class JobFavoriteToggleComponent implements OnInit {
  @Input() jobId: number = null;
  @Output() toggleChange = new EventEmitter<boolean>();

  jobInFavorites$: Observable<boolean>;

  constructor(private store: Store) {
  }

  ngOnInit() {
    this.jobInFavorites$ = this.store.select(CoreState.jobInFavorites).pipe(
      map(filterFn => filterFn(this.jobId)),
    );
  }

  toggleJobFavorite(): void {
    const jobseekerId = this.store.selectSnapshot(AuthState.jobseekerId);
    const jobInFavorites = this.store.selectSnapshot(CoreState.jobInFavorites)(this.jobId);
    if (jobInFavorites) {
      this.store.dispatch(new CoreActions.DeleteJobFromFavorites(jobseekerId, this.jobId)).subscribe(
        () => this.toggleChange.emit(false));
    } else {
      this.store.dispatch(new CoreActions.SaveJobToFavorites(jobseekerId, this.jobId)).subscribe(
        () => this.toggleChange.emit(true));
    }
  }
}
