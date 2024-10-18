import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewPriceMarkerComponent } from './new-price-marker.component';

describe('NewPriceMarkerComponent', () => {
  let component: NewPriceMarkerComponent;
  let fixture: ComponentFixture<NewPriceMarkerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewPriceMarkerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewPriceMarkerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
