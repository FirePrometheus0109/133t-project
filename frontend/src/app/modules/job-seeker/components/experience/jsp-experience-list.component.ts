import { Component, EventEmitter, Input, Output } from '@angular/core';
import { BaseFormComponent } from '../../../shared/components/base-form.component';
import { Enums } from '../../../shared/models/enums.model';


@Component({
  selector: 'app-jsp-experience-list-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Job list</h4>
      </mat-card-title>
      <mat-card-content>
        <div *ngFor="let item of initialData">
          <app-jsp-experience-preview [jobItem]="item"
                                      [enums]="enums"
                                      (deleteItem)="deleteJob($event)"
                                      (editItem)="editJobItem.emit($event)">
          </app-jsp-experience-preview>
        </div>

      </mat-card-content>

    </mat-card>
  `,
  styles: [],
})
export class JspExperienceListComponent extends BaseFormComponent {
  @Input() enums: Enums;
  @Output() deletedJobItem = new EventEmitter<number>();
  @Output() editJobItem = new EventEmitter<any>();

  public deleteJob(itemId: number) {
    this.deletedJobItem.emit(itemId);
  }
}
