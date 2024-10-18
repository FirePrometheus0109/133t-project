import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { InputLengths } from '../../shared/constants/validators/input-length';


@Component({
  selector: 'app-jsp-main-info-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Main Info</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submitChanges()">
          <mat-form-field>
            <input matInput placeholder="First name" formControlName="first_name">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.first_name"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input matInput placeholder="Last Name" formControlName="last_name">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.last_name"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <input matInput placeholder="Email" formControlName="email">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.email"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <mat-form-field>
            <span matPrefix>+ &nbsp;</span>
            <input type="text" matInput placeholder="Phone" formControlName="phone"
                   appPhoneMask maxlength="{{phoneLength}}">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.phone"
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
export class JSPMainInfoFormComponent extends BaseFormComponent implements OnInit {
  @Input() phoneNumber: any;
  @Output() submittedChanges = new EventEmitter<any>();

  public phoneLength = InputLengths.phoneMask;

  ngOnInit() {
    super.ngOnInit();
    this.f.phone.setValue(this.phoneNumber);
  }
}
