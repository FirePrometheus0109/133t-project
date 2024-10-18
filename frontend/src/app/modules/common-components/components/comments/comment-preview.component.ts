import {Component, EventEmitter, Input, Output} from '@angular/core';
import {CommentItem} from '../../models/comment.model';

@Component({
  selector: 'app-comment-preview',
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>
          <span>{{commentItem.title}}</span>
          <span>
            - {{commentItem.user.name}}
          </span>
        </mat-card-title>
        <mat-card-subtitle>
          <span>{{commentItem.submit_date | date}}</span>
        </mat-card-subtitle>
      </mat-card-header>
      <mat-card-content>
        <div>
          <span>{{commentItem.comment}}</span>
        </div>
      </mat-card-content>
      <mat-card-actions align="end">
        <ng-template [ngxPermissionsOnly]="['change_jobcomment', 'change_jobseekercomment']">
          <button mat-button (click)="editComment.emit(commentItem)">
            <mat-icon matSuffix>edit</mat-icon>
          </button>
        </ng-template>
        <ng-template [ngxPermissionsOnly]="['delete_jobcomment', 'delete_jobseekercomment']">
          <button mat-button (click)="deleteComment.emit(commentItem.id)">
            <mat-icon matSuffix>delete</mat-icon>
          </button>
        </ng-template>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [],
})
export class CommentPreviewComponent {
  @Input() commentItem: CommentItem;
  @Output() editComment = new EventEmitter<CommentItem>();
  @Output() deleteComment = new EventEmitter<number>();
}
