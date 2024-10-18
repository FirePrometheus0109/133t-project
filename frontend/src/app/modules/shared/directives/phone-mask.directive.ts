import { Directive, HostListener } from '@angular/core';
import { NgControl } from '@angular/forms';
import StringMask from 'string-mask';


@Directive({
  selector: '[formControlName][appPhoneMask]'
})
export class PhoneMaskDirective {
  static readonly formatter = new StringMask('0-000-000-0000');

  constructor(public ngControl: NgControl) {
  }

  @HostListener('ngModelChange', ['$event'])
  onModelChange(phoneString) {
    this.onInputChange(phoneString);
  }

  @HostListener('keydown.backspace', ['$event'])
  keydownBackspace(event) {
    this.onInputChange(event.target.value);
  }

  onInputChange(phoneString: string) {
    this.ngControl.valueAccessor.writeValue(
      PhoneMaskDirective.formatter.apply(phoneString.replace(/\D/g, ''))
    );
  }
}
