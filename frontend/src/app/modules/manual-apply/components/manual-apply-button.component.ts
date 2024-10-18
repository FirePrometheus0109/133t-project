import { Component, EventEmitter, Inject, Input, OnInit, Output } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { CoreActions } from '../../core/actions';
import { JobSeekerProfilePageActions } from '../../job-seeker/actions';
import { AppMessageDialogComponent } from '../../shared/components/app-dialog-message';
import { ManageApplyRequirementsDialogComponent } from '../../shared/components/manage-apply-requirements-dialog.component';
import { JsManageCoverLettersComponent } from '../../shared/components/manage-cover-letters/js-manage-cover-letters.container';
import { StatesStatuses } from '../../shared/enums/states-statuses';
import { DateTimeHelper } from '../../shared/helpers/date-time.helper';
import { CoverLetterApplyData } from '../../shared/models/cover-letter.model';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { ManualApplyActions } from '../actions';
import { ManualApplyMessageHelper } from '../helpers/manual-apply-validation-message.helper';
import { ManualApplyState } from '../states/manual-apply-view.state';


@Component({
  selector: 'app-manual-apply-button',
  template: `
    <div *ngIf="!(isReapplyPossible$ | async)">
      <button mat-raised-button (click)="applyForJob()"
              [disabled]="!(isApplyPossible$ | async) ||  (applyResult$ | async)">
        Apply
      </button>
      <mat-error *ngIf="!(isApplyPossible$ | async)"> {{validationMessage$ | async}}</mat-error>
    </div>
    <div *ngIf="isReapplyPossible$ | async">
      <button mat-raised-button (click)="reapplyForJob()"
              [disabled]="!(isReapplyPossible$ | async) ||  (applyResult$ | async)">
        Reapply
      </button>
      <mat-error *ngIf="!(isReapplyPossible$ | async)"> {{validationMessage$ | async}}</mat-error>
    </div>
  `,
  styles: []
})
export class ManualApplyButtonComponent implements OnInit {
  @Input() jobData;
  @Output() manualApplyItem = new EventEmitter<any>();

  @Select(ManualApplyState.isApplyPossible) isApplyPossible$: Observable<boolean>;
  @Select(ManualApplyState.isReapplyPossible) isReapplyPossible$: Observable<boolean>;
  @Select(ManualApplyState.validationMessage) validationMessage$: Observable<string>;
  @Select(ManualApplyState.applyResult) applyResult$: Observable<boolean>;

  constructor(private store: Store,
              private confirmationDialogService: ConfirmationDialogService,
              @Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialog) private dialog: MatDialog) {
  }

  ngOnInit() {
    this.store.dispatch(new ManualApplyActions.ResetManualApplyState());
    this.store.dispatch(new ManualApplyActions.ChangeManualApplyPossibility(this.jobData));
    this.store.dispatch(new JobSeekerProfilePageActions.LoadCoverLetterData(this.jobSeekerId));
  }

  public reapplyForJob() {
    this.confirmationDialogService.openConfirmationDialog({
      message: `You've applied for this job on
      ${DateTimeHelper.getDate(this.jobData.applied_at)}.
      Are you sure you want to reapply?`,
      callback: this.applyForJob.bind(this),
      confirmationText: `Reapply`,
      title: `Reapply`,
      dismissible: true
    });
  }

  applyForJob() {
    if (this.jobData.is_cover_letter_required ||
      (!this.jobData.is_questionnaire_answered && this.jobData.questions.length > 0)) {
      const dialogRef = this.dialog.open(ManageApplyRequirementsDialogComponent, {
        width: '60%',
        data: {
          questions: this.jobData.questions,
          jobData: this.jobData,
          is_cover_letter_required: this.jobData.is_cover_letter_required,
          is_questionnaire_answered: this.jobData.is_questionnaire_answered
        },
      });
      dialogRef.componentInstance.manageCoverLetters.subscribe(() => {
        const dialogManageRef = this.dialog.open(JsManageCoverLettersComponent, {
          width: '40%',
          data: {
            isModal: true
          }
        });
        dialogManageRef.afterClosed().subscribe(() => {
          dialogManageRef.close();
        });
      });
      dialogRef.componentInstance.submittedResult.subscribe((result) => {
        if (result === StatesStatuses.DONE && !this.jobData.is_cover_letter_required) {
          dialogRef.close();
          this.provideApply();
        }
      });
      dialogRef.componentInstance.applyResult.subscribe((coverLetterData: CoverLetterApplyData) => {
        dialogRef.close();
        this.provideApply(coverLetterData);
      });
      dialogRef.afterClosed().subscribe(() => {
        dialogRef.componentInstance.submittedResult.unsubscribe();
        dialogRef.componentInstance.manageCoverLetters.unsubscribe();
        dialogRef.componentInstance.applyResult.unsubscribe();
        dialogRef.close();
      });
    } else {
      this.provideApply();
    }
  }

  private provideApply(coverLetterData?: CoverLetterApplyData) {
    if (this.store.selectSnapshot(ManualApplyState.isApplyPossible)) {
      this.store.dispatch(new ManualApplyActions.ManualApplyForJob(this.jobData.id, coverLetterData)).subscribe((result) => {
        this.store.dispatch(new CoreActions.LoadAppliedJobs());
        this.handleApplyResult(result);
      });
    } else if (this.store.selectSnapshot(ManualApplyState.isReapplyPossible)) {
      this.store.dispatch(new ManualApplyActions.ReapplyForJob(this.jobData.id, coverLetterData)).subscribe((result) => {
        this.handleApplyResult(result);
      });
    }
  }

  private handleApplyResult(result) {
    const errors = this.store.selectSnapshot(ManualApplyState.errors);
    if (errors) {
      this.openMessageDialog(errors.join());
    } else {
      this.openMessageDialog(ManualApplyMessageHelper.SUCCESS_MESSAGE);
      this.manualApplyItem.emit(result);
    }
  }

  private openMessageDialog(message: string) {
    this.dialog.open(AppMessageDialogComponent, {
      hasBackdrop: false,
      data: {
        message: message
      }
    });
  }

  private get jobSeekerId() {
    return this.store.selectSnapshot(AuthState.jobseekerId);
  }
}
