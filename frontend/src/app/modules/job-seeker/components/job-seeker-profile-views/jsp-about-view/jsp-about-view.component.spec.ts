import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JspAboutViewComponent } from './jsp-about-view.component';

describe('JspAboutViewComponent', () => {
  let component: JspAboutViewComponent;
  let fixture: ComponentFixture<JspAboutViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JspAboutViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JspAboutViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
