import { SubscriptionModel, SubscriptionPlan } from '../models/subsctiption-plan.model';

export enum ManageSubsctiptionActionType {
  Unsubscribe = '[ManageSubsctiption] Unsubscribe',
  Cancel = '[ManageSubsctiption] Cancel',
  PaymentHistory = '[ManageSubsctiption] PaymentHistory'
}

export class Unsubscribe {
  static readonly type = ManageSubsctiptionActionType.Unsubscribe;

  constructor(public subscription: SubscriptionModel) {}
}

export class Cancel {
  static readonly type = ManageSubsctiptionActionType.Cancel;

  constructor(public subscription: SubscriptionPlan) {}

}

export class PaymentHistory {
  static readonly type = ManageSubsctiptionActionType.PaymentHistory;
}

export type ManageSubsctiptionActionsUnion =
  | Unsubscribe
  | Cancel
  | PaymentHistory;
