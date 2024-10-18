import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditJobPageComponent } from './edit-job-page.component';

describe('EditJobPageComponent', () => {
  let component: EditJobPageComponent;
  let fixture: ComponentFixture<EditJobPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditJobPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditJobPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
