import { Component, OnInit } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { Permission } from '../models/user.model';
import { AuthState } from '../states/auth.state';


@Component({
  selector: 'app-technical-info',
  template: `
    <mat-tab-group>
      <mat-tab>
        <ng-template mat-tab-label>
          <mat-icon class="example-tab-icon">verified_user</mat-icon>
          User Permissions
        </ng-template>

        <table mat-table [dataSource]="permissions$ | async">
          <!-- ID Column -->
          <ng-container matColumnDef="id">
            <th mat-header-cell *matHeaderCellDef> ID</th>
            <td mat-cell *matCellDef="let element"> {{element.id}}</td>
          </ng-container>

          <!-- Name Column -->
          <ng-container matColumnDef="name">
            <th mat-header-cell *matHeaderCellDef> Name</th>
            <td mat-cell *matCellDef="let element"> {{element.name}}</td>
          </ng-container>

          <!-- Code Name Column -->
          <ng-container matColumnDef="codename">
            <th mat-header-cell *matHeaderCellDef> Code Name</th>
            <td mat-cell *matCellDef="let element"> {{element.codename}}</td>
          </ng-container>

          <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
          <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
        </table>
      </mat-tab>

      <mat-tab>
        <ng-template mat-tab-label>
          <mat-icon class="example-tab-icon">supervised_user_circle</mat-icon>
          All Available Permissions
        </ng-template>

        <table mat-table [dataSource]="allPermissions$ | async">
          <!-- ID Column -->
          <ng-container matColumnDef="id">
            <th mat-header-cell *matHeaderCellDef> ID</th>
            <td mat-cell *matCellDef="let element"> {{element.id}}</td>
          </ng-container>

          <!-- Name Column -->
          <ng-container matColumnDef="name">
            <th mat-header-cell *matHeaderCellDef> Name</th>
            <td mat-cell *matCellDef="let element"> {{element.name}}</td>
          </ng-container>

          <!-- Code Name Column -->
          <ng-container matColumnDef="codename">
            <th mat-header-cell *matHeaderCellDef> Code Name</th>
            <td mat-cell *matCellDef="let element"> {{element.codename}}</td>
          </ng-container>

          <tr mat-header-row *matHeaderRowDef="displayedColumns; sticky: true"></tr>
          <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
        </table>
      </mat-tab>
    </mat-tab-group>
  `,
  styles: [],
})
export class TechnicalInfoComponent implements OnInit {
  @Select(AuthState.permissions) permissions$: Observable<Array<Permission>>;
  @Select(AuthState.allPermissions) allPermissions$: Observable<Array<Permission>>;

  public displayedColumns: string[] = ['id', 'name', 'codename'];

  ngOnInit() {
  }
}
