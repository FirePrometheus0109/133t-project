import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JspSkillsViewComponent } from './jsp-skills-view.component';

describe('JspSkillsViewComponent', () => {
  let component: JspSkillsViewComponent;
  let fixture: ComponentFixture<JspSkillsViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JspSkillsViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JspSkillsViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
