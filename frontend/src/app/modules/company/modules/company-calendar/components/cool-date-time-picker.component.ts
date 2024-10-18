import { ChangeDetectionStrategy, Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MomentDateAdapter } from '@angular/material-moment-adapter';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import * as moment from 'moment-timezone';

const momentMinute: moment.unitOfTime.DurationConstructor = 'minute';
const momentDay: moment.unitOfTime.DurationConstructor = 'day';

export const CUSTOM_FORMATS = {
  parse: {
    dateInput: 'LL',
  },
  display: {
    dateInput: 'LL',
    monthYearLabel: 'MMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY',
  },
};

export enum TimePickerOptionsRange {
  start = '12:00am',
  end = '11:30pm',
  delta = 30 // in minutes
}

@Component({
  selector: 'cc-cool-datetime-picker',
  template: `
  <div fxLayoutGap="20px">
    <mat-form-field>
      <input
        matInput
        [formControl]="date"
        [matDatepicker]="datePicker"
        placeholder="Choose a date...">
      <mat-datepicker-toggle matSuffix [for]="datePicker"></mat-datepicker-toggle>
      <mat-datepicker #datePicker></mat-datepicker>
    </mat-form-field>
    <mat-form-field>
      <input
        type="text"
        spellcheck="false"
        matInput
        [formControl]="time"
        [maxlength]="timeFieldMaxLength"
        [matAutocomplete]="timeAuto"
        placeholder="Choose a time...">
      <button mat-button matSuffix mat-icon-button aria-label="Time">
        <mat-icon>access_time</mat-icon>
      </button>
    </mat-form-field>
    <mat-autocomplete #timeAuto="matAutocomplete">
      <mat-option *ngFor="let option of timeOptions" [value]="option">{{option}}</mat-option>
    </mat-autocomplete>
  </div>
  `,
  providers: [
    { provide: DateAdapter, useClass: MomentDateAdapter, deps: [MAT_DATE_LOCALE] },
    { provide: MAT_DATE_FORMATS, useValue: CUSTOM_FORMATS }
  ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CoolDateTimePickerComponent implements OnInit, OnChanges {
  // TODO: rename form controls
  readonly timeFormat = 'h:mma';
  readonly timeFieldMaxLength = 7;

  @Input() formCtrl = new FormControl();
  @Input() timezone = moment.tz.guess();
  @Input() relyInRangeOnCtrl: FormControl;
  @Input() minTimeRange = 30;

  @Output() valueChange = new EventEmitter<any>();

  date = new FormControl('', { updateOn: 'blur' });
  time = new FormControl('', {
    validators: [Validators.maxLength(this.timeFieldMaxLength)],
    updateOn: 'blur'
  });
  internalValue = this.getValidDate(moment().tz(this.timezone));

  timeOptions = this.generateTimeOptions(
    TimePickerOptionsRange.start,
    TimePickerOptionsRange.end,
    TimePickerOptionsRange.delta
  );

  ngOnInit() {
    this.setValues();
    this.time.valueChanges.subscribe(val => {
      if (this.time.valid) {
        this.setInternalTimeFromString(val);
        this.setDirtinessFrom(this.time);
      }
    });
    this.date.valueChanges.subscribe(val => {
      this.setInternalDate(val);
      this.setDirtinessFrom(this.date);
    });
    this.formCtrl.valueChanges.subscribe(val => {
      const mValue = moment(val).tz(this.timezone);
      if (mValue.isValid() && val !== this.internalValue.format()) {
        this.internalValue = this.getValidDate(mValue);
        this.setValues();
      }
    });
    if (this.relyInRangeOnCtrl) {
      this.relyInRangeOnCtrl.valueChanges.subscribe(val => {
        this.setValues();
      });
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.timezone) {
      this.internalValue.tz(changes.timezone.currentValue);
      this.setValues();
    }
  }

  private generateTimeOptions(from: string, to: string, delta: number) {
    const mValue = moment(from, this.timeFormat);
    const outputOptions = [from];
    while (this.getTimeAsString(mValue) !== to) {
      mValue.add(delta, momentMinute);
      outputOptions.push(this.getTimeAsString(mValue));
    }
    return outputOptions;
  }

  setDirtinessFrom(control: FormControl) {
    if (!this.formCtrl.dirty && control.dirty) {
      this.formCtrl.markAsDirty();
    }
  }

  getValidDate(date: moment.Moment) {
    return this.roundToNearest(date).startOf(momentMinute);
  }

  roundToNearest(date: moment.Moment) {
    const neaderestTo = 30; // minutes
    const remainder = neaderestTo - (date.minute() % neaderestTo);
    if (remainder !== neaderestTo) {
      return date.clone().add(remainder, momentMinute);
    }
    return date;
  }

  // it does not check for seconds identity!!!
  checkTimeIdentity(first, second): boolean {
    return first.hours() === second.hours()
      && first.minutes() === second.minutes();
  }

  setInternalTimeFromString(time: string) {
    const mTime = this.getValidDate(moment(time, this.timeFormat));
    // check if new time from controll is valid and check if it does not duplicate internalValue to prevent infinit loop
    if (!this.checkTimeIdentity(mTime, this.internalValue)) {
      if (mTime.isValid()) {
        this.internalValue.set({
          hour: mTime.hours(),
          minute: mTime.minutes()
        });
      }
      this.setValues();
    }
    // condition to check clear representation of time
    else if (this.getTimeAsString(this.internalValue) !== time) {
      this.setValues();
    }
  }

  checkDateIdentity(first, second): boolean {
    return first.isSame(second, momentDay);
  }

  setInternalDate(date: moment.Moment) {
    // protect from "null" values
    if (date && date.isValid()) {
      if (!this.checkDateIdentity(date, this.internalValue)) {
        this.internalValue.set({
          year: date.year(),
          month: date.month(),
          date: date.date()
        });
        this.setValues();
      }
    }
    else {
      // rollback value to previous valid
      this.setValues();
    }
  }

  getTimeAsString(date: moment.Moment): string {
    return date.clone().format(this.timeFormat);
  }

  // TODO: refactor this to add posibility to select "first or last" in range
  validateIfRange() {
    if (this.relyInRangeOnCtrl) {
      const mRelatedValue = moment(this.relyInRangeOnCtrl.value).tz(this.timezone);
      if (this.internalValue.isSameOrBefore(mRelatedValue)) {
        this.internalValue = mRelatedValue.add(this.minTimeRange, momentMinute);
        return false;
      }
    }
    return true;
  }

  setValues() {
    if (this.internalValue.isValid()) {
      this.validateIfRange();
      this.date.setValue(this.internalValue.clone().startOf(momentDay));
      this.time.setValue(this.getTimeAsString(this.internalValue));
      this.formCtrl.setValue(this.internalValue.format());
    }
  }
}
