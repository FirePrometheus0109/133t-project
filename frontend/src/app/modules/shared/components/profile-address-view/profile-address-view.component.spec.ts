import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileAddressViewComponent } from './profile-address-view.component';

describe('ProfileAddressViewComponent', () => {
  let component: ProfileAddressViewComponent;
  let fixture: ComponentFixture<ProfileAddressViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProfileAddressViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileAddressViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
