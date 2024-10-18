import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { GroupedPermission, PermissionGroup } from '../../shared/models/permissions.model';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { CompanyUserManagePageActions } from '../actions';
import { CompanyUser } from '../models/company-user.model';
import { CompanyUserService } from '../services/company-user.service';


export class CompanyUserManagePageStateModel {
  status: string;
  errors: object;
  inviteMode: boolean;
  editMode: boolean;
  viewMode: boolean;
  permissionsGrouped: Array<PermissionGroup>;
  initialPermissionsGrouped: Array<PermissionGroup>;
  selectedPermissions: Array<GroupedPermission>;
  currentCompanyUser: CompanyUser;
}


export const DEFAULT_COMPANY_USER_MANAGE_PAGE_STATE = {
  status: '',
  errors: null,
  inviteMode: false,
  editMode: false,
  viewMode: false,
  permissionsGrouped: [],
  initialPermissionsGrouped: [],
  selectedPermissions: [],
  currentCompanyUser: null,
};


@State<CompanyUserManagePageStateModel>({
  name: 'CompanyUserManagePageState',
  defaults: DEFAULT_COMPANY_USER_MANAGE_PAGE_STATE,
})
export class CompanyUserManagePageState {
  @Selector()
  static inviteMode(state: CompanyUserManagePageStateModel) {
    return state.inviteMode;
  }

  @Selector()
  static editMode(state: CompanyUserManagePageStateModel) {
    return state.editMode;
  }

  @Selector()
  static viewMode(state: CompanyUserManagePageStateModel) {
    return state.viewMode;
  }

  @Selector()
  static permissionsGrouped(state: CompanyUserManagePageStateModel) {
    return state.permissionsGrouped;
  }

  @Selector()
  static initialPermissionsGrouped(state: CompanyUserManagePageStateModel) {
    return state.initialPermissionsGrouped;
  }

  @Selector()
  static selectedPermissions(state: CompanyUserManagePageStateModel) {
    return state.selectedPermissions;
  }

  @Selector()
  static currentCompanyUser(state: CompanyUserManagePageStateModel) {
    return state.currentCompanyUser;
  }

  @Selector()
  static errors(state: CompanyUserManagePageStateModel) {
    return state.errors;
  }

  constructor(private companyUserService: CompanyUserService,
              private navigationService: NavigationService) {
  }

  @Action(CompanyUserManagePageActions.LoadGroupedPermissions)
  loadGroupedPermissions(ctx: StateContext<CompanyUserManagePageStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.getPermissionGrouped().pipe(
      tap((result) => {
        state = ctx.getState();
        result.map((group: PermissionGroup) => group.permissions.forEach(permission => {
          permission.isChecked = false;
          if (state.viewMode) {
            permission.isDisabled = true;
          }
        }));
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          permissionsGrouped: result,
          selectedPermissions: this.companyUserService.setSelectedPermissions(result)
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          permissionsGrouped: [],
        }));
      }),
    );
  }

  @Action(CompanyUserManagePageActions.LoadInitialGroupedPermissions)
  loadInitialGroupedPermissions(ctx: StateContext<CompanyUserManagePageStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.getInitialPermissionGrouped().pipe(
      tap((result) => {
        result.map((group: PermissionGroup) => group.permissions.forEach(permission => {
          permission.isChecked = true;
        }));
        state = ctx.getState();
        this.companyUserService.setPermissionsByUsersPermissions(state.permissionsGrouped, result);
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          initialPermissionsGrouped: result,
          selectedPermissions: this.companyUserService.setSelectedPermissions(result)
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          initialPermissionsGrouped: [],
        }));
      }),
    );
  }

  @Action(CompanyUserManagePageActions.SetInviteMode)
  setInviteMode(ctx: StateContext<CompanyUserManagePageStateModel>,
                {value}: CompanyUserManagePageActions.SetInviteMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      inviteMode: value,
      editMode: false,
      viewMode: false,
    });
  }

  @Action(CompanyUserManagePageActions.SetViewMode)
  setViewMode(ctx: StateContext<CompanyUserManagePageStateModel>,
              {value}: CompanyUserManagePageActions.SetViewMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      inviteMode: false,
      editMode: false,
      viewMode: value,
    });
  }

  @Action(CompanyUserManagePageActions.SetEditMode)
  setEditMode(ctx: StateContext<CompanyUserManagePageStateModel>,
              {value}: CompanyUserManagePageActions.SetEditMode) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      inviteMode: false,
      editMode: value,
      viewMode: false,
    });
  }

  @Action(CompanyUserManagePageActions.SetSelectedPermissions)
  setSelectedPermissions(ctx: StateContext<CompanyUserManagePageStateModel>,
                         {selectedPermission}: CompanyUserManagePageActions.SetSelectedPermissions) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    const currentSelectedPermissions = state.selectedPermissions;
    const indexById = currentSelectedPermissions.findIndex(item => item.id === selectedPermission.id);
    if (indexById < 0) {
      selectedPermission.isChecked = true;
      currentSelectedPermissions.push(selectedPermission);
    } else {
      selectedPermission.isChecked = false;
      currentSelectedPermissions.splice(indexById, 1);
    }
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      selectedPermissions: currentSelectedPermissions,
    });
  }

  @Action(CompanyUserManagePageActions.InviteCompanyUser)
  inviteCompanyUser(ctx: StateContext<CompanyUserManagePageStateModel>,
                    {userData}: CompanyUserManagePageActions.InviteCompanyUser) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.createNewCompanyUser(userData).pipe(
      tap((result: any) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null
        });
        this.navigationService.goToCompanyUserListPage();
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: result.detail,
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(CompanyUserManagePageActions.RestoreDeletedCompanyUser)
  restoreDeletedCompanyUser(ctx: StateContext<CompanyUserManagePageStateModel>,
                            {userData}: CompanyUserManagePageActions.RestoreDeletedCompanyUser) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.restoreCompanyUser(userData).pipe(
      tap((result: any) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null
        });
        this.navigationService.goToCompanyUserListPage();
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: result.detail,
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(CompanyUserManagePageActions.LoadCompanyUserData)
  loadCompanyUserData(ctx: StateContext<CompanyUserManagePageStateModel>,
                      {userId}: CompanyUserManagePageActions.LoadCompanyUserData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.getCompanyUserData(userId).pipe(
      tap((result: CompanyUser) => {
        state = ctx.getState();
        this.companyUserService.setPermissionsByUsersPermissions(state.permissionsGrouped, result.permissions_groups);
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          currentCompanyUser: result,
          selectedPermissions: this.companyUserService.setPermissionsByInitial(result.permissions_groups)
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          currentCompanyUser: null,
        }));
      }),
    );
  }

  @Action(CompanyUserManagePageActions.ResetCurrentCompanyUser)
  resetCurrentCompanyUser(ctx: StateContext<CompanyUserManagePageStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      currentCompanyUser: new CompanyUser()
    });
  }

  @Action(CompanyUserManagePageActions.SaveCompanyUser)
  saveCompanyUser(ctx: StateContext<CompanyUserManagePageStateModel>,
                  {userId, userData}: CompanyUserManagePageActions.SaveCompanyUser) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyUserService.saveCompanyUser(userId, userData).pipe(
      tap((result: any) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null
        });
        this.navigationService.goToCompanyUserListPage();
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: result.detail || 'Done',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }
}
