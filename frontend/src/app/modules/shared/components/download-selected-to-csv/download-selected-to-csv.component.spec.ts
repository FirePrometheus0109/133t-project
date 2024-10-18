import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloadSelectedToCSVComponent } from './download-selected-to-csv.component';

describe('DownloadSelectedToCSVComponent', () => {
  let component: DownloadSelectedToCSVComponent;
  let fixture: ComponentFixture<DownloadSelectedToCSVComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DownloadSelectedToCSVComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloadSelectedToCSVComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
