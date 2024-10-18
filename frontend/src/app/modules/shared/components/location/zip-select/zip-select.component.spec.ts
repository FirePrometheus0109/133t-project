import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ZipSelectComponent } from './zip-select.component';

describe('ZipSelectComponent', () => {
  let component: ZipSelectComponent;
  let fixture: ComponentFixture<ZipSelectComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ZipSelectComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ZipSelectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
