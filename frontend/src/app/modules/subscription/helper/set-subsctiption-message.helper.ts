import { DateTimeHelper } from '../../shared/helpers/date-time.helper';
import { SubscriptionModel } from '../models/subsctiption-plan.model';

export class SetSubscriptionMessageHelper {
  static confirmPaymentWithSavedCardMessage = 'When you confirm, payment will be made with the previously entered card';

  static successBillingInfoChange = 'You successfully changed credit card information';

  static starterPackageMessage = `You are going to choose the package with the list of limitations.
   Right after your confirmation all limitations will be applied. You will have only
   two published job postings and only  one user will have access to the web site.`;

  static alreadyPurchasedSubscription(purchasedPackage: SubscriptionModel) {
    return `You have already purchased ${purchasedPackage.plan.name} for period from
     ${DateTimeHelper.firstDayOfSubscription(purchasedPackage.date_start)}
    to ${DateTimeHelper.firstDayOfSubscription(purchasedPackage.date_end)}`;
  }
  static successRenewMessage(packageName: string) {
    return `The ${packageName} package have  successfully renewed`;
  }
  static successPurchaseMessage(packageName: string) {
    return `The ${packageName} package have  successfully purchased`;
  }
  static cheaperPurchaseMessage(currentPlan: SubscriptionModel, selectedPlanName: string) {
    return `You are going to decrease the number of job postings and profile views.
     Money will be withdrawn on ${DateTimeHelper.firstDayOfSubscription(currentPlan.date_end)}
     and the new ${selectedPlanName}
      will start from  ${DateTimeHelper.firstDayOfSubscription(currentPlan.date_end)}`;
  }
  static suceesPurchaseCheaperPackageMessage(newPlan: SubscriptionModel) {
    return `The ${newPlan.plan.name} package will start on  ${DateTimeHelper.firstDayOfSubscription(newPlan.date_end)} `;
  }

  static successUnsubscription(packageName: string) {
    return `You successfully unsubscribed from  ${packageName}'`;
  }

}
