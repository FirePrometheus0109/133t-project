import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CandidateStatisticPanelComponent } from './candidate-statistic-panel.component';

describe('CandidateStatisticPanelComponent', () => {
  let component: CandidateStatisticPanelComponent;
  let fixture: ComponentFixture<CandidateStatisticPanelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CandidateStatisticPanelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CandidateStatisticPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
