import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeletedJobViewComponent } from './deleted-job-view.component';

describe('DeletedJobViewComponent', () => {
  let component: DeletedJobViewComponent;
  let fixture: ComponentFixture<DeletedJobViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeletedJobViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeletedJobViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
