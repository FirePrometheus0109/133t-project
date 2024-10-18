import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerLastViewsListComponent } from './job-seeker-last-views-list.component';

describe('JobSeekerLastViewsListComponent', () => {
  let component: JobSeekerLastViewsListComponent;
  let fixture: ComponentFixture<JobSeekerLastViewsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobSeekerLastViewsListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobSeekerLastViewsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
