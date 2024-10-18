import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JspAddressViewComponent } from './jsp-address-view.component';

describe('JspAddressViewComponent', () => {
  let component: JspAddressViewComponent;
  let fixture: ComponentFixture<JspAddressViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JspAddressViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JspAddressViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
