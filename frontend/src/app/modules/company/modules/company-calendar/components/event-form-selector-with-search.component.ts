import {
  AfterViewInit,
  Component,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  SimpleChanges,
  ViewChild
} from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatSelect } from '@angular/material';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import {
  SelectorWithSearchBaseComponent,
  ValidOption
} from './event-form-selector-with-search-base.component';


@Component({
  selector: 'ef-selector-with-search',
  template: `
  <mat-form-field>
    <mat-select
      [formControl]="formCtrl"
      [placeholder]="placeholder"
      [multiple]="multiple"
      #select>
      <mat-option>
        <ngx-mat-select-search
          [searching]="pending"
          [formControl]="optionsFilterCtrl"
          [placeholderLabel]="searchPlaceholderLabel"
          noEntriesFoundLabel="No options found..."
        >
        </ngx-mat-select-search>
      </mat-option>
      <mat-option *ngIf="unselect && !multiple" [value]="null">
        None
      </mat-option>
      <mat-option *ngFor="let option of filteredOptions | async" [value]="getValueFromKey ? option[getValueFromKey] : option">
        {{option?.title || option}}
      </mat-option>
    </mat-select>
  </mat-form-field>
  `
})
export class SelectorWithSearchComponent extends SelectorWithSearchBaseComponent implements OnInit, AfterViewInit, OnChanges, OnDestroy {

  @Input() formCtrl = new FormControl();
  @Input() options: ValidOption[];
  @Input() placeholder = 'Select value...';
  @Input() searchPlaceholderLabel = 'Find value...';
  @Input() getValueFromKey?: string;
  @Input() comparingKey;
  @Input() multiple = false;
  @Input() unselect = true;
  @Input() pending = false;

  @ViewChild('select') select: MatSelect;

  optionsFilterCtrl = new FormControl();

  filteredOptions: ReplaySubject<ValidOption[]> = new ReplaySubject<ValidOption[]>(1);

  constructor() {
    super();
  }

  ngOnInit() {
    this.filteredOptions.next(this.options);
    this.optionsFilterCtrl.valueChanges
      .pipe(
        takeUntil(this._onDestroy)
      )
      .subscribe(() => {
        this.filterOptions();
      });
  }

  ngAfterViewInit() {
    this.setInitialValue(this.filteredOptions);
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.options && !changes.pending) {
      const { currentValue } = changes.options;
      this.optionsFilterCtrl.setValue('');
      if (
           !this.formCtrl.value
        && !this.multiple
        && currentValue
        && currentValue.length === 1
      ) {
        const lastOption = currentValue[0];
        this.formCtrl.setValue(
          this.getValueFromKey
          ? lastOption[this.getValueFromKey]
          : lastOption
        );
      }
    }
  }

  filterOptions() {
    if (!this.options) {
      this.filteredOptions.next([]);
      return;
    }
    // get the search keyword
    let search = this.optionsFilterCtrl.value;
    if (!search) {
      this.filteredOptions.next(this.options.slice());
      return;
    } else {
      search = search.toLowerCase();
    }
    // filter the banks
    this.filteredOptions.next(
      this.options.filter(option => {
        const optionString = typeof option === 'string' ? option : option.title;
        if (optionString) {
          return optionString.toLowerCase().indexOf(search) > -1;
        }
        else {
          return;
        }
      })
    );
  }
}
