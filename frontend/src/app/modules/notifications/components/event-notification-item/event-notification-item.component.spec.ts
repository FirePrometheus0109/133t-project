import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventNotificationItemComponent } from './event-notification-item.component';

describe('EventNotificationItemComponent', () => {
  let component: EventNotificationItemComponent;
  let fixture: ComponentFixture<EventNotificationItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventNotificationItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventNotificationItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
