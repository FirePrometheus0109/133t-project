import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CompanyReportsGraphComponent } from './company-reports-graph.component';

describe('CompanyReportsGraphComponent', () => {
  let component: CompanyReportsGraphComponent;
  let fixture: ComponentFixture<CompanyReportsGraphComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CompanyReportsGraphComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CompanyReportsGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
