import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerAutoApplyProgressItemComponent } from './job-seeker-auto-apply-progress-item.component';

describe('JobSeekerAutoApplyProgressItemComponent', () => {
  let component: JobSeekerAutoApplyProgressItemComponent;
  let fixture: ComponentFixture<JobSeekerAutoApplyProgressItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobSeekerAutoApplyProgressItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobSeekerAutoApplyProgressItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
