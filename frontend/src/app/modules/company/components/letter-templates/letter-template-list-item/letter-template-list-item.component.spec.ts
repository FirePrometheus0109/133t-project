import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LetterTemplateItemComponent } from './letter-template-list-item.component';

describe('LetterTemplateItemComponent', () => {
  let component: LetterTemplateItemComponent;
  let fixture: ComponentFixture<LetterTemplateItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LetterTemplateItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LetterTemplateItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
