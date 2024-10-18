import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../../../auth/states/auth.state';


@Component({
  selector: 'app-company-dashboard',
  templateUrl: './company-dashboard.component.html',
  styleUrls: ['./company-dashboard.component.scss']
})
export class CompanyDashboardComponent {
  @Select(AuthState.isSubscriptionExpired) isSubscriptionExpired$: Observable<boolean>;
}
