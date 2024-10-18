import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { environment } from '../../../../../environments/environment';
import { CoreActions } from '../../../core/actions';
import { CoreState } from '../../../core/states/core.state';
import { LocationSearchModel } from '../../models/address.model';
import { FilterData } from '../../models/filters.model';
import { BaseFormComponent } from '../base-form.component';


@Component({
  selector: 'app-search-list-form',
  templateUrl: './search-list-form.component.html',
  styleUrls: ['./search-list-form.component.scss']
})
export class SearchListFormComponent extends BaseFormComponent {
  @Select(CoreState.filteredLocation) filteredLocation$: Observable<Array<any>>;

  @Input() isGlobalSearch: boolean;
  @Input() showLocationSelection: boolean;
  @Input() locationSearchFilter: FilterData;
  @Input() placeholder = 'Skill, keyword';
  @Output() searchChanged = new EventEmitter<object>();
  @Output() selectedLocation = new EventEmitter<object>();

  locationFilterTemplate = 'locationTemplate';

  constructor(private store: Store) {
    super();
  }

  onFullTextSearchChanged(value) {
    if (!this.isGlobalSearch && (value.length >= environment.minimalLengthOfSearchStr || value.length === 0)
    ) {
      this.searchChanged.emit({search: value});
    }
  }

  onSelectLocationFilter(value: LocationSearchModel) {
    this.form.controls.location.setValue(value);
    if (!this.isGlobalSearch) {
      this.selectedLocation.emit(value);
    }
  }

  onLocationSearchChange(value) {
    this.store.dispatch(new CoreActions.LocationSearch(value));
  }
}
