import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LastViewItemComponent } from './last-view-item.component';

describe('LastViewItemComponent', () => {
  let component: LastViewItemComponent;
  let fixture: ComponentFixture<LastViewItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LastViewItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LastViewItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
