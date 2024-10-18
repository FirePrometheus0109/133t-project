import { Component, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { MatAutocompleteSelectedEvent } from '@angular/material';
import { Store } from '@ngxs/store';
import { FilterData } from '../../models/filters.model';
import { SearchFieldComponent } from '../search-field/search-field.component';


@Component({
  selector: 'app-autocomplete-filter',
  templateUrl: './autocomplete-filter.component.html',
  styleUrls: ['./autocomplete-filter.component.css']
})
export class AutocompleteFilterComponent {
  @Output() selectingElement = new EventEmitter<any>();
  @Output() searchElement = new EventEmitter<any>();
  @Input() filteredItems: Array<object>;
  @Input() filterData: FilterData;
  @Input() templateName: string;
  @Input() showLocationSelection: boolean;

  @ViewChild(SearchFieldComponent) searchFieldComponent: SearchFieldComponent;

  constructor(public store: Store) {
  }

  focusFunction(): void {
    this.onSearchChange('');
  }

  onSelectingItem(event: MatAutocompleteSelectedEvent) {
    this.selectingElement.emit(event.option.value);

    if (!this.showLocationSelection) {
      this.searchFieldComponent.formCtrl.setValue('');
    }
    this.searchFieldComponent.formCtrl.markAsUntouched();
  }

  onSearchChange(value: string) {
    this.searchElement.emit(value);
  }

  displayFn(item: any) {
    return (item) ? item.name : '';
  }

  get isSearchEmpty() {
    return !this.searchFieldComponent.formCtrl.value;
  }
}
