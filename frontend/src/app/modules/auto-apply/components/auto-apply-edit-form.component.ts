import { Component, EventEmitter, Input, Output } from '@angular/core';
import { BaseFormComponent } from '../../shared/components/base-form.component';


@Component({
  selector: 'app-auto-apply-edit-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4 *ngIf="this.create_mode">Create</h4>
        <h4 *ngIf="!this.create_mode">Edit</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-action-row>
            <mat-form-field>
              <input matInput placeholder="Auto apply title" formControlName="title" (change)="titleChanged($event)">
            </mat-form-field>
            <app-control-messages [form]="form"
                                  [control]="f.title"
                                  [submitted]="isSubmitted"
                                  [errors]="errors">
            </app-control-messages>
            <mat-form-field>
              <input matInput placeholder="Specify number of applications" formControlName="number" type="number"
                     max="30"
                     (change)="numberChanged($event)"
                     pattern="^(0?[1-9]|[12][0-9]|3[0])$">
            </mat-form-field>
            <app-control-messages [form]="form"
                                  [control]="f.number"
                                  [submitted]="isSubmitted"
                                  [errors]="errors">
            </app-control-messages>
            <button type="submit" mat-raised-button color="primary" [disabled]='!form.valid'>
              <span *ngIf="this.create_mode">Create auto apply</span>
              <span *ngIf="!this.create_mode">Save auto apply</span>
              <mat-icon matSuffix>save</mat-icon>
            </button>
          </mat-action-row>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class AutoApplyEditFormComponent extends BaseFormComponent {
  @Input() create_mode: boolean;
  @Output() changedSpecifyNumber = new EventEmitter<number>();
  @Output() changedTitle = new EventEmitter<string>();

  numberChanged(value) {
    const newValue = value.target.value;
    this.changedSpecifyNumber.emit(newValue);
  }

  titleChanged(value) {
    const newValue = value.target.value;
    this.changedTitle.emit(newValue);
  }
}
