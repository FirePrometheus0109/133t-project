import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerManageNotificationsComponent } from './job-seeker-manage-notifications.component';

describe('JobSeekerManageNotificationsComponent', () => {
  let component: JobSeekerManageNotificationsComponent;
  let fixture: ComponentFixture<JobSeekerManageNotificationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobSeekerManageNotificationsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobSeekerManageNotificationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
