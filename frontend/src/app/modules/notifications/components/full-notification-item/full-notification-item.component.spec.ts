import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FullNotificationItemComponent } from './full-notification-item.component';

describe('FullNotificationItemComponent', () => {
  let component: FullNotificationItemComponent;
  let fixture: ComponentFixture<FullNotificationItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FullNotificationItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FullNotificationItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
