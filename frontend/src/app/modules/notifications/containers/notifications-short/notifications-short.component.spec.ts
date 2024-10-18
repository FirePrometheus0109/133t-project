import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NotificationsShortComponent } from './notifications-short.component';

describe('NotificationsShortComponent', () => {
  let component: NotificationsShortComponent;
  let fixture: ComponentFixture<NotificationsShortComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NotificationsShortComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NotificationsShortComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
