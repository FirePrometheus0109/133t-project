import { Component, EventEmitter, Input, Output } from '@angular/core';
import { GroupedPermission } from '../../../shared/models/permissions.model';


@Component({
  selector: 'app-company-user-permission',
  template: `
    <mat-card>
      <mat-card-content>
        <mat-slide-toggle (change)="permissionSwitched.emit(permission)"
                          [checked]="permission.isChecked" [disabled]="permission.isDisabled">
          <span [matTooltip]="permission.description">{{permission.name}}</span>
        </mat-slide-toggle>
      </mat-card-content>
    </mat-card>

  `,
  styles: [`
    /deep/ .mat-slide-toggle.mat-checked:not(.mat-disabled) .mat-slide-toggle-bar {
      background-color: #49c5b6;
    }

    /deep/ .mat-slide-toggle.mat-checked:not(.mat-disabled) .mat-slide-toggle-thumb {
      background-color: #49c5b6;
    }
  `],
})
export class CompanyUserPermissionComponent {
  @Input() permission: GroupedPermission;
  @Output() permissionSwitched = new EventEmitter<GroupedPermission>();
}
