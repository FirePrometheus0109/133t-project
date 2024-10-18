import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AutocompleteMultiselectFilterComponent } from './autocomplete-multiselect-filter.component';

describe('AutocompleteMultiselectFilterComponent', () => {
  let component: AutocompleteMultiselectFilterComponent;
  let fixture: ComponentFixture<AutocompleteMultiselectFilterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AutocompleteMultiselectFilterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AutocompleteMultiselectFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
