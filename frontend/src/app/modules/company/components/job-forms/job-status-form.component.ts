import {Component, EventEmitter, Input, Output} from '@angular/core';
import {BaseFormComponent} from '../../../shared/components/base-form.component';
import {JobStatusEnum} from '../../../shared/models/enums.model';

@Component({
  selector: 'app-job-status-form',
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <mat-form-field>
        <mat-select
          placeholder="Status"
          formControlName="status"
          (selectionChange)="statusChanged($event)"
          required>
          <mat-option *ngFor="let status of jobStatusEnum | keys" [value]="status.key">
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
    </form>
  `,
  styles: [],
})
export class JobStatusFormComponent extends BaseFormComponent {
  @Input() jobStatusEnum: JobStatusEnum;
  @Output() selectChange = new EventEmitter<any>();

  public statusChanged(status) {
    this.selectChange.emit(status);
  }
}
