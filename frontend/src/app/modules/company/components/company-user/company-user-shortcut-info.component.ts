import {Component, Input} from '@angular/core';
import {Enums} from '../../../shared/models/enums.model';
import {CompanyUser} from '../../models/company-user.model';

@Component({
  selector: 'app-company-user-shortcut-info',
  template: `
    <div>
      Status: {{enums.CompanyUserStatus[userData.status]}}
    </div>
    <div>
      First name: {{userData.user.first_name}}
    </div>
    <div>
      Last name: {{userData.user.last_name}}
    </div>
    <div>
      Email: {{userData.user.email}}
    </div>
  `,
  styles: [],
})
export class CompanyUserShortcutInfoComponent {
  @Input() enums: Enums;
  @Input() userData: CompanyUser;
}
