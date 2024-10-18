import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { ViewJobPreviewComponent } from '../../company/components/view-job-preview.component';
import { CoreActions } from '../../core/actions';
import { CoreState } from '../../core/states/core.state';
import { StopJobDialogComponent } from '../../shared/components/stop-job-dialog.component';
import { InputLengths } from '../../shared/constants/validators/input-length';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { UtilsService } from '../../shared/services/utils.service';
import { AutoApplyEditActions } from '../actions';
import { AutoApplyEditState } from '../states/auto-apply-edit.state';


@Component({
  selector: 'app-auto-apply-edit-page',
  template: `
    <app-auto-apply-edit-form [form]="autoApplyEditForm"
                              [initialData]="editFormData$ | async"
                              [create_mode]="create_mode$ | async"
                              (changedSpecifyNumber)="changedSpecifyNumber($event)"
                              (changedTitle)="changedTitle($event)"
                              (submitted)="onSubmitEdit($event)">
    </app-auto-apply-edit-form>
    <div class="auto-apply-status">
      Status: {{(enums$ | async)['AutoapplyStatusEnum'][(autoApplyStatus$ | async)] || 'New'}}
    </div>
    <app-auto-apply-search-form [form]="autoApplySearchForm"
                                [initialData]="searchFormData$ | async"
                                (valueChanged)="searchValueChanged($event)">
    </app-auto-apply-search-form>
    <app-location-select-filter [form]="autoApplyLocationForm"
                                [initialData]="queryParams$ | async"
                                [filteredLocationItems]="filteredLocationItems$ | async"
                                (valueChanged)="searchLocationChanged($event)"
                                (locationSelected)="locationSelected($event)">
    </app-location-select-filter>
    <button type="button" mat-raised-button color="primary"
            *ngIf="!(create_mode$ | async)"
            [disabled]="(applied_jobs$ | async).length === 0 || checkIsAutoApplyStarted()"
            (click)="startAutoApply()">
      Start auto apply
      <mat-icon matSuffix>launch</mat-icon>
    </button>
    <div *ngIf="(autoApplyStatus$ | async)">
      <button type="button" mat-raised-button color="primary"
              (click)="copyAutoApply()">
        Copy to new auto apply
        <mat-icon matSuffix>file_copy</mat-icon>
      </button>
      <mat-icon matSuffix
                matTooltip="Create new auto apply based on the current search criteria.
You will be able to edit any of the search criteria.">
        info
      </mat-icon>
    </div>
    <div>Queue {{(autoApplyJobsCount$ | async)}}</div>
    <app-auto-apply-queue-item-preview *ngFor="let queueItem of (autoApplyJobsList$ | async)"
                                       [applied_jobs]="applied_jobs$ | async"
                                       [enums]="enums$ | async"
                                       [autoApplyQueueItem]="queueItem"
                                       [stopped_jobs]="stopped_jobs$ | async"
                                       [editMode]="true"
                                       (viewJobItem)="viewJobItemDetails($event)"
                                       (deleteJobItem)="deleteJobItem($event)"
                                       (startJobItem)="startJobItem($event)"
                                       (stopJobItem)="stopJobItem($event)">
    </app-auto-apply-queue-item-preview>
  `,
  styles: [],
})
export class AutoApplyEditComponent implements OnInit {
  @Select(CoreState.enums) enums$: Observable<object>;
  @Select(CoreState.filteredLocationItems) filteredLocationItems$: Observable<any[]>;
  @Select(AutoApplyEditState.autoApplyJobsList) autoApplyJobsList$: Observable<object>;
  @Select(AutoApplyEditState.autoApplyJobsCount) autoApplyJobsCount$: Observable<number>;
  @Select(AutoApplyEditState.autoApplyResult) autoApplyResult$: Observable<object>;
  @Select(AutoApplyEditState.editFormData) editFormData$: Observable<object>;
  @Select(AutoApplyEditState.searchFormData) searchFormData$: Observable<object>;
  @Select(AutoApplyEditState.specifyNumber) specifyNumber$: Observable<number>;
  @Select(AutoApplyEditState.selectedJobDetail) selectedJobDetail$: Observable<object>;
  @Select(AutoApplyEditState.stoppedJobs) stopped_jobs$: Observable<any>;
  @Select(AutoApplyEditState.autoApplyStatus) autoApplyStatus$: Observable<string>;
  @Select(AutoApplyEditState.appliedJobs) applied_jobs$: Observable<any>;
  @Select(AutoApplyEditState.createMode) create_mode$: Observable<any>;
  @Select(AutoApplyEditState.errors) errors$: Observable<any>;
  @Select(AutoApplyEditState.queryParams) queryParams$: Observable<any>;

  private autoApplyId: number;

  constructor(private store: Store,
              private route: ActivatedRoute,
              public dialog: MatDialog,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  autoApplySearchForm: FormGroup = new FormGroup({
    search: new FormControl('', Validators.maxLength(InputLengths.titles)),
  });

  autoApplyLocationForm = new FormGroup({
    location: new FormControl('', Validators.maxLength(InputLengths.location)),
  });

  autoApplyEditForm: FormGroup = new FormGroup({
    title: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    number: new FormControl('', Validators.required),
  });

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.autoApplyId = params.id;
    });
  }

  searchValueChanged(formData) {
    this.store.dispatch(new AutoApplyEditActions.SetQueryParams(formData));
  }

  searchLocationChanged(formData: any) {
    if (formData.location && UtilsService.isString(formData.location)) {
      forkJoin(
        this.store.dispatch(new CoreActions.GetStates({name__icontains: formData.location})),
        this.store.dispatch(new CoreActions.GetCities({name: formData.location}))
      );
    } else {
      this.store.dispatch(new AutoApplyEditActions.SetQueryParams(formData));
    }
  }

  locationSelected(data: any) {
    this.store.dispatch(new AutoApplyEditActions.SetQueryParams({location: data}));
  }

  onSubmitEdit(formData) {
    const formDataToSend = this.prepareFormData(formData);
    if (this.store.selectSnapshot(AutoApplyEditState.createMode)) {
      this.store.dispatch(new AutoApplyEditActions.CreateAutoApply(formDataToSend));
    } else {
      this.store.dispatch(new AutoApplyEditActions.UpdateAutoApply(formDataToSend, this.autoApplyId));
    }
  }

  viewJobItemDetails(data: any) {
    this.store.dispatch(new AutoApplyEditActions.GetSelectedJob(data.jobId)).subscribe((state) => {
      this.provideViewJobDetailsModal();
    });
  }

  changedSpecifyNumber(number) {
    number ? this.store.dispatch(new AutoApplyEditActions.SetSpecifyNumber(number)) :
      this.store.dispatch(new AutoApplyEditActions.SetSpecifyNumber(0));
  }

  changedTitle(title: string) {
    this.store.dispatch(new AutoApplyEditActions.SetTitle(title));
  }

  deleteJobItem(jobItemId: number) {
    this.store.dispatch(new AutoApplyEditActions.SetDeletedJobs(jobItemId));
  }

  startJobItem(jobItemId: number) {
    this.store.dispatch(new AutoApplyEditActions.ReturnJobFromStopped(jobItemId));
  }

  stopJobItem(jobItemId: number) {
    this.store.dispatch(new AutoApplyEditActions.SetStoppedJobs(jobItemId)).subscribe(() => {
      const lastAppliedJobId = [...this.store.selectSnapshot(AutoApplyEditState.appliedJobs)].pop();
      this.provideStopJobDialog(lastAppliedJobId);
    });
  }

  startAutoApply() {
    const applied_jobs = this.store.selectSnapshot(AutoApplyEditState.appliedJobs);
    const formDataToSend = this.prepareFormData(this.autoApplyEditForm.value);
    this.store.dispatch(new AutoApplyEditActions.UpdateAutoApply(formDataToSend, this.autoApplyId)).subscribe(() => {
      this.store.dispatch(new AutoApplyEditActions.StartAutoApply(this.autoApplyId, {applied_jobs}));
    });
  }

  checkIsAutoApplyStarted() {
    const enums = this.store.selectSnapshot(CoreState.enums);
    const currentAutoApplyStatus = this.store.selectSnapshot(AutoApplyEditState.autoApplyStatus);
    return enums.AutoapplyStatusEnum[currentAutoApplyStatus] === enums.AutoapplyStatusEnum.IN_PROGRESS;
  }

  copyAutoApply() {
    const currentEditFormData = this.store.selectSnapshot(AutoApplyEditState.editFormData);
    const formDataToSend = this.prepareFormData(currentEditFormData);
    this.store.dispatch(new AutoApplyEditActions.UpdateAutoApply(formDataToSend, this.autoApplyId))
      .subscribe(() => this.store.dispatch(new AutoApplyEditActions.CreateAutoApplyFromId(this.autoApplyId)));
  }

  prepareFormData(formData) {
    return Object.assign(formData, {
      query_params: this.store.selectSnapshot(AutoApplyEditState.queryParams),
      deleted_jobs: this.store.selectSnapshot(AutoApplyEditState.deletedJobs),
      stopped_jobs: this.store.selectSnapshot(AutoApplyEditState.stoppedJobs),
    });
  }

  private provideStopJobDialog(lastAppliedJobId: number) {
    const dialogRef = this.dialog.open(StopJobDialogComponent, {
      width: '60%'
    });
    dialogRef.componentInstance.showNextJob.subscribe(() => {
      this.viewJobItemDetails({jobId: lastAppliedJobId});
      dialogRef.close();
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.componentInstance.showNextJob.unsubscribe();
      dialogRef.close();
    });
  }

  private provideViewJobDetailsModal() {
    const dialogRef = this.dialog.open(ViewJobPreviewComponent, {
      width: '80%',
      data: {
        jobItem: this.store.selectSnapshot(AutoApplyEditState.selectedJobDetail),
        enums: this.store.selectSnapshot(CoreState.enums),
        skillsToMatch: this.store.selectSnapshot(AuthState.user).job_seeker.skills,
      },
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.close();
    });
  }

  canDeactivate() {
    if (this.store.selectSnapshot(AutoApplyEditState.changesOccurred)) {
      this.confirmationDialogService.openConfirmationDialog({
        message: `Do you want to close this page without saving?`,
        confirmationText: `Yes`,
        negativeText: `No`,
        dismissible: true,
      });
      return this.confirmationDialogService.modalSelection$;
    }
    return true;
  }
}
