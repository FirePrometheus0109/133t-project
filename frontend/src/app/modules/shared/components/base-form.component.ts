import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { debounceTime } from 'rxjs/internal/operators';
import { environment } from '../../../../environments/environment';


@Component({
  selector: 'app-base-form-container',
  template: ``,
  styles: [],
})
export class BaseFormComponent implements OnInit {
  @Input()
  set pending(isPending: boolean) {
    this.handlePending.emit(isPending);
  }

  // initialData <--
  public _initialData: any | null;
  @Input()
  public set initialData(initialData: any) {
    this._initialData = initialData;
    if (initialData) {
      this.handleSetInitialData.emit(initialData);
    }
  }

  public get initialData(): any {
    return this._initialData;
  }

  // initialData -->

  // form <--
  private _form: FormGroup;
  @Input()
  set form(form: FormGroup) {
    this._form = form;
    if (form) {
      this.handleFormIsInstalled.emit(form);
    }
  }

  get form(): FormGroup {
    return this._form;
  }

  // form -->

  @Input() errors: object | null;
  @Output() submitted = new EventEmitter<any>();
  @Output() submittedChanges = new EventEmitter<any>();
  @Output() valueChanged = new EventEmitter<any>();
  @Output() handleFormPatch = new EventEmitter<any>();

  handlePending = new EventEmitter<any>();
  handleFormIsInstalled = new EventEmitter<any>();
  handleSetInitialData = new EventEmitter<any>();

  isSubmitted = false;

  ngOnInit() {
    this.handleFormPatch.subscribe((data) => {
      this.form.patchValue(data);
    });
    this.handlePending.subscribe((value: boolean) => {
      if (this.form) {
        if (value) {
          this.form.disable();
        } else {
          this.form.enable();
        }
      }
    });
    this.handleSetInitialData.subscribe((initialData) => {
      if (this.form && initialData) {
        this.handleFormPatch.emit(initialData);
      }
    });
    this.emitAll();
    // using for search changes in form
    if (this.form) {
      this.form.valueChanges.pipe(debounceTime(environment.searchDebounceTime)).subscribe((changedData) => {
        this.valueChanged.emit(changedData);
      });
    }
  }

  public emitAll(): void {
    this.handleFormIsInstalled.emit(this.form);
    this.handleSetInitialData.emit(this.initialData);
    this.handlePending.emit(this.pending);
  }

  get f() {
    return this.form['controls'];
  }

  get pf() {
    return this.form['controls'].passwords['controls'];
  }

  submit() {
    if (this.form.valid) {
      this.submitted.emit(this.form.value);
    }
  }

  submitChanges() {
    // submit only changed data
    if (this.form.valid) {
      const changedData = {};
      const formValue = this.form.value;

      for (const key in formValue) {
        if (formValue.hasOwnProperty(key)) {
          if (formValue[key] !== this.initialData[key]) {
            changedData[key] = formValue[key];
          }
        }
      }
      this.submittedChanges.emit(changedData);
    }
  }


  compState(o1: any, o2: any): boolean {
    if ((o1 === null && o2 !== null) || (o2 === null && o1 !== null)) {
      return false;
    }
    return o1.id === o2.id;
  }
}
