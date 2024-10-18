import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CandidatesQuickListComponent } from './candidates-quick-list.component';

describe('CandidatesQuickListComponent', () => {
  let component: CandidatesQuickListComponent;
  let fixture: ComponentFixture<CandidatesQuickListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CandidatesQuickListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CandidatesQuickListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
