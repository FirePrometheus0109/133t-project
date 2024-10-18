import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LetterTemplateManageComponent } from './letter-template-manage.component';

describe('LetterTemplateManageComponent', () => {
  let component: LetterTemplateManageComponent;
  let fixture: ComponentFixture<LetterTemplateManageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LetterTemplateManageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LetterTemplateManageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
