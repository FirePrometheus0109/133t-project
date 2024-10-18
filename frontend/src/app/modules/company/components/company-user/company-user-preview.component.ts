import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Enums } from '../../../shared/models/enums.model';
import { CompanyUser } from '../../models/company-user.model';


@Component({
  selector: 'app-company-user-preview',
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>
          <span class="title-link" (click)="goToCompanyUserView.emit(companyUser)">
            {{companyUser.user.first_name}}, {{companyUser.user.last_name}}
          </span>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div>Status: {{enums.CompanyUserStatus[companyUser.status]}}</div>
        <div>
          Permissions
          <button mat-icon-button color="accent"
                  matTooltipClass="jsp-profile-validation-tooltip"
                  [matTooltip]="getCompanyUserPermissions()">
            <mat-icon>info</mat-icon>
          </button>
        </div>
      </mat-card-content>
      <mat-card-actions align="end">
        <button mat-button *ngxPermissionsOnly="['change_companyuser']"
                (click)="editCompanyUser.emit(companyUser)">
          <mat-icon matSuffix>edit</mat-icon>
        </button>
        <button mat-button *ngxPermissionsOnly="['delete_companyuser']"
                (click)="deleteCompanyUser.emit(companyUser)"
                [disabled]="companyUser.id === currentUserId">
          <mat-icon matSuffix>delete</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [`
    .title-link {
      cursor: pointer;
    }
  `],
})
export class CompanyUserPreviewComponent {
  @Input() companyUser: CompanyUser;
  @Input() enums: Enums;
  @Input() currentUserId: number;
  @Output() editCompanyUser = new EventEmitter<any>();
  @Output() deleteCompanyUser = new EventEmitter<any>();
  @Output() goToCompanyUserView = new EventEmitter<any>();

  public getCompanyUserPermissions() {
    if (this.companyUser) {
      const result = [];
      this.companyUser.permissions_groups.forEach(group => group.permissions
        .forEach(permission => result.push(permission.name)));
      if (result.length === 0) {
        return 'none';
      } else {
        return result.join('\n');
      }
    }
  }
}
