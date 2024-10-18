import {
  AfterViewInit,
  Component,
  EventEmitter,
  Input,
  OnDestroy,
  OnInit,
  Output,
  ViewChild,
} from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatSelect } from '@angular/material';
import { Observable, Subject } from 'rxjs';
import { debounceTime, takeUntil } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

import {
  SelectorWithSearchBaseComponent,
  ValidOption
} from './event-form-selector-with-search-base.component';


@Component({
  selector: 'ef-selector-with-server-search',
  template: `
  <mat-form-field>
    <mat-select
      msInfiniteScroll
      (infiniteScroll)="getNextBatch()"
      [complete]="offset === (options | async).length"
      [formControl]="formCtrl"
      [placeholder]="placeholder"
      [multiple]="multiple"
      #select>
      <mat-option>
        <ngx-mat-select-search
          [searching]="pending"
          [formControl]="optionsFilterCtrl"
          [clearSearchInput]="false"
          [placeholderLabel]="searchPlaceholderLabel"
          noEntriesFoundLabel="No options found..."
        >
        </ngx-mat-select-search>
      </mat-option>
      <mat-optgroup *ngIf="formCtrl.value" label="Selected">
        <mat-option [value]="formCtrl.value">
          {{formCtrl.value?.title || option}}
        </mat-option>
      </mat-optgroup>
      <mat-optgroup *ngIf="(options | async)?.length" label="Options">
        <mat-option *ngIf="unselect && !multiple" [value]="null">
          None
        </mat-option>
        <mat-option *ngFor="let option of options | async" [value]="option">
          {{option?.title || option}}
        </mat-option>
      </mat-optgroup>
    </mat-select>
  </mat-form-field>
  `
})
export class SelectorWithServerSearchComponent extends SelectorWithSearchBaseComponent implements OnInit, AfterViewInit, OnDestroy {

  @Input() formCtrl = new FormControl();
  @Input() options: Observable<ValidOption[]>;
  @Input() offset: number;
  @Input() placeholder = 'Select value...';
  @Input() searchPlaceholderLabel = 'Find value...';
  @Input() comparingKey;
  @Input() multiple = false;
  @Input() unselect = true;
  @Input() pending = false;

  @Output() changeSearchString = new EventEmitter<string>();
  @Output() getNextOptions = new EventEmitter<void>();

  @ViewChild('select') select: MatSelect;

  optionsFilterCtrl = new FormControl();

  public currentlyScrolled = 0;

  protected _onGetNextBatch = new Subject<void>();

  constructor() {
    super();
  }

  ngOnInit() {
    this.optionsFilterCtrl.valueChanges
      .pipe(
        takeUntil(this._onDestroy),
        debounceTime(environment.searchDebounceTime)
      )
      .subscribe((val) => {
        this.changeSearchString.emit(val);
      });
    this._onGetNextBatch
      .pipe(
        debounceTime(environment.searchDebounceTime)
      )
      .subscribe(() => this.getNextOptions.emit());
    this.options
      .pipe(
        takeUntil(this._onDestroy)
      )
      .subscribe(() => {
        this.protectAutoScroll();
      });
  }

  ngAfterViewInit() {
    this.setInitialValue(this.options);
  }

  ngOnDestroy() {
    super.ngOnDestroy();
    this._onGetNextBatch.complete();
  }

  getNextBatch() {
    // Part of fix for ngx-mat-select-search
    const overlayDirNativeElement = this.getPanelNativeElement();
    if (overlayDirNativeElement) {
      this.currentlyScrolled = overlayDirNativeElement.scrollTop;
    }

    this._onGetNextBatch.next();
  }

  private getPanelNativeElement() {
    if (!this.select.panel) {
      return null;
    }
    return this.select.panel.nativeElement;
  }

  // Fast fix for scrolling issue in "ngx-mat-select-search"
  // Issue is created for this bug: https://github.com/bithost-gmbh/ngx-mat-select-search/issues/130
  private protectAutoScroll() {
    const overlayDirElement = this.getPanelNativeElement();
    if (overlayDirElement) {
      const conterMatSelectSearchDelay = 100;
      this.currentlyScrolled = overlayDirElement.scrollTop;
      setTimeout(
        () => overlayDirElement.scrollTop = this.currentlyScrolled,
        conterMatSelectSearchDelay
      );
    }
  }
}
