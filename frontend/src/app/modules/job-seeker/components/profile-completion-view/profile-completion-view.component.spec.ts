import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileCompletionViewComponent } from './profile-completion-view.component';

describe('ProfileCompletionViewComponent', () => {
  let component: ProfileCompletionViewComponent;
  let fixture: ComponentFixture<ProfileCompletionViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProfileCompletionViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileCompletionViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
