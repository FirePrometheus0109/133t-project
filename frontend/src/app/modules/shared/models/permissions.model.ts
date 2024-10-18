export interface GroupedPermission {
  id: number;
  name: string;
  description: string;
  isChecked?: boolean;
  isDisabled?: boolean;
}


export interface PermissionGroup {
  title: string;
  permissions: Array<GroupedPermission>;
}
