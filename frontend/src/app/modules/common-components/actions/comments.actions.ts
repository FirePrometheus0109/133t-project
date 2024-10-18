import {CommentModel} from '../models/comment.model';

export enum CommentsActionTypes {
  LoadCommentsData = '[Comments] LoadCommentsData',
  ChangePagination = '[Comments] ChangePagination',
  DeleteComment = '[Comments] DeleteComment',
  GetCurrentComment = '[Comments] GetCurrentComment',
  SetEditCommentMode = '[Comments] SetEditCommentMode',
  CreateNewComment = '[Comments] CreateNewComment',
  SaveComment = '[Comments] SaveComment',
  ResetCommentState = '[Comments] ResetCommentState',
  ResetCurrentComment = '[Comments] ResetCurrentComment',
  SetCommentType = '[Comments] SetCommentType',
  SetModalMode = '[Comments] SetModalMode',
}

export class LoadCommentsData {
  static readonly type = CommentsActionTypes.LoadCommentsData;

  constructor(public sourceId: number, public params?: any) {
  }
}

export class ChangePagination {
  static readonly type = CommentsActionTypes.ChangePagination;

  constructor(public params?: object, public limit?: number, public offset?: number) {
  }
}

export class DeleteComment {
  static readonly type = CommentsActionTypes.DeleteComment;

  constructor(public commentId: number) {
  }
}

export class CreateNewComment {
  static readonly type = CommentsActionTypes.CreateNewComment;

  constructor(public commentData: CommentModel) {
  }
}

export class SaveComment {
  static readonly type = CommentsActionTypes.SaveComment;

  constructor(public commentId: number, public commentData: CommentModel) {
  }
}

export class GetCurrentComment {
  static readonly type = CommentsActionTypes.GetCurrentComment;

  constructor(public commentId: number) {
  }
}

export class SetEditCommentMode {
  static readonly type = CommentsActionTypes.SetEditCommentMode;

  constructor(public value: boolean) {
  }
}

export class ResetCommentState {
  static readonly type = CommentsActionTypes.ResetCommentState;
}

export class ResetCurrentComment {
  static readonly type = CommentsActionTypes.ResetCurrentComment;
}

export class SetCommentType {
  static readonly type = CommentsActionTypes.SetCommentType;

  constructor(public commentType: string) {
  }
}

export class SetModalMode {
  static readonly type = CommentsActionTypes.SetModalMode;

  constructor(public value: boolean) {
  }
}

export type CommentsActionUnion =
  | SetModalMode
  | SetCommentType
  | ResetCurrentComment
  | ResetCommentState
  | SaveComment
  | CreateNewComment
  | SetEditCommentMode
  | GetCurrentComment
  | DeleteComment
  | ChangePagination
  | LoadCommentsData;
