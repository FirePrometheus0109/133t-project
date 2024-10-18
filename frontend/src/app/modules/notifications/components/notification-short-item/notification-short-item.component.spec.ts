import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NotificationShortItemComponent } from './notification-short-item.component';

describe('NotificationShortItemComponent', () => {
  let component: NotificationShortItemComponent;
  let fixture: ComponentFixture<NotificationShortItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NotificationShortItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NotificationShortItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
