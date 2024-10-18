import { Component, EventEmitter, Input, Output } from '@angular/core';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { InputLengths } from '../../shared/constants/validators/input-length';
import { User } from '../models/user.model';


@Component({
  selector: 'app-edit-account',
  template: `
    <mat-card>
      <form [formGroup]="form">
        <mat-card-content>
          <mat-form-field>
            <input matInput formControlName="first_name" placeholder="First name" [maxlength]="namesInputLengths">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.first_name"
                                [submitted]="isSubmitted">
          </app-control-messages>
        </mat-card-content>
        <mat-card-content>
          <mat-form-field>
            <input matInput formControlName="last_name" placeholder="Last name" [maxlength]="namesInputLengths">
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.last_name"
                                [submitted]="isSubmitted">
          </app-control-messages>
        </mat-card-content>
        <mat-card-content>
          Email {{initialData.email}}
        </mat-card-content>
        <button mat-button color="primary" (click)="changePassword()">Password change</button>
        <div class="controls-container">
          <button mat-button color="primary" (click)="save()">Save</button>
          <button mat-button color="primary" (click)="cancel()">Cancel</button>
        </div>
      </form>
    </mat-card>
  `,
  styles: [`
    .controls-container {
      display: flex;
      justify-content: center;
      margin-top: 100px;
    }
  `,
  ],
})
export class EditAccountComponent extends BaseFormComponent {
  @Input() user: User;
  @Output() changeAccountPassword = new EventEmitter<any>();
  @Output() saveAccount = new EventEmitter<any>();
  @Output() cancelEdit = new EventEmitter<any>();

  public namesInputLengths = InputLengths.names;

  public changePassword() {
    this.changeAccountPassword.emit();
  }

  public save() {
    this.saveAccount.emit();
  }

  public cancel() {
    this.cancelEdit.emit();
  }
}
