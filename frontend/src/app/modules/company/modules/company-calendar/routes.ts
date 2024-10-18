import { Routes } from '@angular/router';

import { AuthGuard } from '../../../auth/services/auth-guard.service';
import { IsSubsctiptionPurchased } from '../../../subscription/services/subscription-guard.sevice';
import { CompanyGuard } from '../../services/company-guard.service';

import { CompanyCalendarPageResolver } from './resolvers/calendar.resolver';

import { CalendarComponent } from './containers/calendar/calendar.component';


const calendarRoute = 'calendar';

const companyCalendarRoutes: Routes = [
  {
    path: calendarRoute,
    component: CalendarComponent,
    canActivate: [AuthGuard, CompanyGuard, IsSubsctiptionPurchased],
    resolve: {data: CompanyCalendarPageResolver}
  },
];

export {
  calendarRoute,
  companyCalendarRoutes,
};

export default companyCalendarRoutes;
