import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerSavedJobsListComponent } from './job-seeker-saved-jobs-list.component';

describe('JobSeekerSavedJobsListComponent', () => {
  let component: JobSeekerSavedJobsListComponent;
  let fixture: ComponentFixture<JobSeekerSavedJobsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobSeekerSavedJobsListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobSeekerSavedJobsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
