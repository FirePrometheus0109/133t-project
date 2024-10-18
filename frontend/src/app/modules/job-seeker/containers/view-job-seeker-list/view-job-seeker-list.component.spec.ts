import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewJobSeekerListComponent } from './view-job-seeker-list.component';

describe('ViewJobSeekerListComponent', () => {
  let component: ViewJobSeekerListComponent;
  let fixture: ComponentFixture<ViewJobSeekerListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ViewJobSeekerListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewJobSeekerListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
