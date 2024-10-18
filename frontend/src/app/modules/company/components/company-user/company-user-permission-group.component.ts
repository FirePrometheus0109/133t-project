import {Component, EventEmitter, Input, Output} from '@angular/core';
import {GroupedPermission} from '../../../shared/models/permissions.model';

@Component({
  selector: 'app-company-user-permission-group',
  template: `
    <mat-card>
      <mat-card-title>
        <span>{{groupTitle}}</span>
      </mat-card-title>
      <mat-card-content>
        <app-company-user-permission *ngFor="let permission of permissions"
                                     [permission]="permission"
                                     (permissionSwitched)="permissionSwitched.emit($event)">
        </app-company-user-permission>
      </mat-card-content>
    </mat-card>

  `,
  styles: [],
})
export class CompanyUserPermissionGroupComponent {
  @Input() groupTitle: string;
  @Input() permissions: Array<GroupedPermission>;
  @Output() permissionSwitched = new EventEmitter<GroupedPermission>();
}
