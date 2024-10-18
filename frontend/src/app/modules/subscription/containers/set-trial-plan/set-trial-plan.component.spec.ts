import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SetTrialPlanComponent } from './set-trial-plan.component';

describe('SetTrialPlanComponent', () => {
  let component: SetTrialPlanComponent;
  let fixture: ComponentFixture<SetTrialPlanComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SetTrialPlanComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SetTrialPlanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
