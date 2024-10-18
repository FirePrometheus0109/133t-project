import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationSelectFilterComponent } from './location-select-filter.component';

describe('LocationSelectFilterComponent', () => {
  let component: LocationSelectFilterComponent;
  let fixture: ComponentFixture<LocationSelectFilterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LocationSelectFilterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LocationSelectFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
