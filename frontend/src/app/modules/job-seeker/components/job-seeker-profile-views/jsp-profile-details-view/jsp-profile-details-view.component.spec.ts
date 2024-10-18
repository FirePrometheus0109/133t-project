import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JspProfileDetailsViewComponent } from './jsp-profile-details-view.component';

describe('JspProfileDetailsViewComponent', () => {
  let component: JspProfileDetailsViewComponent;
  let fixture: ComponentFixture<JspProfileDetailsViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JspProfileDetailsViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JspProfileDetailsViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
