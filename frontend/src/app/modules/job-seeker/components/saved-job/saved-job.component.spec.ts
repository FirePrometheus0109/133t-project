import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SavedJobComponent } from './saved-job.component';

describe('SavedJobComponent', () => {
  let component: SavedJobComponent;
  let fixture: ComponentFixture<SavedJobComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SavedJobComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SavedJobComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
