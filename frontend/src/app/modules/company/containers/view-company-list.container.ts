import { Component } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../core/services/navigation.service';
import { ViewCompanyListPageActions } from '../actions';
import { PublicCompanyItem } from '../models/public-company.model';
import { ViewCompanyListPageState } from '../states/view-company-list-page.state';


@Component({
  selector: 'app-view-company-list-page',
  template: `
    <mat-paginator [length]="count$ | async"
                   [pageSize]="pageSize$ | async"
                   [pageSizeOptions]="pageSizeOptions$ | async"
                   (page)="onPageChanged($event)">
    </mat-paginator>
    <mat-list role="list">
      <mat-list-item role="listitem" *ngFor="let company of (results$ | async); index as i;">
        <a mat-button routerLink="." (click)="goToCompany(company.id)">{{company.name}}</a>
        <a mat-button routerLink="." (click)="goToCompanyJobs(company.id)">{{company.job_count}} Jobs</a>
      </mat-list-item>
    </mat-list>
  `,
  styles: [],
})
export class ViewCompanyListPageComponent {
  @Select(ViewCompanyListPageState.count) count$: Observable<number>;
  @Select(ViewCompanyListPageState.pageSize) pageSize$: Observable<number>;
  @Select(ViewCompanyListPageState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;
  @Select(ViewCompanyListPageState.results) results$: Observable<Array<PublicCompanyItem>>;

  constructor(private store: Store,
              private navigationService: NavigationService) {
  }

  onPageChanged(event: PageEvent) {
    this.store.dispatch(new ViewCompanyListPageActions.ChangePagination(event));
  }

  goToCompany(companyId: number) {
    this.navigationService.goToCompanyProfileViewPage(companyId.toString());
  }

  goToCompanyJobs(companyId: number) {
    console.log('goToCompanyJobs', companyId);
  }
}
