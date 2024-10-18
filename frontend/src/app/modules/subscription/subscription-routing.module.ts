import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../auth/services/auth-guard.service';
import { SubscriptionRoute } from '../shared/constants/routes/subscription-routes';
import { ChangeBillingInformationComponent } from './containers/change-billing-information/change-billing-information.component';
import { ManageSubscriptionComponent } from './containers/manage-subscription/manage-subscription.component';
import { PaymentProcessComponent } from './containers/payment-process/payment-process.component';
import { SetTrialPlanComponent } from './containers/set-trial-plan/set-trial-plan.component';
import { ManageSubsctiptionResolver } from './resolvers/manage-subscription.resolver';
import { ViewAvailableTrialPlanListResolver } from './resolvers/set-trial-plan.resolver';
import { IsSubsctiptionPurchased } from './services/subscription-guard.sevice';

const routes: Routes = [
  {
  path: SubscriptionRoute.companyUserPaymentProcess,
  component: PaymentProcessComponent,
  canActivate: [],
},
{
  path: SubscriptionRoute.setTrialPackage,
  component: SetTrialPlanComponent,
  canActivate: [AuthGuard],
  canDeactivate: [IsSubsctiptionPurchased],
  resolve: {profileData: ViewAvailableTrialPlanListResolver},
},
{
  path: SubscriptionRoute.manageSubsctiptionRoute,
  component: ManageSubscriptionComponent,
  canActivate: [AuthGuard],
    resolve: {profileData: ManageSubsctiptionResolver},
},
{
  path: SubscriptionRoute.ChangeBillingDataRoute,
  component: ChangeBillingInformationComponent,
  canActivate: [AuthGuard],
}

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SubscriptionRoutingModule { }
