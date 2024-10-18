import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/internal/operators';
import { environment } from '../../../../../environments/environment';
import { AuthState } from '../../../auth/states/auth.state';
import { NavigationService } from '../../../core/services/navigation.service';
import { CoreState } from '../../../core/states/core.state';
import { InputLengths } from '../../../shared/constants/validators/input-length';
import { CompanyUserStatuses } from '../../../shared/enums/company-user-statuses';
import { Enums } from '../../../shared/models/enums.model';
import { GroupedPermission, PermissionGroup } from '../../../shared/models/permissions.model';
import { ConfirmationDialogService } from '../../../shared/services/confirmation-dialog.service';
import { ValidationService } from '../../../shared/services/validation.service';
import { CompanyUserManagePageActions } from '../../actions';
import { CompanyUser, CompanyUserData } from '../../models/company-user.model';
import { CompanyUserManagePageState } from '../../states/company-user-manage-page.state';


@Component({
  selector: 'app-company-user-manage-page',
  template: `
    <mat-card>
      <mat-card-title>
        <span *ngIf="inviteMode$ | async">Invite user</span>
        <span *ngIf="!(inviteMode$ | async)">
          <span *ngIf="currentCompanyUser$ | async">
            {{(currentCompanyUser$ | async).user.first_name}}, {{(currentCompanyUser$ | async).user.last_name}}
          </span>
        </span>
      </mat-card-title>
      <mat-card-content>
        <div *ngIf="!(viewMode$ | async)">
          <app-company-user-form [form]="companyUserForm"
                                 [editMode]="editMode$ | async"
                                 [enums]="enums$ | async"
                                 [userStatusEnum]="CompanyUserStatuses"
                                 [isCurrentUser]="checkIsCurrentUser()"
                                 [initialData]="userData">
          </app-company-user-form>
        </div>
        <app-company-user-shortcut-info *ngIf="viewMode$ | async"
                                        [enums]="(enums$ | async)"
                                        [userData]="(currentCompanyUser$ | async)">
        </app-company-user-shortcut-info>
        <div>
          <span>Permissions:</span>
          <app-company-user-permission-group *ngFor="let permissionGroup of (permissionsGrouped$ | async)"
                                             [groupTitle]="permissionGroup.title"
                                             [permissions]="permissionGroup.permissions"
                                             (permissionSwitched)="permissionSwitched($event)">
          </app-company-user-permission-group>
        </div>
      </mat-card-content>
      <mat-card-actions>
        <button type="button" mat-raised-button color="primary"
                *ngIf="inviteMode$ | async"
                [disabled]="companyUserForm.invalid"
                (click)="inviteNewUser()">
          Invite
        </button>
        <button type="button" mat-raised-button color="primary" *ngIf="viewMode$ | async" (click)="goToUserEdit()">
          Edit
        </button>
        <button type="button" mat-raised-button color="primary" *ngIf="editMode$ | async" (click)="saveCompanyUser()">
          Save
        </button>
        <button type="button" mat-raised-button color="primary" *ngIf="!(viewMode$ | async)" (click)="goToUsersList()">
          Cancel
        </button>
      </mat-card-actions>
    </mat-card>

  `,
  styles: [],
})
export class CompanyUserManageComponent implements OnInit {
  @Select(CoreState.enums) enums$: Observable<Enums>;
  @Select(CompanyUserManagePageState.inviteMode) inviteMode$: Observable<boolean>;
  @Select(CompanyUserManagePageState.errors) errors$: Observable<object>;
  @Select(CompanyUserManagePageState.editMode) editMode$: Observable<boolean>;
  @Select(CompanyUserManagePageState.viewMode) viewMode$: Observable<boolean>;
  @Select(CompanyUserManagePageState.permissionsGrouped) permissionsGrouped$: Observable<Array<PermissionGroup>>;
  @Select(CompanyUserManagePageState.currentCompanyUser) currentCompanyUser$: Observable<CompanyUser>;

  public CompanyUserStatuses = CompanyUserStatuses;
  public userData: any;
  private companyUserId: number;

  companyUserForm = new FormGroup({
    first_name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
    last_name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
    email: new FormControl('', Validators.compose([Validators.required, ValidationService.emailValidator])),
  });

  constructor(private store: Store, private route: ActivatedRoute,
              private navigationService: NavigationService,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  ngOnInit() {
    this.companyUserId = this.route.snapshot.params['id'];
    if (this.store.selectSnapshot(CompanyUserManagePageState.editMode)) {
      this.companyUserForm.addControl('status', new FormControl('', Validators.required));
    }
    this.userData = Object.assign({status: this.currentUser.status}, this.currentUser.user);
  }

  public inviteNewUser() {
    this.store.dispatch(new CompanyUserManagePageActions.InviteCompanyUser(this.prepareCompanyUserData())).pipe(
      catchError(error => {
        return of(error);
      })).subscribe(response => {
      response = response['CompanyUserManagePageState'];
      if (response && response.errors && response.errors.field_errors && response.errors.field_errors.email.includes(
          environment.deletedCompanyUserResponse)) {
        this.confirmationDialogService.openConfirmationDialog({
          message: `${environment.deletedCompanyUserResponse}\n Confirm that you want to restore user's account or use other email.`,
          callback: this.restoreUser.bind(this),
          arg: this.prepareCompanyUserData(),
          confirmationText: 'Confirm',
          dismissible: true,
        });
      }
    });
  }

  public goToUsersList() {
    this.navigationService.goToCompanyUserListPage();
  }

  public goToUserEdit() {
    this.navigationService.goToCompanyUserEditPage(this.companyUserId.toString());
  }

  public saveCompanyUser() {
    this.store.dispatch(new CompanyUserManagePageActions.SaveCompanyUser(this.companyUserId, this.prepareCompanyUserData()));
  }

  public permissionSwitched(switchedPermission: GroupedPermission) {
    this.store.dispatch(new CompanyUserManagePageActions.SetSelectedPermissions(switchedPermission));
  }

  public checkIsCurrentUser() {
    return +this.companyUserId === +this.store.selectSnapshot(AuthState.companyId);
  }

  private prepareCompanyUserData(): CompanyUserData {
    let companyUserData: CompanyUserData;
    companyUserData = Object.assign(this.companyUserForm.value,
      {
        permissions_groups: this.selectedPermissions
          .map(item => item.id)
      });
    if (this.store.selectSnapshot(CompanyUserManagePageState.editMode)) {
      delete companyUserData.email;
    }
    if (this.checkIsCurrentUser() || this.isStatusNew(this.companyUserForm.value.status)) {
      delete companyUserData.status;
    }
    return companyUserData;
  }

  private isStatusNew(status: string) {
    return this.enums.CompanyUserStatus[status] === this.enums.CompanyUserStatus.NEW;
  }

  private get enums() {
    return this.store.selectSnapshot(CoreState.enums);
  }

  private get currentUser() {
    return this.store.selectSnapshot(CompanyUserManagePageState.currentCompanyUser);
  }

  private get selectedPermissions() {
    return this.store.selectSnapshot(CompanyUserManagePageState.selectedPermissions);
  }

  private restoreUser(userData: CompanyUserData) {
    this.store.dispatch(new CompanyUserManagePageActions.RestoreDeletedCompanyUser(userData));
  }
}
