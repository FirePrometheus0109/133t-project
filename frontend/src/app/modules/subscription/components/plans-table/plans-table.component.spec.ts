import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PlansTableComponent } from './plans-table.component';

describe('PlansTableComponent', () => {
  let component: PlansTableComponent;
  let fixture: ComponentFixture<PlansTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PlansTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlansTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
