import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialog, MatSelectChange, PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { CommentsActions } from '../../common-components/actions';
import { CommentsComponent } from '../../common-components/containers/comments.container';
import { CommentType } from '../../common-components/models/comment.model';
import { NavigationService } from '../../core/services/navigation.service';
import { CoreState } from '../../core/states/core.state';
import { ExtraJobStatus } from '../../shared/constants/extra-job-status';
import { CheckBoxHelper } from '../../shared/helpers/list-checkbox.helper';
import { LocationSearchModel } from '../../shared/models/address.model';
import { JobItem } from '../../shared/models/experience.model';
import { JobSortingTypes, SortingFilter, UpdateParamTypes } from '../../shared/models/filters.model';
import { DEFAULT_PAGINATED_OPTIONS } from '../../shared/models/paginated-data.model';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { LocationFilterService } from '../../shared/services/location-filter.service';
import { ViewJobListPageActions } from '../actions';
import { LocationSearchFilter } from '../models/jobs-list-filters.model';
import { ViewJobListPageState } from '../states/view-job-list-page.state';


@Component({
  selector: 'app-edit-job-list-page',
  template: `
    <mat-card>
      <mat-card-content>
        <app-score-card-stats *ngIf="!(isSubscriptionExpired$ | async)"></app-score-card-stats>
        <mat-paginator [length]="count$ | async"
                       [pageSize]="pageSize$ | async"
                       [pageSizeOptions]="pageSizeOptions$ | async"
                       (page)="onPageChanged($event)">
        </mat-paginator>
        <app-search-list-form [form]="jobSearchForm"
                              [locationSearchFilter]="locationSearchFilter"
                              [showLocationSelection]="true"
                              (searchChanged)="onFullTextSearchChanged($event)"
                              (selectedLocation)="onSelectLocationFilter($event)"
                              (submitted)="onSubmitSearch($event)">
        </app-search-list-form>
        <mat-checkbox (change)="onSelectAllJobs()"></mat-checkbox>
        <app-sorting-field [sortingFilter]="jobSortingFilters | async"
                           (sortingFilterSelect)="onSortingFilterSelect($event)">
        </app-sorting-field>
        <mat-form-field *ngIf="showAuthorFilter">
          <mat-select (selectionChange)="onAuthorFilterSelect($event)" placeholder="Author">
            <mat-option>All</mat-option>
            <mat-option *ngIf="currentUserAuthorId" [value]="currentUserAuthorId">Mine</mat-option>
            <ng-container *ngFor="let author of jobAuthors$ | async">
              <mat-option *ngIf="currentUserId !== author.user.id" [value]="author.id">
                <span>{{author.user.name}}</span>
              </mat-option>
            </ng-container>
          </mat-select>
        </mat-form-field>
      </mat-card-content>
    </mat-card>
    <mat-card>
      <mat-card-content align="end">
        <div class="job-list-actions">
          <button mat-raised-button color="primary" (click)="goToCompanyJobCreatePage()">
            Add new job
          </button>
        </div>
        <div class="job-list-actions">
          <button mat-raised-button color="primary" [disabled]="!isJobsSelected()" (click)="onDeleteSelectedJobs()">
            Delete selected
            <mat-icon matSuffix>delete</mat-icon>
          </button>
          <app-download-selected-to-csv [isDisabled]="!isJobsSelected()"
                                        (downloadToCSV)="downloadAllSelected()">
          </app-download-selected-to-csv>
        </div>
      </mat-card-content>
    </mat-card>
    <div align="center">
      <app-filter-job [statuses]="allJobStatuses$ | async"
                      (filterJobItem)="onFilterJobChanged($event)"
                      (removeFiltersItem)="onFilterJobRemoved()"
                      (filterDeletedJobs)="onFilterDeletedJob($event)">
      </app-filter-job>
    </div>

    <app-job-preview *ngFor="let jobItem of results | async"
                     [jobItem]="jobItem"
                     [statuses]="JobStatusEnum$ | async"
                     [enums]="enums$ | async"
                     [editable]="true"
                     [isCompanyUser]="isCompanyUser$ | async"
                     (editJobItem)="onEditJobItem($event)"
                     [canViewDetails]="true"
                     (goToDetails)="goToDetails($event)"
                     [checkBoxName]="checkBoxHelper.checkBoxName"
                     (deleteJobItem)="onDeleteJobItem($event)"
                     (restoreJobItem)="onRestoreJobItem($event)"
                     (commentJobItem)="onCommentJobItem($event)">
    </app-job-preview>
  `,
  styles: [],
})
export class EditJobListComponent {
  @Select(ViewJobListPageState.jobSortingFilters) jobSortingFilters: Observable<SortingFilter[]>;
  @Select(ViewJobListPageState.results) results: Observable<any>;
  @Select(ViewJobListPageState.count) count$: Observable<number>;
  @Select(ViewJobListPageState.pageSize) pageSize$: Observable<number>;
  @Select(ViewJobListPageState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;
  @Select(ViewJobListPageState.jobAuthors) jobAuthors$: Observable<Array<any>>;
  @Select(CoreState.enums) enums$: Observable<object>;
  @Select(CoreState.JobStatusEnum) JobStatusEnum$: Observable<object>;
  @Select(CoreState.allJobStatuses) allJobStatuses$: Observable<Array<string>>;
  @Select(AuthState.isCompanyUser) isCompanyUser$: Observable<boolean>;
  @Select(AuthState.isSubscriptionExpired) isSubscriptionExpired$: Observable<boolean>;

  jobSearchForm: FormGroup = new FormGroup({
    search: new FormControl(''),
    location: new FormControl(''),
  });

  checkBoxHelper = new CheckBoxHelper('job-control-checkbox');
  locationSearchFilter = LocationSearchFilter;
  private deleteJobConfirmationText = 'Are you sure you want to delete the job posting? Note that all candidates will be moved to Rejected';
  showAuthorFilter = false;
  currentUserId = this.store.selectSnapshot(AuthState.user).pk;

  constructor(private store: Store,
              private navigationService: NavigationService,
              public dialog: MatDialog,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  onSortingFilterSelect({value}: MatSelectChange) {
    if (value === JobSortingTypes.AUTHOR) {
      this.showAuthorFilter = true;
      this.store.dispatch(new ViewJobListPageActions.LoadJobsAuthorsData());
    } else {
      this.showAuthorFilter = false;
      this.store.dispatch(new ViewJobListPageActions.RemoveParams([UpdateParamTypes.OWNER]));
    }
    this.store.dispatch(new ViewJobListPageActions.UpdateParams(value, UpdateParamTypes.SORTING));
  }

  onAuthorFilterSelect({value}: MatSelectChange) {
    if (value) {
      this.store.dispatch(new ViewJobListPageActions.UpdateParams(value, UpdateParamTypes.OWNER));
    } else {
      this.store.dispatch(new ViewJobListPageActions.RemoveParams([UpdateParamTypes.OWNER]));
      this.store.dispatch(new ViewJobListPageActions.UpdateParams({}, UpdateParamTypes.COMMON));
    }
  }

  get currentUserAuthorId() {
    const currentAuthor = this.store.selectSnapshot(ViewJobListPageState.jobAuthors)
      .find(author => author.user.id === this.currentUserId);
    return currentAuthor && currentAuthor.id;
  }

  onSubmitSearch(formData: any) {
    this.store.dispatch(new ViewJobListPageActions.UpdateParams(formData, UpdateParamTypes.COMMON));
  }

  public onFullTextSearchChanged(event: any) {
    this.store.dispatch(new ViewJobListPageActions.UpdateParams(event, UpdateParamTypes.COMMON));
  }

  onSelectLocationFilter(selectedLocation: LocationSearchModel) {
    const filter = LocationFilterService.getLocationFilter(this.locationSearchFilter, selectedLocation);
    this.store.dispatch(new ViewJobListPageActions.UpdateParams({[filter.data.param]: filter.value.key}, UpdateParamTypes.COMMON));
  }

  onPageChanged(event: PageEvent) {
    this.store.dispatch(new ViewJobListPageActions.UpdateParams(event, UpdateParamTypes.PAGINATION));
  }

  onFilterJobChanged(value: string) {
    this.store.dispatch(new ViewJobListPageActions.RemoveParams([ExtraJobStatus.deletedStatusParam]));
    this.store.dispatch(new ViewJobListPageActions.UpdateParams(value, UpdateParamTypes.STATUS));
  }

  onFilterJobRemoved() {
    this.store.dispatch(new ViewJobListPageActions.RemoveParams([ExtraJobStatus.deletedStatusParam, 'status']));
    this.store.dispatch(new ViewJobListPageActions.UpdateParams({}, UpdateParamTypes.COMMON));
  }

  onFilterDeletedJob(value: object) {
    this.store.dispatch(new ViewJobListPageActions.RemoveParams(['status']));
    this.store.dispatch(new ViewJobListPageActions.UpdateParams(value, UpdateParamTypes.STATUS));
  }

  public onEditJobItem(jobItem: JobItem) {
    this.navigationService.goToCompanyJobEditPage(jobItem.id.toString());
  }

  public onDeleteJobItem(jobId: number) {
    this.confirmationDialogService.openConfirmationDialog({
      message: `${this.deleteJobConfirmationText}?`,
      callback: this.deleteJob.bind(this),
      arg: jobId,
      confirmationText: 'Delete',
    });
  }

  public onDeleteSelectedJobs() {
    const jobIds = this.getAllSelectedIds();
    this.confirmationDialogService.openConfirmationDialog({
      message: `${this.deleteJobConfirmationText}'s?`,
      callback: this.deleteSelectedJobs.bind(this),
      arg: jobIds,
      confirmationText: 'Delete',
    });
  }

  downloadAllSelected() {
    const jobIds = this.getAllSelectedIds();
    this.store.dispatch(new ViewJobListPageActions.DownloadJobList(jobIds));
  }

  public onSelectAllJobs() {
    this.checkBoxHelper.selectAllCheckboxes();
  }

  public onRestoreJobItem(jobId: number) {
    this.restoreJob(jobId);
  }

  public onCommentJobItem(jobId: number) {
    this.getCommentData(jobId).subscribe(() => {
      const dialogRef = this.dialog.open(CommentsComponent, {
        width: '60%'
      });
      dialogRef.afterClosed().subscribe(() => {
        dialogRef.close();
      });
    });
  }

  private getCommentData(jobId: number) {
    return forkJoin(
      this.store.dispatch(new CommentsActions.SetCommentType(CommentType.JobComment)),
      this.store.dispatch(new CommentsActions.SetModalMode(true)),
      this.store.dispatch(new CommentsActions.LoadCommentsData(jobId, DEFAULT_PAGINATED_OPTIONS))
    );
  }

  private restoreJob(jobId: number) {
    this.store.dispatch(new ViewJobListPageActions.RestoreJob(jobId));
  }

  private getAllSelectedIds(): number[] {
    return this.checkBoxHelper.getAllSelectedItems();
  }

  private deleteSelectedJobs(jobIds: number[]) {
    this.store.dispatch(new ViewJobListPageActions.DeleteJobList(jobIds));
  }

  private deleteJob(jobId: number) {
    this.store.dispatch(new ViewJobListPageActions.DeleteJob(jobId));
  }

  goToDetails(jobId: number) {
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }

  isJobsSelected() {
    return this.getAllSelectedIds().length > 0;
  }

  goToCompanyJobCreatePage() {
    this.navigationService.goToCompanyJobCreatePage();
  }
}
