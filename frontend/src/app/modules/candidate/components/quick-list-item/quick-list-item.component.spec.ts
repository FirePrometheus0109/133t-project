import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { QuickListItemComponent } from './quick-list-item.component';

describe('QuickListItemComponent', () => {
  let component: QuickListItemComponent;
  let fixture: ComponentFixture<QuickListItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ QuickListItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QuickListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
