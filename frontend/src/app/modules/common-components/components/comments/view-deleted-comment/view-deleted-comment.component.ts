import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material';


@Component({
  selector: 'app-view-deleted-comment',
  templateUrl: './view-deleted-comment.component.html',
  styleUrls: ['./view-deleted-comment.component.scss']
})
export class ViewDeletedCommentComponent {
  @Output() navigateToUser = new EventEmitter<object>();

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any) {
  }
}
