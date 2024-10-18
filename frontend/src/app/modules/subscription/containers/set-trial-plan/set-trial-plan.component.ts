import { Component, OnInit } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from 'src/app/modules/core/services/navigation.service';
import { environment } from 'src/environments/environment.base';
import { SetTrialPlanActions } from '../../actions';
import { SubscriptionPlan } from '../../models/subsctiption-plan.model';
import { SetTrialPlanState } from '../../states/set-trial-plan.state';


@Component({
  selector: 'app-set-trial-plan',
  templateUrl: './set-trial-plan.component.html',
  styleUrls: ['./set-trial-plan.component.css']
})
export class SetTrialPlanComponent implements OnInit {
  @Select(SetTrialPlanState.availablePlans) availablePlans$: Observable<Array<SubscriptionPlan>>;
  @Select(SetTrialPlanState.trialSuccess) trialSuccess$: Observable<any>;

  trialLengthPeriod = environment.trialLengthPeriod;
  selectedPlan: SubscriptionPlan;

  constructor(private store: Store, private navigationService: NavigationService) {
  }

  ngOnInit() {
    this.selectedPlan = this.store.selectSnapshot(SetTrialPlanState.firstPlan);
    this.trialSuccess$.subscribe((result) => {
      if (result && result.id) {
        this.navigationService.goToCompanyDashboardPage();
      }
    });
  }

  onTrialPackageSubmitted() {
    this.store.dispatch(new SetTrialPlanActions.PurchaseTrialPackage(this.selectedPlan.id));
  }

  onTrialPackageSelected(plan: SubscriptionPlan) {
    this.selectedPlan = plan;
  }
}
