import { Component, OnInit } from '@angular/core';
import { MatSelectChange } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { SortingFilter } from 'src/app/modules/shared/models/filters.model';
import { CompanyReportsActions } from '../../actions';
import { ActivityStats } from '../../models/company-reports.model';
import { CompanyReportsState } from '../../states/company-reports.state';

@Component({
  selector: 'app-workflow-stats-widget',
  templateUrl: './workflow-stats-widget.component.html',
  styleUrls: ['./workflow-stats-widget.component.css']
})
export class WorkflowStatsWidgetComponent implements OnInit {
  @Select(CompanyReportsState.workflowStatsData) data$: Observable<Array<ActivityStats>>;
  @Select(CompanyReportsState.workflowStatsFilter) filter$: Observable<SortingFilter>;
  @Select(CompanyReportsState.workflowFilter) filterData$: Observable<Array<SortingFilter>>;

  selectedFilter;
  constructor(private store: Store) { }

  ngOnInit() {
    this.selectedFilter = this.store.selectSnapshot(CompanyReportsState.workflowStatsFilter);
  }

  onFilterChanges(event: MatSelectChange ) {
    this.store.dispatch(new CompanyReportsActions.ChangeWorkflowFilter(event.value));
  }

   compareFn(v1: SortingFilter, v2: SortingFilter): boolean {
    return v1 && v2 ? v1.value === v2.value : v1 === v2;
  }
}
