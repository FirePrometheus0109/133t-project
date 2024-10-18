import { Component, EventEmitter, Input, OnDestroy, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Subject, Subscription } from 'rxjs';
import { debounceTime } from 'rxjs/internal/operators';
import { environment } from '../../../../../environments/environment';


@Component({
  selector: 'app-search-field',
  templateUrl: './search-field.component.html',
  styleUrls: ['./search-field.component.scss'],
})
export class SearchFieldComponent implements OnDestroy {

  @Input() formCtrl = new FormControl();
  @Input() placeholder: string;
  @Input() autocompleteProp = null;
  @Input() isMatAutocompleteDisabled = true;
  @Input() initialValue: any = '';
  @Input() isDisabled = false;
  @Output() searchChanged = new EventEmitter<any>();
  @Output() focused = new EventEmitter<any>();

  private debouncer = new Subject();
  private debouncerSubscription: Subscription;

  constructor() {
    this.debouncerSubscription = this.debouncer
      .pipe(debounceTime(environment.searchDebounceTime))
      .subscribe(value => this.searchChanged.emit(value));
  }

  onSearchChanged(value) {
    this.debouncer.next(value);
  }

  ngOnDestroy() {
    this.debouncerSubscription.unsubscribe();
  }

}
