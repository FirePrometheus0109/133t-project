import { LoggedUser } from '../../auth/models/user.model';
import { PermissionGroup } from '../../shared/models/permissions.model';


export class CompanyUser {
  id: number;
  user: LoggedUser;
  permissions_groups: Array<PermissionGroup>;
  status: string;
}


export class CompanyUserData {
  last_name: string;
  first_name: string;
  email?: string;
  permissions_groups: Array<number>;
  status?: string;
}
