import { Component } from '@angular/core';
import { BaseFormComponent } from '../../../shared/components/base-form.component';


@Component({
  selector: 'app-forgot-password-form',
  templateUrl: './forgot-password-form.component.html',
  styleUrls: ['./forgot-password-form.component.css']
})
export class ForgotPasswordFormComponent extends BaseFormComponent {

  public get emailPlaceholder() {
    if ((this.initialData && this.initialData.email) || this.form.value.email) {
      return `Email`;
    } else {
      return `Enter your email`;
    }
  }
}
