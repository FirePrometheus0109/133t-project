import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StripeDataFormComponent } from './stripe-data-form.component';

describe('StripeDataFormComponent', () => {
  let component: StripeDataFormComponent;
  let fixture: ComponentFixture<StripeDataFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StripeDataFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StripeDataFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
