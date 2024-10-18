import { Component, EventEmitter } from '@angular/core';
import { MatSelectChange } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreActions } from '../../core/actions';
import { CoreState } from '../../core/states/core.state';
import { CityModel, ZipModel } from '../models/address.model';
import { BaseFormComponent } from './base-form.component';


@Component({
  selector: 'app-address-component',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Address</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <table cellspacing="0">
            <tr *ngIf="form.controls.address">
              <td>
                <mat-form-field>
                  <textarea matInput placeholder="Address" formControlName="address"></textarea>
                </mat-form-field>
                <app-control-messages [form]="form"
                                      [control]="f.address"
                                      [submitted]="isSubmitted"
                                      [errors]="errors">
                </app-control-messages>
              </td>
            </tr>
            <tr>
              <td>
                <mat-form-field>
                  <mat-select (selectionChange)="changeValue($event)"
                              placeholder="Country"
                              formControlName="country"
                              [compareWith]="compState">
                    <mat-option *ngFor="let country of countries$ | async" [value]="country">
                      {{country.name}}
                    </mat-option>
                  </mat-select>
                </mat-form-field>
                <app-control-messages [form]="form"
                                      [control]="f.country"
                                      [submitted]="isSubmitted"
                                      [errors]="errors">
                </app-control-messages>
              </td>
              <td>
                <app-city-select [form]="form"
                                 [filteredCities]="citiesFiltered$ | async"
                                 [initialData]="initialData"
                                 (searchLocation)="onCityChanged($event)"
                                 (citySelected)="onCitySelected($event)"></app-city-select>
              </td>
              <td>
                <app-zip-select [form]="form"
                                [isDisabled]="zipDisabled"
                                [initialData]="initialData"
                                [availableZips]="availableZips$ | async"
                                (searchZip)="onZipChanged($event)">
                </app-zip-select>
              </td>
            </tr>
          </table>
          <ng-content></ng-content>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class AddressComponent extends BaseFormComponent {
  @Select(CoreState.countries) countries$: Observable<object[]>;
  @Select(CoreState.citiesFiltered) citiesFiltered$: Observable<CityModel[]>;
  @Select(CoreState.availableZips) availableZips$: Observable<ZipModel[]>;

  constructor(private store: Store) {
    super();
  }

  get zipDisabled() {
    const { city } = this.form.value;
    return !city || !city.id;
  }

  changeValue($event: EventEmitter<MatSelectChange>) {
    this.form.controls['city'].reset();
    this.form.controls['zip'].reset();
  }

  onCityChanged(searchString: string) {
    this.form.controls['zip'].reset();
    const requestData = {
      country_id: this.form.value.country.id,
      name: searchString
    };
    this.store.dispatch(new CoreActions.GetCities(requestData));
  }

  onCitySelected(selectedCityId: number) {
    this.form.controls['zip'].reset();
    this.store.dispatch(new CoreActions.GetZips(selectedCityId));
  }

  onZipChanged(searchString: string) {
    this.store.dispatch(new CoreActions.GetZips(this.form.value.city.id, {search: searchString}));
  }
}
