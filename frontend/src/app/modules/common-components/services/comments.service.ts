import {Injectable} from '@angular/core';
import {ApiService} from '../../shared/services/api.service';
import {CommentModel, CommentType} from '../models/comment.model';

@Injectable()
export class CommentsService {
  private jobSeekerComment = 'job-seeker-comment';
  private jobComment = 'job-comment';

  constructor(private api: ApiService) {
  }

  public createNewComment(commentData: CommentModel, commentType: string) {
    return this.api.post(`${this.setCommentRoute(commentType)}`, commentData);
  }

  public getCurrentComment(commentId: number, commentType: string) {
    return this.api.getById(`${this.setCommentRoute(commentType)}`, commentId);
  }

  public saveComment(commentId: number, commentData: CommentModel, commentType: string) {
    return this.api.putById(`${this.setCommentRoute(commentType)}`, commentId, commentData);
  }

  public deleteComment(commentId: number, commentType: string) {
    return this.api.deleteById(`${this.setCommentRoute(commentType)}`, commentId);
  }

  private setCommentRoute(commentType: string) {
    if (commentType === CommentType.JobSeekerComment) {
      return this.jobSeekerComment;
    } else if (commentType === CommentType.JobComment) {
      return this.jobComment;
    }
  }
}
