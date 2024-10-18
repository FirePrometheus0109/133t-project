import {Component, EventEmitter, Input, Output} from '@angular/core';
import {User} from '../models/user.model';

@Component({
  selector: 'app-view-account',
  template: `
    <mat-card>
      <mat-card-content>
        First name {{user.first_name}}
      </mat-card-content>
      <mat-card-content>
        Last name {{user.last_name}}
      </mat-card-content>
      <mat-card-content>
        Email {{user.email}}
      </mat-card-content>
      <button mat-button color="primary" (click)="changePassword()">Password change</button>
      <div class="controls-container">
        <button mat-button color="primary" (click)="edit()">Edit</button>
      </div>
    </mat-card>
  `,
  styles: [`
    .controls-container {
      display: flex;
      justify-content: center;
      margin-top: 100px;
    }
  `],
})
export class ViewAccountComponent {
  @Input() user: User;
  @Output() changeAccountPassword = new EventEmitter<any>();
  @Output() editAccount = new EventEmitter<any>();

  public changePassword() {
    this.changeAccountPassword.emit();
  }

  public edit() {
    this.editAccount.emit();
  }
}
