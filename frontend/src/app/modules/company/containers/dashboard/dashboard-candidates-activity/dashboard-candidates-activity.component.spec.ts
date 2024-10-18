import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardCandidatesActivityComponent } from './dashboard-candidates-activity.component';

describe('DashboardCandidatesActivityComponent', () => {
  let component: DashboardCandidatesActivityComponent;
  let fixture: ComponentFixture<DashboardCandidatesActivityComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DashboardCandidatesActivityComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardCandidatesActivityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
