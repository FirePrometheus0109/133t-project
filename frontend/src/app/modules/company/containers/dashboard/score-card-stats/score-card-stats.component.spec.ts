import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ScoreCardStatsComponent } from './score-card-stats.component';

describe('ScoreCardStatsComponent', () => {
  let component: ScoreCardStatsComponent;
  let fixture: ComponentFixture<ScoreCardStatsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ScoreCardStatsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ScoreCardStatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
