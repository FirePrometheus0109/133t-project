import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewDeletedCommentComponent } from './view-deleted-comment.component';

describe('ViewDeletedCommentComponent', () => {
  let component: ViewDeletedCommentComponent;
  let fixture: ComponentFixture<ViewDeletedCommentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ViewDeletedCommentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewDeletedCommentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
