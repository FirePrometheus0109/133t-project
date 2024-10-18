import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { companyCalendarRoutes } from './routes';


@NgModule({
  imports: [
    RouterModule.forChild(companyCalendarRoutes),
  ],
  exports: [
    RouterModule,
  ],
})
export class CompanyCalendarRoutingModule {}
