import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatCheckboxChange, MatRadioChange } from '@angular/material';
import { Filter, FilterData, FilterMode, FilterResult } from '../models/filters.model';
import { UtilsService } from '../services/utils.service';


@Component({
  selector: 'app-radio-filter',
  template: `
    <mat-card>
      <mat-card-title><h4>{{filterData.title}}</h4></mat-card-title>
      <mat-card-content class="filter-group">
        <div *ngIf="filterData.filterMode === radioFilterMode.SINGLE">
          <mat-radio-group>
            <mat-radio-button (change)="onFilterChange($event)" [checked]="!isFilterSelected()"> Any {{filterData.title}}</mat-radio-button>
            <div *ngIf="!isArray(filterData.filterEnum)">
              <mat-radio-button *ngFor="let item of filterData.filterEnum | keys" [value]="item" (change)="onFilterChange($event)">
                {{item.value}}
              </mat-radio-button>
            </div>
            <div *ngIf="isArray(filterData.filterEnum)">
              <mat-radio-button *ngFor="let item of filterData.filterEnum" [value]="item" (change)="onFilterChange($event)">
                {{item.name}}
              </mat-radio-button>
            </div>
          </mat-radio-group>
        </div>
        <div *ngIf="filterData.filterMode === radioFilterMode.MULTIPLE">
          <section class="checkbox-section">
            <mat-checkbox (change)="removeAllRadioFilter()" [checked]="!isFilterSelected()">Any {{filterData.title}}</mat-checkbox>
            <mat-checkbox *ngFor="let item of filterData.filterEnum | keys"
                          [checked]="isCheckBoxFilterSelected(item)" [value]="item" (change)="onMultipleFilterChange($event)">
              {{item.value}}
            </mat-checkbox>
          </section>
        </div>
      </mat-card-content>
    </mat-card>`,
  styles: [`
    .filter-group {
      display: flex;
    }

    .filter-group div {
      display: flex;
      flex-direction: column;
    }

    .filter-group div section {
      display: flex;
      flex-direction: column;
    }
  `]
})
export class RadioFilterComponent {
  @Input() filterData: FilterData;
  @Input() selectedFilters: Array<Filter> = [];
  @Output() radioFilterSelect = new EventEmitter<any>();
  @Output() radioFilterDelete = new EventEmitter<any>();

  radioFilterMode = FilterMode;

  public onFilterChange(event: MatRadioChange) {
    const filterResult = event.value && event.value.key ? event.value : new FilterResult(event.value);
    this.radioFilterSelect.emit(new Filter(this.filterData, filterResult));
  }

  public onMultipleFilterChange(event: MatCheckboxChange) {
    const filter = new Filter(this.filterData, <any>event.source.value);
    if (event.checked) {
      this.radioFilterSelect.emit(filter);
    } else {
      this.radioFilterDelete.emit(filter);
    }
  }

  isFilterSelected() {
    return this.selectedFilters.filter(item => item.data === this.filterData).length;
  }

  isCheckBoxFilterSelected(filter: FilterResult) {
    return this.selectedFilters.filter(item => item.value.key === filter.key).length;
  }

  removeAllRadioFilter() {
    this.selectedFilters.filter(item => item.data === this.filterData)
      .forEach(item => this.radioFilterDelete.emit(item));
  }

  isArray(object) {
    return UtilsService.isArray(object);
  }
}
