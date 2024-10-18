export enum SetTrialPlanActionType {
  LoadAvailablePlans = '[SetTrialPlan] LoadAvailablePlans',
  PurchaseTrialPackage = '[SetTrialPlan] PurchaseTrialPackage'
}

export class LoadAvailablePlans {
  static readonly type = SetTrialPlanActionType.LoadAvailablePlans;

  constructor() {
  }
}

export class PurchaseTrialPackage {
  static readonly type = SetTrialPlanActionType.PurchaseTrialPackage;

  constructor(public id: number) {
  }
}

export type SetTrialPlanActionsUnion =
  | LoadAvailablePlans
  | PurchaseTrialPackage;
