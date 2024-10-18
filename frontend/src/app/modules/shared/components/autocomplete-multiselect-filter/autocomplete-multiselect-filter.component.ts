import { Component, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocomplete, MatAutocompleteSelectedEvent, MatAutocompleteTrigger } from '@angular/material';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/internal/operators';
import { environment } from '../../../../../environments/environment';
import { FilterData } from '../../models/filters.model';


@Component({
  selector: 'app-autocomplete-multiselect-filter',
  templateUrl: './autocomplete-multiselect-filter.component.html',
  styleUrls: ['./autocomplete-multiselect-filter.component.css']
})
export class AutocompleteMultiselectFilterComponent {
  @Output() selectingElement = new EventEmitter<any>();
  @Output() searchElement = new EventEmitter<any>();
  @Output() clearElements = new EventEmitter<any>();
  @Input() filteredItems: Array<object>;
  @Input() filterData: FilterData;
  @Input() searchParam: string;
  @Input() placeholder: string;
  @Input() label: string;
  @ViewChild('auto') statesAutocompleteRef: MatAutocomplete;
  @ViewChild('searchInput', {read: MatAutocompleteTrigger}) searchInput: MatAutocompleteTrigger;

  outputCtrl: FormControl;
  valueCtrl: FormControl;
  filteredValues: Observable<any[]>;

  constructor() {
    this.valueCtrl = new FormControl();
    this.outputCtrl = new FormControl([]);
    this.filteredValues = this.valueCtrl.valueChanges
      .pipe(
        startWith(''),
        map(value => value ? this.filterValues(value) : this.filteredItems.slice())
      );
  }

  onSelectingItem(event: MatAutocompleteSelectedEvent) {
    const outputValues: any[] = this.outputCtrl.value;
    const index: number = outputValues.findIndex((item) => {
      return item.id === event.option.value.id;
    });
    if (index >= 0) {
      outputValues.splice(index, 1);
    } else {
      outputValues.push(event.option.value);
    }
    this.valueCtrl.setValue(this.searchParam);
    this.selectingElement.emit({
      value: event.option.value,
      isSelected: this.isValueAlreadySelected(event.option.value)
    });
    setTimeout(() => {
      this.searchInput.openPanel();
    });
  }

  onSearchChange(event) {
    this.placeholder = '';
    if (event && event.target.value.length >= environment.minimalLengthOfSearchStr) {
      this.searchElement.emit(event.target.value);
    } else {
      this.filteredItems = [];
    }
  }

  isSelected(value) {
    return this.outputCtrl.value.find((item) => {
      return item.id === value.id;
    });
  }

  displayAllSelectedItems() {
    return this.outputCtrl.value.map(item => item.name).join('; ');
  }

  filterValues(value: object) {
    return this.filteredItems.filter(item =>
      item['id'].indexOf(value) === 0);
  }

  isValueAlreadySelected(selected) {
    return !this.outputCtrl.value.some(item => item.id === selected.id);
  }
}
