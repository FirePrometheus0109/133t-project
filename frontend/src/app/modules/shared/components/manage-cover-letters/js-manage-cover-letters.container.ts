import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { environment } from '../../../../../environments/environment';
import { AuthState } from '../../../auth/states/auth.state';
import { CoreState } from '../../../core/states/core.state';
import { JobSeekerProfilePageActions } from '../../../job-seeker/actions';
import { JSPPageState } from '../../../job-seeker/states/jsp-page.state';
import { Enums } from '../../../shared/models/enums.model';
import { InputLengths } from '../../constants/validators/input-length';
import { CoverLetterItem, CoverLetterMode } from '../../models/cover-letter.model';


@Component({
  selector: 'app-js-manage-cover-letters',
  template: `
    <mat-dialog-content>
      <ng-template [ngxPermissionsOnly]="['add_coverletter']">
        <button type="button" mat-raised-button color="primary"
                *ngIf="(coverLetterMode$ | async) === CoverLetterMode.VIEW"
                [disabled]="(coverLetter$ | async).length === environment.maxCoverLettersCount"
                (click)="addNewCoverLetter()">
          Add new Cover letter
          <mat-icon matSuffix>add</mat-icon>
        </button>
      </ng-template>
      <ng-template [ngxPermissionsOnly]="['add_coverletter', 'change_coverletter']">
        <app-jsp-cover-letter-form
            (submitted)="onSubmitCoverLetter($event)"
            (closeForm)="closeCoverLetterForm()"
            *ngIf="(coverLetterMode$ | async) !== CoverLetterMode.VIEW"
            [defaultCoverLetter]="defaultCoverLetter$ | async"
            [errors]="errors$ | async"
            [form]="coverLetterForm">
        </app-jsp-cover-letter-form>
      </ng-template>
      <ng-template [ngxPermissionsOnly]="['view_coverletter']">
        <app-jsp-cover-letter-list [initialData]="coverLetter$ | async"
                                   (editCoverLetterItem)="onEditCoverLetter($event)"
                                   (deletedCoverLetterItem)="deleteCoverLetterItem($event)">
        </app-jsp-cover-letter-list>
      </ng-template>
    </mat-dialog-content>
    <mat-dialog-actions *ngIf="modalData && modalData.isModal">
      <button type="button" mat-raised-button matDialogClose color="primary">
        <span>Cancel</span>
        <mat-icon matSuffix>close</mat-icon>
      </button>
    </mat-dialog-actions>
  `,
  styles: [],
})
export class JsManageCoverLettersComponent implements OnInit {
  @Select(JSPPageState.pending) pending$: Observable<boolean>;
  @Select(JSPPageState.errors) errors$: Observable<any>;
  @Select(JSPPageState.coverLetter) coverLetter$: Observable<Array<CoverLetterItem>>;
  @Select(JSPPageState.coverLetterMode) coverLetterMode$: Observable<string>;
  @Select(JSPPageState.defaultCoverLetter) defaultCoverLetter$: Observable<any>;
  @Select(CoreState.enums) enums$: Observable<Enums>;

  public environment = environment;
  public CoverLetterMode = CoverLetterMode;
  private jsId: number;

  public coverLetterForm: FormGroup = new FormGroup({
    title: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    body: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.descriptions)])),
    is_default: new FormControl(false),
  });

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogManageRef: MatDialogRef<any>,
              private store: Store) {
  }

  ngOnInit() {
    this.jsId = this.store.selectSnapshot(AuthState.jobseekerId);
  }

  public addNewCoverLetter() {
    this.resetCoverLetterForm();
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateCoverLetterMode(this.CoverLetterMode.NEW),
    );
  }

  public onSubmitCoverLetter(formData: CoverLetterItem) {
    if (this.store.snapshot().JSPPage.coverLetterMode === this.CoverLetterMode.NEW) {
      this.store.dispatch(
        new JobSeekerProfilePageActions.CreateNewCoverLetter(this.jsId, formData),
      );
    }
    if (this.store.snapshot().JSPPage.coverLetterMode === this.CoverLetterMode.EDIT) {
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateCoverLetter(this.jsId, formData.id, formData),
      );
    }
  }

  public onEditCoverLetter(formData: CoverLetterItem) {
    this.resetCoverLetterForm();
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateCoverLetterMode(this.CoverLetterMode.EDIT),
    );
    this.coverLetterForm.patchValue(formData);
    this.coverLetterForm.addControl('id', new FormControl(formData.id));
  }

  public deleteCoverLetterItem(letterId: number) {
    this.store.dispatch(new JobSeekerProfilePageActions.DeleteCoverLetter(this.jsId, letterId));
  }

  public closeCoverLetterForm() {
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateCoverLetterMode(this.CoverLetterMode.VIEW),
    );
  }

  private resetCoverLetterForm() {
    this.coverLetterForm.reset();
    this.coverLetterForm.patchValue({is_default: false});
  }
}
