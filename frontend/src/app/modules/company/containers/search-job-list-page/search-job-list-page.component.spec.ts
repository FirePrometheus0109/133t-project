import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchJobListPageComponent } from './search-job-list-page.component';

describe('SearchJobListPageComponent', () => {
  let component: SearchJobListPageComponent;
  let fixture: ComponentFixture<SearchJobListPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchJobListPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchJobListPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
