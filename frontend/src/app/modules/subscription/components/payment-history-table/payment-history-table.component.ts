import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatSort, MatTableDataSource } from '@angular/material';
import { PaymentHistoryItem } from '../../models/subsctiption-plan.model';

@Component({
  selector: 'app-payment-history-table',
  templateUrl: './payment-history-table.component.html',
  styleUrls: ['./payment-history-table.component.css']
})
export class PaymentHistoryTableComponent implements OnInit {
  @Input() paymentHistory: Array<PaymentHistoryItem>;
  @ViewChild(MatSort) sort: MatSort;

  displayedColumns = ['name', 'amount', 'date', 'circle', 'pdf'];

  dataSource;
  constructor() { }

  ngOnInit() {
    this.dataSource = new MatTableDataSource(this.paymentHistory);
    this.dataSource.sort = this.sort;
  }

}
