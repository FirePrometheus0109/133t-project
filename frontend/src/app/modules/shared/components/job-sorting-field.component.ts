import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatAutocompleteSelectedEvent } from '@angular/material';
import { SortingFilter } from '../models/filters.model';


@Component({
  selector: 'app-sorting-field',
  template: `
    <mat-form-field>
      <mat-select (selectionChange)="onSortingChange($event)" placeholder="Sort">
        <mat-option *ngFor="let filter of sortingFilter" [value]="filter.value">
          {{filter.viewValue}}
        </mat-option>
      </mat-select>
    </mat-form-field>
  `,
  styles: []
})
export class SortingFieldComponent {
  @Input() sortingFilter: SortingFilter[];
  @Output() sortingFilterSelect = new EventEmitter<any>();

  public onSortingChange(event: MatAutocompleteSelectedEvent) {
    this.sortingFilterSelect.emit(event);
  }
}
