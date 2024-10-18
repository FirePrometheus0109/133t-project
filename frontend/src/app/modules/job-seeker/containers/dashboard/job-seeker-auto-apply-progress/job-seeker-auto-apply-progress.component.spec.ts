import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerAutoApplyProgressComponent } from './job-seeker-auto-apply-progress.component';

describe('JobSeekerAutoApplyProgressComponent', () => {
  let component: JobSeekerAutoApplyProgressComponent;
  let fixture: ComponentFixture<JobSeekerAutoApplyProgressComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobSeekerAutoApplyProgressComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobSeekerAutoApplyProgressComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
