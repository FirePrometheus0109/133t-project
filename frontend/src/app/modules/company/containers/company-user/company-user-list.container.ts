import { Component } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { environment } from '../../../../../environments/environment';
import { AuthState } from '../../../auth/states/auth.state';
import { NavigationService } from '../../../core/services/navigation.service';
import { CoreState } from '../../../core/states/core.state';
import { Enums } from '../../../shared/models/enums.model';
import { ConfirmationDialogService } from '../../../shared/services/confirmation-dialog.service';
import { CompanyUserListPageActions } from '../../actions';
import { CompanyUser } from '../../models/company-user.model';
import { CompanyUserListPageState } from '../../states/company-user-list-page.state';


@Component({
  selector: 'app-company-user-list-page',
  template: `
    <mat-card>
      <mat-card-title>
        Users
      </mat-card-title>
      <mat-card-actions *ngxPermissionsOnly="['add_companyuser']">
        <button type="button" mat-raised-button color="primary" [disabled]="isInvitationDisabled()"
                (click)="inviteNewUser()">
          <mat-icon matSuffix>person_add</mat-icon>
          Invite new user
        </button>
        <span>(you can have up to 10 users in Active and New status together)</span>
      </mat-card-actions>
      <mat-card-content *ngxPermissionsOnly="['view_companyuser']">
        <mat-paginator [length]="count$ | async"
                       [pageSize]="pageSize$ | async"
                       [pageSizeOptions]="pageSizeOptions$ | async"
                       (page)="onPageChanged($event)">
        </mat-paginator>
        <app-company-user-preview *ngFor="let companyUser of (companyUserList$ | async)"
                                  [enums]="enums$ | async" [companyUser]="companyUser"
                                  [currentUserId]="companyId$ | async"
                                  (editCompanyUser)="goToUserEdit($event)"
                                  (deleteCompanyUser)="deleteCompanyUser($event)"
                                  (goToCompanyUserView)="goToCompanyUserView($event)">
        </app-company-user-preview>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class CompanyUserListComponent {
  @Select(CoreState.enums) enums$: Observable<Enums>;
  @Select(CompanyUserListPageState.results) results$: Observable<any>;
  @Select(CompanyUserListPageState.count) count$: Observable<number>;
  @Select(CompanyUserListPageState.pageSize) pageSize$: Observable<number>;
  @Select(CompanyUserListPageState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;
  @Select(CompanyUserListPageState.companyUserList) companyUserList$: Observable<Array<CompanyUser>>;
  @Select(AuthState.companyId) companyId$: Observable<number>;

  private params = {};

  private static getPaginationParams(paginatedData: PageEvent): object {
    return {
      limit: paginatedData.pageSize,
      offset: paginatedData.pageIndex * paginatedData.pageSize,
    };
  }

  constructor(private store: Store,
              private navigationService: NavigationService,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  public inviteNewUser() {
    this.navigationService.goToInviteCompanyUserPage();
  }

  public onPageChanged(paginationData: PageEvent) {
    this.updatePageParams(CompanyUserListComponent.getPaginationParams(paginationData));
    this.store.dispatch(new CompanyUserListPageActions.ChangePagination(this.params));
  }

  public isInvitationDisabled() {
    return this.store.selectSnapshot(CompanyUserListPageState.companyUserList).length === environment.maxInvitedUsersCount;
  }

  public goToCompanyUserView(userData: CompanyUser) {
    this.navigationService.goToCompanyUserViewPage(userData.id.toString());
  }

  public goToUserEdit(userData: CompanyUser) {
    this.navigationService.goToCompanyUserEditPage(userData.id.toString());
  }

  public deleteCompanyUser(userData: CompanyUser) {
    this.confirmationDialogService.openConfirmationDialog({
      message: `Are you sure you want to delete account of ${userData.user.first_name} ${userData.user.last_name} from the system?`,
      callback: this.deleteUserAction.bind(this),
      arg: userData.id,
      confirmationText: 'Delete'
    });
  }

  private updatePageParams(params: object) {
    this.params = Object.assign(this.params, params);
  }

  private deleteUserAction(userId: number) {
    this.store.dispatch(new CompanyUserListPageActions.DeleteCompanyUser(userId));
  }
}
