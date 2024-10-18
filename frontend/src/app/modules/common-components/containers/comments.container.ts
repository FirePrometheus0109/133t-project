import { Component, OnDestroy } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs/index';
import { environment } from '../../../../environments/environment';
import { CommentsActions } from '../actions/index';
import { CommentItem, CommentModel } from '../models/comment.model';
import { CommentsState } from '../states/comments.state';


@Component({
  selector: 'app-comments',
  template: `
    <mat-card>
      <mat-card-content>
        <mat-dialog-content>
          <div class="comment-container">
            <ng-template [ngxPermissionsOnly]="['add_jobcomment', 'change_jobcomment', 'add_jobseekercomment', 'change_jobseekercomment']">
              <div class="comment-edit">
                <app-comment-edit-form [form]="commentForm"
                                       [initialData]="currentComment$ | async"
                                       [editCommentMode]="editCommentMode$ | async"
                                       [errors]="errors$ | async"
                                       (submitted)="submitForm($event)"
                                       (closeForm)="closeEditForm()">
                </app-comment-edit-form>
              </div>
            </ng-template>
            <div class="comments-list">
              <mat-paginator [length]="count$ | async"
                             [pageSize]="pageSize$ | async"
                             [pageSizeOptions]="pageSizeOptions$ | async"
                             (page)="onPageChanged($event)">
              </mat-paginator>
              <mat-card>New comments: {{ newComments$ | async }}</mat-card>
              <app-comment-preview *ngFor="let comment of (comments$ | async)"
                                   [commentItem]="comment"
                                   (editComment)="editComment($event)"
                                   (deleteComment)="deleteComment($event)">
              </app-comment-preview>
            </div>
          </div>
        </mat-dialog-content>
      </mat-card-content>
    </mat-card>
    <mat-dialog-actions align="end" *ngIf="modalMode">
      <button mat-raised-button color="accent" [matDialogClose]>
        <mat-icon matSuffix>close</mat-icon>
        Cancel
      </button>
    </mat-dialog-actions>
  `,
  styles: [`
    .comment-container {
      display: flex;
      align-content: center;
      justify-content: space-between;
    }
  `],
})
export class CommentsComponent implements OnDestroy {
  @Select(CommentsState.results) results$: Observable<any>;
  @Select(CommentsState.count) count$: Observable<number>;
  @Select(CommentsState.pageSize) pageSize$: Observable<number>;
  @Select(CommentsState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;
  @Select(CommentsState.comments) comments$: Observable<Array<CommentItem>>;
  @Select(CommentsState.currentComment) currentComment$: Observable<CommentItem>;
  @Select(CommentsState.editCommentMode) editCommentMode$: Observable<boolean>;
  @Select(CommentsState.newComments) newComments$: Observable<number>;
  @Select(CommentsState.errors) errors$: Observable<object>;

  private params = {};

  commentForm = new FormGroup({
    title: new FormControl('',
      Validators.compose([Validators.required, Validators.maxLength(environment.maxCommentTitleInputLength)])),
    comment: new FormControl('',
      Validators.compose([Validators.required, Validators.maxLength(environment.maxCommentBodyInputLength)])),
    id: new FormControl(''),
  });

  private static getPaginationParams(paginatedData: PageEvent): object {
    return {
      limit: paginatedData.pageSize,
      offset: paginatedData.pageIndex * paginatedData.pageSize,
    };
  }

  constructor(private store: Store) {
  }

  ngOnDestroy() {
    this.store.dispatch(new CommentsActions.ResetCommentState());
  }

  public submitForm(formData: CommentModel) {
    if (this.store.selectSnapshot(CommentsState.editCommentMode)) {
      this.store.dispatch(new CommentsActions.SaveComment(formData.id, formData));
    } else {
      Object.assign(formData, {source: this.store.selectSnapshot(CommentsState.sourceId)});
      this.store.dispatch(new CommentsActions.CreateNewComment(formData));
    }
    this.resetForm();
  }

  public onPageChanged(paginationData: PageEvent) {
    this.updatePageParams(CommentsComponent.getPaginationParams(paginationData));
    this.store.dispatch(new CommentsActions.ChangePagination(this.params));
  }

  public deleteComment(commentId: number) {
    this.store.dispatch(new CommentsActions.DeleteComment(commentId));
  }

  public editComment(comment: CommentModel) {
    this.store.dispatch(new CommentsActions.SetEditCommentMode(true));
    this.store.dispatch(new CommentsActions.GetCurrentComment(comment.id));
  }

  public closeEditForm() {
    this.store.dispatch(new CommentsActions.SetEditCommentMode(false));
    this.store.dispatch(new CommentsActions.ResetCurrentComment());
    this.resetForm();
  }

  public get modalMode() {
    return this.store.selectSnapshot(CommentsState.modalMode);
  }

  private updatePageParams(params: object) {
    this.params = Object.assign(this.params, params);
  }

  private resetForm() {
    this.commentForm.reset();
  }
}
