import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreState } from '../../core/states/core.state';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { Industry } from '../../shared/models/industry.model';


@Component({
  selector: 'app-company-profile-info-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Info</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field>
            <input type="text" matInput placeholder="Company name" formControlName="name">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.name"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <textarea matInput placeholder="Company profile" formControlName="description">
            </textarea>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.description"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <span matPrefix>+ &nbsp;</span>
            <input type="tel" matInput placeholder="Phone" formControlName="phone">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.phone"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <span matPrefix>+ &nbsp;</span>
            <input type="tel" matInput placeholder="Fax" formControlName="fax">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.fax"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input type="email" matInput placeholder="Email" formControlName="email">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.email"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input type="email" matInput placeholder="Website" formControlName="website">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.website"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <mat-select placeholder="Industry" formControlName="industry"
                        [compareWith]="compState" [value]="initialData?.industry" required>
              <mat-option *ngFor="let industry of industries$ | async" [value]="industry">
                {{industry.name}}
              </mat-option>
            </mat-select>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.industry"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <ng-content></ng-content>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class CompanyProfileInfoFormComponent extends BaseFormComponent {
  @Select(CoreState.industries) industries$: Observable<Industry[]>;
}
