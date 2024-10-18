import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CandidateActivityItemComponent } from './candidate-activity-item.component';

describe('CandidateActivityItemComponent', () => {
  let component: CandidateActivityItemComponent;
  let fixture: ComponentFixture<CandidateActivityItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CandidateActivityItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CandidateActivityItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
