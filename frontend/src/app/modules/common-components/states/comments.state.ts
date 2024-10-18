import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { JobService } from '../../company/services/job.service';
import { JobSeekerService } from '../../job-seeker/services';
import { CommentsPaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { CommentsActions } from '../actions/index';
import { CommentItem, CommentModel, CommentType } from '../models/comment.model';
import { CommentsService } from '../services/comments.service';


class CommentsStateModel extends BasePaginatedPageStateModel {
  results: object[];
  editCommentMode: boolean;
  currentComment: CommentItem;
  comments: Array<CommentItem>;
  sourceId: number;
  commentType: string;
  modalMode: boolean;
  newComments: number;
}


export const DEFAULT_COMMENTS_STATE = Object.assign({
  comments: [],
  currentComment: null,
  editCommentMode: false,
  sourceId: null,
  commentType: '',
  modalMode: false,
  newComments: 0,
}, DEFAULT_PAGINATED_STATE);


@State<CommentsStateModel>({
  name: 'CommentsState',
  defaults: DEFAULT_COMMENTS_STATE,
})

export class CommentsState extends BaseBlockablePageState {
  @Selector()
  static count(state: CommentsStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: CommentsStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: CommentsStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: CommentsStateModel): Array<any> {
    return state.results;
  }

  @Selector()
  static comments(state: CommentsStateModel): Array<CommentModel> {
    return state.comments;
  }

  @Selector()
  static editCommentMode(state: CommentsStateModel): boolean {
    return state.editCommentMode;
  }

  @Selector()
  static currentComment(state: CommentsStateModel): CommentModel {
    return state.currentComment;
  }

  @Selector()
  static sourceId(state: CommentsStateModel): number {
    return state.sourceId;
  }

  @Selector()
  static commentsCount(state: CommentsStateModel): number {
    return state.comments.length;
  }

  @Selector()
  static modalMode(state: CommentsStateModel): boolean {
    return state.modalMode;
  }

  @Selector()
  static newComments(state: CommentsStateModel): number {
    return state.newComments;
  }

  constructor(private commentsService: CommentsService,
              private jobSeekerService: JobSeekerService,
              private jobService: JobService) {
    super();
  }

  @Action(CommentsActions.LoadCommentsData)
  loadCommentsData(ctx: StateContext<CommentsStateModel>, {sourceId, params}: CommentsActions.LoadCommentsData) {
    let state = ctx.getState();
    let gettingCommentsService: any;
    ctx.setState({
      ...state,
      status: 'pending',
    });
    if (state.commentType === CommentType.JobSeekerComment) {
      gettingCommentsService = this.jobSeekerService.getCommentsForJS.bind(this.jobSeekerService);
    } else if (state.commentType === CommentType.JobComment) {
      gettingCommentsService = this.jobService.getCommentsForJob.bind(this.jobService);
    }
    return gettingCommentsService(sourceId, params).pipe(
      tap((result: CommentsPaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          count: result.count,
          next: result.next,
          previous: result.previous,
          results: result.results,
          comments: result.results,
          newComments: result.new_comments,
          sourceId: sourceId,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          count: 0,
          next: null,
          previous: null,
          results: [],
        }));
      }),
    );
  }

  @Action(CommentsActions.DeleteComment)
  deleteComment(ctx: StateContext<CommentsStateModel>,
                {commentId}: CommentsActions.DeleteComment) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.commentsService.deleteComment(commentId, state.commentType).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done'
        });
        return ctx.dispatch(new CommentsActions.LoadCommentsData(state.sourceId, {
          limit: state.limit,
          offset: state.offset
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(CommentsActions.CreateNewComment)
  createNewComment(ctx: StateContext<CommentsStateModel>,
                   {commentData}: CommentsActions.CreateNewComment) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.commentsService.createNewComment(commentData, state.commentType).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done'
        });
        state = ctx.getState();
        return ctx.dispatch(new CommentsActions.LoadCommentsData(state.sourceId, {
          limit: state.limit,
          offset: state.offset
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(CommentsActions.SaveComment)
  saveComment(ctx: StateContext<CommentsStateModel>,
              {commentId, commentData}: CommentsActions.SaveComment) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.commentsService.saveComment(commentId, commentData, state.commentType).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done'
        });
        ctx.dispatch(new CommentsActions.SetEditCommentMode(false));
        ctx.dispatch(new CommentsActions.ResetCurrentComment());
        return ctx.dispatch(new CommentsActions.LoadCommentsData(state.sourceId, {
          limit: state.limit,
          offset: state.offset
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(CommentsActions.GetCurrentComment)
  getCurrentComment(ctx: StateContext<CommentsStateModel>,
                    {commentId}: CommentsActions.GetCurrentComment) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.commentsService.getCurrentComment(commentId, state.commentType).pipe(
      tap((comment: CommentItem) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          currentComment: comment
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(CommentsActions.SetEditCommentMode)
  setCommentEditMode(ctx: StateContext<CommentsStateModel>,
                     {value}: CommentsActions.SetEditCommentMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      editCommentMode: value
    });
  }

  @Action(CommentsActions.ResetCommentState)
  resetCommentState(ctx: StateContext<CommentsStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      ...DEFAULT_COMMENTS_STATE,
    });
  }

  @Action(CommentsActions.ChangePagination)
  changePagination(ctx: StateContext<CommentsStateModel>,
                   {params}: CommentsActions.ChangePagination) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      limit: params['limit'],
      offset: params['offset']
    });
    return ctx.dispatch(new CommentsActions.LoadCommentsData(state.sourceId, params));
  }

  @Action(CommentsActions.ResetCurrentComment)
  resetCurrentComment(ctx: StateContext<CommentsStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      currentComment: null
    });
  }

  @Action(CommentsActions.SetCommentType)
  setCommentType(ctx: StateContext<CommentsStateModel>,
                 {commentType}: CommentsActions.SetCommentType) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      commentType: commentType
    });
  }

  @Action(CommentsActions.SetModalMode)
  setModalMode(ctx: StateContext<CommentsStateModel>,
               {value}: CommentsActions.SetModalMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      modalMode: value
    });
  }
}
