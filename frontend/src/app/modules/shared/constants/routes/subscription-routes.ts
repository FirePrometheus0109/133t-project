import { BaseRoute } from './base-routes';

export class SubscriptionRoute extends BaseRoute {
  public static readonly rootRoute = 'subscription';
  public static readonly payment = 'payment';
  public static readonly trial = 'set-trial';
  public static readonly manage = 'manage';
  public static readonly changeBilling = 'change-billing';

  public static readonly companyUserPaymentProcess = `${SubscriptionRoute.payment}`;
  public static readonly setTrialPackage = `${SubscriptionRoute.trial}`;
  public static readonly manageSubsctiptionRoute = `${SubscriptionRoute.manage}`;
  public static readonly ChangeBillingDataRoute = `${SubscriptionRoute.changeBilling}`;


  public static getFullSetTrialPackageRoute() {
    return `${this.rootRoute}/${SubscriptionRoute.setTrialPackage}`;
  }

  public static getFullPaymentRoute() {
    return `${this.rootRoute}/${SubscriptionRoute.companyUserPaymentProcess}`;
  }
}
