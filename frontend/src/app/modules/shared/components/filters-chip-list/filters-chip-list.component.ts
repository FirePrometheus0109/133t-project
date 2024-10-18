import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Filter } from '../../models/filters.model';


@Component({
  selector: 'app-filters-chip-list',
  templateUrl: './filters-chip-list.component.html',
  styleUrls: ['./filters-chip-list.component.css']
})
export class FiltersChipListComponent {
  @Input() selectedFilters: Filter[];
  @Output() clearFilters = new EventEmitter<any>();
  @Output() removeFilterAction = new EventEmitter<Filter>();

  removeFilter(filter: Filter) {
    this.removeFilterAction.emit(filter);
  }
}
