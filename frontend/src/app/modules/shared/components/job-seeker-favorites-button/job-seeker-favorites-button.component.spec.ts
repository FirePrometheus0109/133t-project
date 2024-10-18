import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerFavoritesButtonComponent } from './job-seeker-favorites-button.component';

describe('JobSeekerFavoritesButtonComponent', () => {
  let component: JobSeekerFavoritesButtonComponent;
  let fixture: ComponentFixture<JobSeekerFavoritesButtonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobSeekerFavoritesButtonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobSeekerFavoritesButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
