import { Component, EventEmitter, Input, Output } from '@angular/core';
import { AutoapplyStatusEnum } from '../../shared/models/enums.model';
import { AutoApply } from '../models/auto-apply.model';


@Component({
  selector: 'app-auto-apply-preview',
  template: `
    <div class="auto-apply-preview">
      <mat-card>
        <mat-card-header>
          <mat-card-title>
            {{autoApplyItem.title}}
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div>
            Number of jobs in the list: {{autoApplyItem.jobs_count}}
            <span *ngIf="autoApplyItem.new_jobs_count"
                  matBadge="{{autoApplyItem.new_jobs_count}}"
                  [matBadgeOverlap]="false" [matBadgeColor]="'warn'">
            </span>
          </div>
          <div>Status: <b>{{autoApplyEnums[autoApplyItem.status]}}</b></div>
          <div *ngIf="autoApplyEnums[autoApplyItem.status] === autoApplyEnums.IN_PROGRESS">
            Days to completion: {{autoApplyItem.days_to_completion}}
          </div>
        </mat-card-content>
        <mat-card-actions>
          <button mat-button (click)="goToAutoApply.emit(autoApplyItem)">
            Go to auto apply
            <mat-icon matSuffix>arrow_forward_ios</mat-icon>
          </button>
          <button mat-button (click)="deleteAutoApply.emit(autoApplyItem)">
            Delete
            <mat-icon matSuffix>delete</mat-icon>
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
  styles: [`
    div {
      margin-bottom: 10px;
    }

    .auto-apply-preview {
      border-bottom: 1px solid #607d8b;
    }
  `],
})
export class AutoApplyPreviewComponent {
  @Input() autoApplyItem;
  @Input() autoApplyEnums: AutoapplyStatusEnum;
  @Output() goToAutoApply = new EventEmitter<AutoApply>();
  @Output() deleteAutoApply = new EventEmitter<AutoApply>();
}
