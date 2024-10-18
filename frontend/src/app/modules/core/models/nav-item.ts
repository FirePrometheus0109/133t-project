export interface NavItem {
  caption: string;
  disabled?: boolean;
  icon: string;
  routerLink?: string;
  children?: NavItem[];
}
