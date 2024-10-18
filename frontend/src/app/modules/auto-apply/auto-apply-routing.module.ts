// Modules
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Guards
import { AuthGuard } from '../auth/services/auth-guard.service';
import { JSPMyGuard } from '../job-seeker/services/jsp-my-guard.service';
import { CanDeactivateGuard } from '../shared/services/page-leaving-guard.service';

// Constants
import { AutoApplyRoute } from '../shared/constants/routes/auto-apply-routes';

// components
import { AutoApplyEditComponent } from './containers/auto-apply-edit.container';
import { AutoApplyListComponent } from './containers/auto-apply-list.container';
import { AutoApplyResultComponent } from './containers/auto-apply-result.container';

// Resolvers
import { AutoApplyCreatePageResolver } from './resolvers/auto-apply-create-page.resolver';
import { AutoApplyEditPageResolver } from './resolvers/auto-apply-edit-page.resolver';
import { AutoApplyListPageResolver } from './resolvers/auto-apply-list-page.resolver';
import { AutoApplyResultPageResolver } from './resolvers/auto-apply-result-page.resolver';

const AutoApplyRoutes: Routes = [
  {
    path: AutoApplyRoute.autoApplyListRoute,
    component: AutoApplyListComponent,
    canActivate: [JSPMyGuard, AuthGuard],
    resolve: {
      data: AutoApplyListPageResolver
    }
  },
  {
    path: AutoApplyRoute.autoApplyCreateRoute,
    component: AutoApplyEditComponent,
    canActivate: [AuthGuard],
    canDeactivate: [CanDeactivateGuard],
    resolve: {
      data: AutoApplyCreatePageResolver
    }
  },
  {
    path: AutoApplyRoute.autoApplyEditRoute,
    component: AutoApplyEditComponent,
    canActivate: [JSPMyGuard, AuthGuard],
    resolve: {
      data: AutoApplyEditPageResolver
    }
  },
  {
    path: AutoApplyRoute.autoApplyResultRoute,
    component: AutoApplyResultComponent,
    canActivate: [JSPMyGuard, AuthGuard],
    resolve: {
      data: AutoApplyResultPageResolver
    }
  },
];


@NgModule({
  imports: [
    RouterModule.forChild(AutoApplyRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class AutoApplyRoutingModule {
}
