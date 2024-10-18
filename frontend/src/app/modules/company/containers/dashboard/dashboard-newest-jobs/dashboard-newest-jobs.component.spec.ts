import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardNewestJobsComponent } from './dashboard-newest-jobs.component';

describe('DashboardNewestJobsComponent', () => {
  let component: DashboardNewestJobsComponent;
  let fixture: ComponentFixture<DashboardNewestJobsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DashboardNewestJobsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardNewestJobsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
