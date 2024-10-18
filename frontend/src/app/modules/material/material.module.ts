import { NgModule } from '@angular/core';
import { NgxPermissionsModule } from 'ngx-permissions';

import {
  MAT_DIALOG_DATA,
  MatAutocompleteModule,
  MatBadgeModule,
  MatButtonModule,
  MatButtonToggleModule,
  MatCardModule,
  MatCheckboxModule,
  MatChipsModule,
  MatDatepickerModule,
  MatDialogModule,
  MatExpansionModule,
  MatGridListModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatMenuModule,
  MatNativeDateModule,
  MatPaginatorModule,
  MatProgressBarModule,
  MatProgressSpinnerModule,
  MatRadioModule,
  MatSelectModule,
  MatSidenavModule,
  MatSlideToggleModule,
  MatSnackBarModule,
  MatSortModule,
  MatStepperModule,
  MatTableModule,
  MatTabsModule,
  MatToolbarModule,
  MatTooltipModule,
  MatTreeModule
} from '@angular/material';
import { MAT_MOMENT_DATE_ADAPTER_OPTIONS, MatMomentDateModule } from '@angular/material-moment-adapter';

const IMPORTED_MAT_MODULES = [
  NgxPermissionsModule,
  MatInputModule,
  MatCardModule,
  MatButtonModule,
  MatSlideToggleModule,
  MatButtonToggleModule,
  MatSidenavModule,
  MatListModule,
  MatIconModule,
  MatToolbarModule,
  MatProgressSpinnerModule,
  MatDialogModule,
  MatSnackBarModule,
  MatExpansionModule,
  MatProgressBarModule,
  MatGridListModule,
  MatSelectModule,
  MatStepperModule,
  MatAutocompleteModule,
  MatChipsModule,
  MatDatepickerModule,
  MatNativeDateModule,
  MatCheckboxModule,
  MatMenuModule,
  MatTooltipModule,
  MatTabsModule,
  MatBadgeModule,
  MatPaginatorModule,
  MatRadioModule,
  MatSortModule,
  MatTableModule,
  MatTreeModule,
  MatMomentDateModule
];


@NgModule({
  imports: IMPORTED_MAT_MODULES,
  exports: IMPORTED_MAT_MODULES,
  providers: [
    {provide: MAT_DIALOG_DATA, useValue: {}},
    {provide: MAT_MOMENT_DATE_ADAPTER_OPTIONS, useValue: {useUtc: true}}
  ]
})
export class MaterialModule {
}
