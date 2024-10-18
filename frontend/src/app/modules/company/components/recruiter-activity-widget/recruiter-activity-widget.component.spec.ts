import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RecruiterActivityWidgetComponent } from './recruiter-activity-widget.component';

describe('RecruiterActivityWidgetComponent', () => {
  let component: RecruiterActivityWidgetComponent;
  let fixture: ComponentFixture<RecruiterActivityWidgetComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecruiterActivityWidgetComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecruiterActivityWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
