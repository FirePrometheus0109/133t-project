import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ShareJobControlComponent } from './share-job-control.component';

describe('ShareJobControlComponent', () => {
  let component: ShareJobControlComponent;
  let fixture: ComponentFixture<ShareJobControlComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ShareJobControlComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ShareJobControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
