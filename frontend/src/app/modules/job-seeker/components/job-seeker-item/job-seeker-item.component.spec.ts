import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerItemComponent } from './job-seeker-item.component';

describe('JobSeekerItemComponent', () => {
  let component: JobSeekerItemComponent;
  let fixture: ComponentFixture<JobSeekerItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobSeekerItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobSeekerItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
