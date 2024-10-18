import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../core/services/navigation.service';
import { ViewJobViewerActions } from '../actions';
import { ViewJobViewerPageState } from '../states/view-job-viewers.state';


@Component({
  selector: 'app-job-viewers',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Who viewed</h4>
      </mat-card-title>
      <mat-card-content>
        <mat-paginator [length]="count$ | async"
                       [pageSize]="pageSize$ | async"
                       [pageSizeOptions]="pageSizeOptions$ | async"
                       (page)="onPageChanged($event)">
        </mat-paginator>
        <div *ngFor="let view of viewData | async">
          <span *ngIf="view.viewer"
                class="link"
                (click)="goToJobSeekerProfilePage(view.viewer.id)">
            {{view.viewer.name}}
          </span>
          <span>view on: {{view.created_at | date}} </span>
        </div>
      </mat-card-content>

      <mat-card-actions>
        <button type="button" mat-raised-button matDialogClose color="primary">
          <span>Close</span>
          <mat-icon matSuffix>close</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: []
})
export class ViewJobViewersComponent {
  @Select(ViewJobViewerPageState.results) viewData: Observable<Array<object>>;
  @Select(ViewJobViewerPageState.count) count$: Observable<number>;
  @Select(ViewJobViewerPageState.pageSize) pageSize$: Observable<number>;
  @Select(ViewJobViewerPageState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>,
              private navigationService: NavigationService,
              private store: Store) {
  }

  onPageChanged(event: PageEvent) {
    this.store.dispatch(new ViewJobViewerActions.ChangePagination(this.modalData.jobId, event));
  }

  goToJobSeekerProfilePage(id: string) {
    this.dialogRef.close();
    this.navigationService.goToJobSeekerProfileViewPage(id);
  }
}
