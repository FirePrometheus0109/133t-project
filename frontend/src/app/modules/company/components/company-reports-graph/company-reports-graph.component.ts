import { Component, OnInit } from '@angular/core';
import { MatSelectChange } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { DateTimeHelper } from 'src/app/modules/shared/helpers/date-time.helper';
import { DateBasis } from '../../../shared/enums/company-reports.enums';
import { CompanyReportsActions } from '../../actions';
import { ReportsGraphData } from '../../models/company-reports.model';
import { CompanyReportsState } from '../../states/company-reports.state';

@Component({
  selector: 'app-company-reports-graph',
  templateUrl: './company-reports-graph.component.html',
  styleUrls: ['./company-reports-graph.component.css']
})
export class CompanyReportsGraphComponent implements OnInit {
  @Select(CompanyReportsState.graphData) graphData$: Observable<Array<ReportsGraphData>>;
  @Select(CompanyReportsState.graphBasic) graphBasic$: Observable<DateBasis>;
  @Select(CompanyReportsState.fromDate) fromDate$: Observable<DateBasis>;

  dateBasis;
  selectedBasic;
  chartOptions;

  readonly chartXWidth = 1300;
  readonly chartYwidth = 400;

  constructor(private store: Store) { }

  ngOnInit() {
    this.dateBasis = DateBasis;
    this.chartOptions = {
      view: [this.chartXWidth, this.chartYwidth],
      showXAxis: true,
      showYAxis: true,
      gradient: false,
      showLegend: true,
      showXAxisLabel: true,
      showYAxisLabel: true,
      timeline: true,
      colorScheme: {
        domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
      },
    };
    this.selectedBasic =  this.store.selectSnapshot(CompanyReportsState.graphBasic);
  }

  onBasisChange(event: MatSelectChange ) {
    this.store.dispatch(new CompanyReportsActions.ChangeGraphDateBasic(event.value));
  }

  formatTimeline(val) {
    const basic = this.store.selectSnapshot(CompanyReportsState.graphBasic);
    return DateTimeHelper.formatGraphDate(val, basic);
  }

   onMoveGraphToPast() {
     this.store.dispatch(new CompanyReportsActions.MoveGraphToPast());
   }

   onMoveGraphToFuture() {
     this.store.dispatch(new CompanyReportsActions.MoveGraphToFuture());
   }

   isGraphOnCurrentState() {
     return DateTimeHelper.isDateEqual(this.store.selectSnapshot(CompanyReportsState.fromDate), new Date());
   }

}
