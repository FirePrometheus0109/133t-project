import {User} from '../../auth/models/user.model';
import {Job} from '../../auto-apply/models/auto-apply.model';

export enum AssignCandidateActionType {
  LoadInitialData = '[AssignCandidate Page] LoadInitialData',
  AssignCandidate = '[AssignCandidate Page] AssignCandidate',
  ResetAssignmentWindow = '[AssignCandidate Page] ResetAssignmentWindow',
}

export class LoadInitialData {
  static readonly type = AssignCandidateActionType.LoadInitialData;

  constructor() {
  }
}

export class ResetAssignmentWindow {
  static readonly type = AssignCandidateActionType.ResetAssignmentWindow;

  constructor() {
  }
}

export class AssignCandidate {
  static readonly type = AssignCandidateActionType.AssignCandidate;

  constructor(public users: Array<User>, public jobs: Array<Job>) {
  }
}

export type AssignCandidateActionsUnion =
  | LoadInitialData
  | AssignCandidate
  | ResetAssignmentWindow;
