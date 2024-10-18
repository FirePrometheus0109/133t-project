import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LetterTemplateViewComponent } from './letter-template-view.component';

describe('LetterTemplateViewComponent', () => {
  let component: LetterTemplateViewComponent;
  let fixture: ComponentFixture<LetterTemplateViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LetterTemplateViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LetterTemplateViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
