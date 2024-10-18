import { Injectable } from '@angular/core';
import { PermissionGroup } from '../../shared/models/permissions.model';
import { ApiService } from '../../shared/services/api.service';
import { CompanyUserData } from '../models/company-user.model';


@Injectable()
export class CompanyUserService {
  route = 'company-user';
  permissionGrouped = 'permission-groups';
  initialPermissionGrouped = 'initial-permission-groups';
  companyUserRestore = 'company-user-restore';
  candidateStatuses = 'viewed-candidates-statuses';

  constructor(private api: ApiService) {
  }

  public getCompanyUsers(params?: object) {
    return this.api.get(`${this.route}`, params);
  }

  public getPermissionGrouped() {
    return this.api.get(`${this.permissionGrouped}`);
  }

  public getInitialPermissionGrouped() {
    return this.api.get(`${this.initialPermissionGrouped}`);
  }

  public createNewCompanyUser(userData: CompanyUserData) {
    return this.api.post(`${this.route}`, userData);
  }

  public setCandidateStatuses(statusIds: Array<any>) {
    return this.api.post(`${this.candidateStatuses}`, {statuses : statusIds} );
  }


  public getCompanyUserData(userId: number) {
    return this.api.getById(`${this.route}`, userId);
  }

  public saveCompanyUser(userId: number, userData: CompanyUserData) {
    return this.api.putById(`${this.route}`, userId, userData);
  }

  public deleteCompanyUser(userId: number) {
    return this.api.deleteById(`${this.route}`, userId);
  }

  public restoreCompanyUser(userData: CompanyUserData) {
    return this.api.post(`${this.companyUserRestore}`, userData);
  }

  public setPermissionsByUsersPermissions(permissionData: Array<PermissionGroup>, userPermissionData: Array<PermissionGroup>) {
    return permissionData.map((group) => {
      group.permissions.forEach(permission => {
        userPermissionData.forEach(userGroup => userGroup.permissions.forEach(userPermission => {
          if (userPermission.id === permission.id) {
            permission.isChecked = true;
          }
        }));
      });
    });
  }

  public setPermissionsByInitial(userPermissionData: Array<PermissionGroup>) {
    const result = [];
    userPermissionData.forEach(userGroup => userGroup.permissions.forEach(userPermission => {
      userPermission.isChecked = true;
      result.push(userPermission);
    }));
    return result;
  }

  public setSelectedPermissions(permissionData: Array<PermissionGroup>) {
    const selected = [];
    permissionData.forEach(group => group.permissions.forEach(permission => {
      if (permission.isChecked) {
        selected.push(permission);
      }
    }));
    return selected;
  }
}
