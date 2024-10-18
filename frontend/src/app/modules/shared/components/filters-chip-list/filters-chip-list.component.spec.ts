import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FiltersChipListComponent } from './filters-chip-list.component';

describe('FiltersChipListComponent', () => {
  let component: FiltersChipListComponent;
  let fixture: ComponentFixture<FiltersChipListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FiltersChipListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FiltersChipListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
