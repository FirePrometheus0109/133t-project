import {Component, Input} from '@angular/core';
import {BaseFormComponent} from '../../../shared/components/base-form.component';
import {CompanyUserStatusEnum, Enums} from '../../../shared/models/enums.model';

@Component({
  selector: 'app-company-user-form',
  template: `
    <form [formGroup]="form">
      <div *ngIf="form.controls.status">
        <div *ngIf="!isStatusNew && !isCurrentUser">
          <mat-form-field>
            <mat-select placeholder="Status" formControlName="status">
              <mat-option *ngFor="let status of userStatusEnum | keys" [value]="status.key">
                {{status.value}}
              </mat-option>
            </mat-select>
          </mat-form-field>
          <app-control-messages
            [form]="form"
            [control]="f.status"
            [submitted]="isSubmitted"
            [errors]="errors">
          </app-control-messages>
        </div>
        <div *ngIf="isStatusNew || isCurrentUser">
          Status: {{enums.CompanyUserStatus[form.controls.status.value]}}
        </div>
      </div>
      <div>
        <mat-form-field>
          <input type="text" matInput placeholder="First name" formControlName="first_name">
        </mat-form-field>
        <app-control-messages
          [form]="form"
          [control]="f.first_name"
          [submitted]="isSubmitted"
          [errors]="errors">
        </app-control-messages>
      </div>
      <div>
        <mat-form-field>
          <input type="text" matInput placeholder="Last name" formControlName="last_name">
        </mat-form-field>
        <app-control-messages
          [form]="form"
          [control]="f.last_name"
          [submitted]="isSubmitted"
          [errors]="errors">
        </app-control-messages>
      </div>
      <div *ngIf="!editMode">
        <mat-form-field>
          <input type="text" matInput placeholder="Email" formControlName="email">
        </mat-form-field>
        <app-control-messages
          [form]="form"
          [control]="f.email"
          [submitted]="isSubmitted"
          [errors]="errors">
        </app-control-messages>
      </div>
      <div *ngIf="editMode">
        Email: {{initialData.email}}
      </div>
    </form>
  `,
  styles: [],
})
export class CompanyUserFormComponent extends BaseFormComponent {
  @Input() userStatusEnum: CompanyUserStatusEnum;
  @Input() enums: Enums;
  @Input() editMode: boolean;
  @Input() isCurrentUser: boolean;

  public get isStatusNew() {
    return this.enums.CompanyUserStatus[this.form.controls.status.value] === this.enums.CompanyUserStatus.NEW;
  }
}
