import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ExtraJobStatus } from '../../shared/constants/extra-job-status';


@Component({
  selector: 'app-filter-job',
  template: `
    <mat-card>
      <mat-button-toggle-group>
        <mat-button-toggle (click)="removeFilter()" checked="true">All</mat-button-toggle>
        <mat-button-toggle *ngFor="let status of statuses" (click)="filterJob(status)">
          {{status | titlecase}}
        </mat-button-toggle>
        <mat-button-toggle (click)="deleteSelected()">{{deletedStatusName | titlecase}}</mat-button-toggle>
      </mat-button-toggle-group>
    </mat-card>
  `,
  styles: []
})
export class AppFilterJobComponent {
  @Input() statuses: Array<string>;
  @Output() filterJobItem = new EventEmitter<any>();
  @Output() removeFiltersItem = new EventEmitter<any>();
  @Output() filterDeletedJobs = new EventEmitter<any>();

  public deletedStatusName = ExtraJobStatus.deletedStatusName;

  public filterJob(value) {
    this.filterJobItem.emit(value);
  }

  public removeFilter() {
    this.removeFiltersItem.emit();
  }

  public deleteSelected() {
    this.filterDeletedJobs.emit({[ExtraJobStatus.deletedStatusParam]: true});
  }
}
