import { Component, EventEmitter, Output } from '@angular/core';
import { CoverLetterItem } from '../../models/cover-letter.model';
import { BaseFormComponent } from '../base-form.component';


@Component({
  selector: 'app-jsp-cover-letter-list',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Cover letter list</h4>
      </mat-card-title>
      <mat-card-content>
        <div *ngFor="let item of initialData">
          <app-jsp-cover-letter-preview [coverLetterItem]="item"
                                        (deleteItem)="deletedCoverLetterItem.emit($event)"
                                        (editItem)="editCoverLetterItem.emit($event)">
          </app-jsp-cover-letter-preview>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class JspCoverLetterListComponent extends BaseFormComponent {
  @Output() deletedCoverLetterItem = new EventEmitter<number>();
  @Output() editCoverLetterItem = new EventEmitter<CoverLetterItem>();
}
