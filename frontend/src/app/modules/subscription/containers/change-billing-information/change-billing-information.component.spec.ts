import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangeBillingInformationComponent } from './change-billing-information.component';

describe('ChangeBillingInformationComponent', () => {
  let component: ChangeBillingInformationComponent;
  let fixture: ComponentFixture<ChangeBillingInformationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChangeBillingInformationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChangeBillingInformationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
