import { PaymentData } from '../models/payment-data.model';


export enum SetSubscriptionActionType {
  LoadCurrentPlan = '[SetSubscription] LoadCurrentPlan',
  LoadAllPlans = '[SetSubscription] LoadAllPlans',
  PurchaseSubscription = '[SetSubscription] PurchaseSubscription',
  UpvoteSubscription = '[SetSubscription] UpvoteSubscription',
  DownvoteSubscription = '[SetSubscription] DownvoteSubscription',
  UpdatePaymentData = '[SetSubscription] UpdatePaymentData',
  GoToPaymentDetails = '[SetSubscription] GoToPaymentDetails',
  CancelNextSubscription = '[SetSubscription] CancelNextSubscription',
  SetFirstPlanSelected = '[SetSubscription] SetFirstPlanSelected',
  ReturnToPlans = '[SetSubscription] ReturnToPlans',
}


export class LoadCurrentPlan {
  static readonly type = SetSubscriptionActionType.LoadCurrentPlan;

  constructor() {
  }
}


export class LoadAllPlans {
  static readonly type = SetSubscriptionActionType.LoadAllPlans;

  constructor() {
  }
}


export class CancelNextSubscription {
  static readonly type = SetSubscriptionActionType.CancelNextSubscription;

  constructor() {
  }
}


export class GoToPaymentDetails {
  static readonly type = SetSubscriptionActionType.GoToPaymentDetails;

  constructor() {
  }
}


export class DownvoteSubscription {
  static readonly type = SetSubscriptionActionType.DownvoteSubscription;

  constructor() {
  }
}


export class UpvoteSubscription {
  static readonly type = SetSubscriptionActionType.UpvoteSubscription;

  constructor() {
  }
}


export class PurchaseSubscription {
  static readonly type = SetSubscriptionActionType.PurchaseSubscription;

  constructor(public plan: number) {
  }
}


export class UpdatePaymentData {
  static readonly type = SetSubscriptionActionType.UpdatePaymentData;

  constructor(public data: PaymentData) {
  }
}


export class SetFirstPlanSelected {
  static readonly type = SetSubscriptionActionType.SetFirstPlanSelected;
}


export class ReturnToPlans {
  static readonly type = SetSubscriptionActionType.ReturnToPlans;
}

export type SetSubscriptionActionsUnion =
  | SetFirstPlanSelected
  | ReturnToPlans
  | LoadCurrentPlan
  | LoadAllPlans
  | DownvoteSubscription
  | UpvoteSubscription
  | PurchaseSubscription
  | UpdatePaymentData
  | CancelNextSubscription;
