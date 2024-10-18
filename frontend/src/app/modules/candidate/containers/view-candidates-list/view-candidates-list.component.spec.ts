import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewCandidatesListComponent } from './view-candidates-list.component';

describe('ViewCandidatesListComponent', () => {
  let component: ViewCandidatesListComponent;
  let fixture: ComponentFixture<ViewCandidatesListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ViewCandidatesListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewCandidatesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
