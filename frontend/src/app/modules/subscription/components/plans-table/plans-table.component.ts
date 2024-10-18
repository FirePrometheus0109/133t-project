import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatRadioChange, MatTableDataSource } from '@angular/material';
import { SubscriptionPlan } from '../../models/subsctiption-plan.model';

@Component({
  selector: 'app-plans-table',
  templateUrl: './plans-table.component.html',
  styleUrls: ['./plans-table.component.css']
})
export class PlansTableComponent implements OnInit {

  @Input() availablePlans: Array<SubscriptionPlan>;
  @Output() changeSelectedPlan = new EventEmitter();

  displayedColumns: string[] = ['name', 'jobsCount', 'jobSeekerCount', 'price', 'checkbox'];
  dataSource;

  ngOnInit() {
    this.dataSource = new MatTableDataSource<SubscriptionPlan>(this.availablePlans);
  }

  onChangeSelectedPlan(event: MatRadioChange ) {
    this.changeSelectedPlan.emit(event.value);
  }

}
