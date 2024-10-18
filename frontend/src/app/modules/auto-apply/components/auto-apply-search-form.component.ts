import { Component } from '@angular/core';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { InputLengths } from '../../shared/constants/validators/input-length';


@Component({
  selector: 'app-auto-apply-search-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Search</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field>
            <input matInput placeholder="Job title" formControlName="search" maxlength="{{inputLengths.titles}}">
          </mat-form-field>
          <app-control-messages
              [form]="form"
              [control]="f.search"
              [submitted]="isSubmitted"
              [errors]="errors">
          </app-control-messages>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class AutoApplySearchFormComponent extends BaseFormComponent {
  public inputLengths = InputLengths;
}
