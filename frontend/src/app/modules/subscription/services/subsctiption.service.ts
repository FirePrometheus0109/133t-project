import { Injectable } from '@angular/core';
import { ApiService } from '../../shared/services/api.service';
import { PaymentData } from '../models/payment-data.model';


@Injectable({
  providedIn: 'root',
})
export class SubscriptionService {
  route = 'subscription';
  trial_plan = 'trial-plan';
  plan = 'plan';
  trial = 'trial';
  active = 'active';
  billing = 'billing-information';
  unsubscribe = 'unsubscribe';
  paymentHistory = 'payment-history';

  constructor(private api: ApiService) {
  }

  getTrialPlans() {
    return this.api.get(`${this.route}/${this.trial_plan}`);
  }

  setTrial(id: number, renew_auto?: boolean) {
    const data = {plan: id, is_auto_renew: renew_auto};
    return this.api.post(`${this.route}/${this.trial}`, data);
  }

  getActivePlan() {
    return this.api.get(`${this.route}/${this.active}`);
  }

  getAvailablePlan() {
    return this.api.get(`${this.route}/${this.plan}`);
  }

  purchaseSubscription(id: number) {
      const data = {plan: id};
      return this.api.post(`${this.route}`, data);
  }

  updateBillingData(data: PaymentData) {
    return this.api.post(`${this.route}/${this.billing}`, data);
  }

  unsubscribeSubscription(id: number) {
    return this.api.put(`${this.route}/${id}/${this.unsubscribe}`, {});
  }

  getPaymentHistory() {
    return this.api.get(`${this.route}/${this.paymentHistory}`);
  }
}
