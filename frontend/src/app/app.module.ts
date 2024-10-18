// Modules
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
// import { NgxsLoggerPluginModule } from '@ngxs/logger-plugin';
import { NgxsReduxDevtoolsPluginModule } from '@ngxs/devtools-plugin';
import { NgxsFormPluginModule } from '@ngxs/form-plugin';
import { NgxsRouterPluginModule } from '@ngxs/router-plugin';
import { NgxsStoragePluginModule } from '@ngxs/storage-plugin';
import { NgxsModule } from '@ngxs/store';
import {
  CalendarDateFormatter,
  CalendarModule,
  CalendarMomentDateFormatter,
  DateAdapter,
  MOMENT
} from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/moment';
import * as moment from 'moment';
import { NgxPermissionsModule } from 'ngx-permissions';
import { AppRoutingModule } from './app-routing.module';
import { AuthModule } from './modules/auth/auth.module';
import { CoreModule } from './modules/core/core.module';
import { SharedModule } from './modules/shared';

// Components
import { AppComponent } from './modules/core/containers/app.container';

export function momentAdapterFactory() {
  return adapterFactory(moment);
}


@NgModule({
  imports: [
    CommonModule,
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AuthModule,
    AppRoutingModule,
    // Third-Party
    NgxPermissionsModule.forRoot(),
    NgxsModule.forRoot([]),
    NgxsReduxDevtoolsPluginModule.forRoot(),
    NgxsRouterPluginModule.forRoot(),
    // NgxsLoggerPluginModule.forRoot(),
    NgxsStoragePluginModule.forRoot({
      key: ['auth.token', 'auth.expiresAt', 'auth.user', 'core.settings.validators'],
    }),
    NgxsFormPluginModule.forRoot(),
    CalendarModule.forRoot(
      {
        provide: DateAdapter,
        useFactory: momentAdapterFactory
      },
      {
        dateFormatter: {
          provide: CalendarDateFormatter,
          useClass: CalendarMomentDateFormatter
        }
      }
    ),
    // Custom Modules
    CoreModule,
    SharedModule,
  ],
  bootstrap: [AppComponent],
  providers: [
    {
      provide: MOMENT,
      useValue: moment
    }
  ]
})
export class AppModule {
}
