import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SetSubscriptionPanelComponent } from './set-subscription-panel.component';

describe('SetSubscriptionPanelComponent', () => {
  let component: SetSubscriptionPanelComponent;
  let fixture: ComponentFixture<SetSubscriptionPanelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SetSubscriptionPanelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SetSubscriptionPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
