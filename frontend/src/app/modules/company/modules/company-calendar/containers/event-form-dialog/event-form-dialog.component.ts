import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material';
import { Actions, ofActionSuccessful, Select, Store } from '@ngxs/store';
import * as moment from 'moment-timezone';
import { Observable } from 'rxjs';

import { EventFormActions } from '../../actions';
import { ExtendedCalendarEvent } from '../../models/company-event.model';
import { companyEventFormStateFullKey, EventFormState } from '../../states/event-form-dialog.state';

import { NavigationService } from '../../../../../core/services/navigation.service';

export interface EventFormInitialData {
  forEvent: ExtendedCalendarEvent;
}

export enum SaveButtonText {
  Save = 'Send',
  SaveAnyway = 'Save anyway',
  Update = 'Send updates',
  UpdateAnyway = 'Update anyway'
}

const maxLengthArray = (max: number) => {
  return (c: AbstractControl): {[key: string]: any} => {
      if (c.value.length <= max) {
        return null;
      }
      return { 'maxLengthArray': {valid: false }};
  };
};

const shortTextMaxLength = 256;
const bigTextMaxLength = 4000;

const maxSelected = 10;

@Component({
  selector: 'cc-event-form-dialog',
  templateUrl: './event-form-dialog.component.html',
  styleUrls: ['./event-form-dialog.component.scss']
})
export class EventFormDialogComponent implements OnInit, OnDestroy {

  static defaultWidth = '80%';

  public readonly ngxsConnectFormKey = companyEventFormStateFullKey;
  public readonly minTimeRange = 30;

  @Select(EventFormState.formState) formState$: Observable<any>;
  @Select(EventFormState.eventState) eventState$: Observable<any>;
  @Select(EventFormState.eventOwner) eventOwner$: Observable<any>;
  @Select(EventFormState.eventType) eventType$: Observable<any>;
  @Select(EventFormState.colleaguesState) colleaguesState$: Observable<any>;
  @Select(EventFormState.candidatesState) candidatesState$: Observable<any>;
  @Select(EventFormState.jobsState) jobsState$: Observable<any>;
  @Select(EventFormState.zonesState) zonesState$: Observable<any>;
  @Select(EventFormState.letterTemplatesState) letterTemplatesState$: Observable<any>;
  @Select(EventFormState.countriesState) countriesState$: Observable<any>;
  @Select(EventFormState.citiesState) citiesState$: Observable<any>;
  @Select(EventFormState.citiesList) citiesList$: Observable<any>;
  @Select(EventFormState.zipsState) zipsState$: Observable<any>;

  form = this.formBuilder.group({
    type: [this.data.forEvent.type],
    time_from: [moment().format(), Validators.required],
    time_to: [moment().add(this.minTimeRange).format(), Validators.required],
    colleagues: [[], maxLengthArray(maxSelected)],
    candidates: [[], Validators.compose([Validators.required, maxLengthArray(maxSelected)])],
    job: [null, Validators.required],
    timezone: [moment.tz.guess(), Validators.required],
    location: this.formBuilder.group({
      country: [null, Validators.required],
      city: [null, Validators.required],
      zip: [null, Validators.required],
      address: ['', Validators.compose([Validators.required, Validators.maxLength(shortTextMaxLength)])]
    }),
    subject: [
      { value: '', disabled: this.isFormUpdatingEvent() },
      Validators.compose([Validators.required, Validators.maxLength(shortTextMaxLength)])
    ],
    description: ['', Validators.compose([Validators.required, Validators.maxLength(bigTextMaxLength)])]
  });

  letterTemplateCtrl = new FormControl(null);

  constructor(
    public dialogRef: MatDialogRef<any>,
    @Inject(MAT_DIALOG_DATA) public data: EventFormInitialData,
    private formBuilder: FormBuilder,
    private store: Store,
    public dialog: MatDialog,
    private actions$: Actions,
    private navigationService: NavigationService
  ) {
    this.form.controls.job.valueChanges.subscribe(val => {
      const jobId = val ? val.id : null;
      this.store.dispatch(new EventFormActions.UpdateCandidates(jobId));
    });
    this.form.controls.location['controls'].country.valueChanges.subscribe(val => {
      this.store.dispatch(new EventFormActions.UpdateCities(val));
      this.form.controls.location['controls'].city.setValue(null);
    });
    this.form.controls.location['controls'].city.valueChanges.subscribe(val => {
      this.store.dispatch(new EventFormActions.UpdateZips(val ? val.id : null));
      this.form.controls.location['controls'].zip.setValue(null);
    });
    this.letterTemplateCtrl.valueChanges.subscribe(val => {
      const template = val || {subject: '', body: ''};
      if (!val) {
        this.validateAllFormFields(this.form);
      }
      if (this.form.controls.subject.disabled) {
        this.form.patchValue({
          description: template.body
        });
      }
      else {
        this.form.patchValue({
          subject: template.subject,
          description: template.body
        });
      }
    });
  }

  ngOnInit() {
    this.store.dispatch(new EventFormActions.LoadInitData(this.data.forEvent));
    this.actions$
      .pipe(
        ofActionSuccessful(EventFormActions.CloseEventFormDialog)
      )
      .subscribe(() => this.dialogRef.close('success'));
    if (!this.isFormUpdatingEvent()) {
      this.validateAllFormFields(this.form);
    }
  }

  ngOnDestroy(): void {
    this.store.dispatch(new EventFormActions.CleenUp());
  }

  changeCitySearchString(val) {
    this.store.dispatch(new EventFormActions.ChangeCitiesSearch(val));
  }

  getNextCities() {
    this.store.dispatch(new EventFormActions.GetNextCities());
  }

  isFormUpdatingEvent() {
    return this.data.forEvent.id;
  }

  goToJobPage(jobId) {
    this.navigationService.goToCompanyJobViewDetailsPage(jobId, true);
  }

  goToCompanyUserPage(userId) {
    this.navigationService.goToCompanyUserViewPage(userId, true);
  }

  goToOwnerPage() {
    const owner = this.store.selectSnapshot(EventFormState.eventOwner);
    if (owner.company_user) {
      this.navigationService.goToCompanyUserViewPage(owner.company_user.id, true);
    }
  }

  getSaveButtonText(): SaveButtonText {
    const formState = this.store.selectSnapshot(EventFormState.formState);
    const { errors } = formState;

    if (this.isFormUpdatingEvent()) {
      if (this.getIsSubmitingForced()) {
        return SaveButtonText.UpdateAnyway;
      }
      return SaveButtonText.Update;
    }
    else {
      if (this.getIsSubmitingForced()) {
        return SaveButtonText.SaveAnyway;
      }
      else {
        return SaveButtonText.Save;
      }
    }
  }

  getIsSubmitingForced(): boolean {
    const formState = this.store.selectSnapshot(EventFormState.formState);
    const { errors } = formState;
    return !!errors.collision;
  }

  onDelete() {
    this.store.dispatch(new EventFormActions.DeleteEvent());
  }

  validateAllFormFields(formGroup: FormGroup) {
    Object.keys(formGroup.controls).forEach(field => {
      const control = formGroup.get(field);
      if (control instanceof FormControl) {
        control.markAsTouched({ onlySelf: true });
      } else if (control instanceof FormGroup) {
        this.validateAllFormFields(control);
      }
    });
  }

  onSubmit() {
    const forced = this.getIsSubmitingForced();
    this.store.dispatch(new EventFormActions.Submit(forced));
  }
}
