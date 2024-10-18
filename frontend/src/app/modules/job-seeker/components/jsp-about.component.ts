import { Component } from '@angular/core';
import { BaseFormComponent } from '../../shared/components/base-form.component';


@Component({
  selector: 'app-jsp-about-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>About</h4>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field class="about-section">
            <textarea matInput
                      class="no-resize-textarea"
                      rows="5"
                      placeholder="Let employers know a bit about your professional adveture"
                      formControlName="about">
            </textarea>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.about"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <ng-content></ng-content>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .about-section {
      width: 100%;
    }

    .no-resize-textarea {
      resize: none;
    }
  `],
})
export class JspAboutComponent extends BaseFormComponent {
}
