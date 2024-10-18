export enum AutoApplyListActionsTypes {
  LoadAutoApplyList = '[Auto Apply List] LoadAutoApplyList',
  DeleteAutoApplyItem = '[Auto Apply List] DeleteAutoApplyItem',
}

export class LoadAutoApplyList {
  static readonly type = AutoApplyListActionsTypes.LoadAutoApplyList;
}

export class DeleteAutoApplyItem {
  static readonly type = AutoApplyListActionsTypes.DeleteAutoApplyItem;

  constructor(public autoApplyId: number) {
  }
}

export type AutoApplyListActionsUnion =
  | LoadAutoApplyList
  | DeleteAutoApplyItem;
