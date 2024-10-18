import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchListFormComponent } from './search-list-form.component';

describe('SearchListFormComponent', () => {
  let component: SearchListFormComponent;
  let fixture: ComponentFixture<SearchListFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchListFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchListFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
