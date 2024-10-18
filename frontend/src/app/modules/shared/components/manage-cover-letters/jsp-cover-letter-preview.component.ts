import {Component, EventEmitter, Input, Output} from '@angular/core';
import {CoverLetterItem} from '../../models/cover-letter.model';

@Component({
  selector: 'app-jsp-cover-letter-preview',
  template: `
    <mat-card>
      <mat-card-content>
        <div class="name">{{coverLetterItem.title}}</div>
        <div class="body">{{coverLetterItem.body}}</div>
        <div class="as-default" *ngIf="coverLetterItem.is_default">
          <mat-icon matSuffix>check_circle</mat-icon>
          Default
        </div>
      </mat-card-content>
      <mat-card-actions>
        <ng-template [ngxPermissionsOnly]="['change_coverletter']">
          <button mat-button (click)="editItem.emit(coverLetterItem)">
            <mat-icon matSuffix>edit</mat-icon>
          </button>
        </ng-template>
        <ng-template [ngxPermissionsOnly]="['delete_coverletter']">
          <button mat-button (click)="deleteItem.emit(coverLetterItem.id)">
            <mat-icon matSuffix>delete</mat-icon>
          </button>
        </ng-template>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [],
})
export class JspCoverLetterPreviewComponent {
  @Input() coverLetterItem: CoverLetterItem;
  @Output() deleteItem = new EventEmitter<number>();
  @Output() editItem = new EventEmitter<CoverLetterItem>();
}
