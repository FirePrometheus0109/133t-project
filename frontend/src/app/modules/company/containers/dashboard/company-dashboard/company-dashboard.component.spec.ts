import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CompanyDashboardComponent } from './company-dashboard.component';

describe('CompanyDashboardComponent', () => {
  let component: CompanyDashboardComponent;
  let fixture: ComponentFixture<CompanyDashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CompanyDashboardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CompanyDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
