import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LetterTemplateFromComponent } from './letter-template-from.component';

describe('LetterTemplateFromComponent', () => {
  let component: LetterTemplateFromComponent;
  let fixture: ComponentFixture<LetterTemplateFromComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LetterTemplateFromComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LetterTemplateFromComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
