export interface SubscriptionPlan {
  id: number;
  name: string;
  job_seekers_count: number;
  jobs_count: number;
  isCustom: boolean;
  price: number;
  new_price: number;
  price_apply_date: string;
}


export interface SubscriptionBalance {
  job_seekers_count: number;
  jobs_count: number;
}


export interface SubscriptionModel {
  id: number;
  plan: SubscriptionPlan;
  is_trial: boolean;
  date_start: Date;
  date_end: Date;
  is_auto_renew: boolean;
  balance: SubscriptionBalance;
  next_subscription: SubscriptionModel;
}


export interface PaymentHistoryItem {
  amount: number;
  plan: string;
  payment_date: Date;
  date_start: Date;
  date_end: Date;
  pdf_invoice_url: string;
}
