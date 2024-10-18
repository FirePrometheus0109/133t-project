import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowStatsWidgetComponent } from './workflow-stats-widget.component';

describe('WorkflowStatsWidgetComponent', () => {
  let component: WorkflowStatsWidgetComponent;
  let fixture: ComponentFixture<WorkflowStatsWidgetComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WorkflowStatsWidgetComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WorkflowStatsWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
