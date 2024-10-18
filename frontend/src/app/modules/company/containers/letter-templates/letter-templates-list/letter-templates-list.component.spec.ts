import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LetterTemplatesListComponent } from './letter-templates-list.component';

describe('LetterTemplatesListComponent', () => {
  let component: LetterTemplatesListComponent;
  let fixture: ComponentFixture<LetterTemplatesListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LetterTemplatesListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LetterTemplatesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
