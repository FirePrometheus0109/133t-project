import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JspMainInfoViewComponent } from './jsp-main-info-view.component';

describe('JspMainInfoViewComponent', () => {
  let component: JspMainInfoViewComponent;
  let fixture: ComponentFixture<JspMainInfoViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JspMainInfoViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JspMainInfoViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
