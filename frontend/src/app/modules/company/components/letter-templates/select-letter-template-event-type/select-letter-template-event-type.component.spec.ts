import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectLetterTemplateEventTypeComponent } from './select-letter-template-event-type.component';

describe('SelectLetterTemplateEventTypeComponent', () => {
  let component: SelectLetterTemplateEventTypeComponent;
  let fixture: ComponentFixture<SelectLetterTemplateEventTypeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SelectLetterTemplateEventTypeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectLetterTemplateEventTypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
