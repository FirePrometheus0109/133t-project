import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerPrintViewComponent } from './job-seeker-print-view.component';

describe('JobSeekerPrintViewComponent', () => {
  let component: JobSeekerPrintViewComponent;
  let fixture: ComponentFixture<JobSeekerPrintViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobSeekerPrintViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobSeekerPrintViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
