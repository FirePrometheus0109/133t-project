import { NestedTreeControl } from '@angular/cdk/tree';
import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { of } from 'rxjs';
import { CoreState } from '../../core/states/core.state';
import { Changelog, Version } from '../models/version.model';

const GetChildren = (node: Changelog) => of(node.children);
const TC = new NestedTreeControl(GetChildren);


@Component({
  selector: 'app-technical-info',
  template: `
    <span>Version: {{(version$ | async)?.version}}</span>
    <span>Date Release: {{(version$ | async)?.date | date}}</span>

    <h3>Changelog</h3>
    <mat-tree [dataSource]="changelog$ | async" [treeControl]="tc">
      <mat-tree-node *matTreeNodeDef="let node" matTreeNodeToggle>
        <li>
          <div>
            <button mat-icon-button disabled>
              <mat-icon>
                remove
              </mat-icon>
            </button>
            {{node.name}}
          </div>
        </li>
      </mat-tree-node>

      <mat-nested-tree-node *matTreeNodeDef="let node; when: hasChild">
        <li>
          <div class="mat-tree-node">
            <button mat-icon-button matTreeNodeToggle>
              <mat-icon>
                {{tc.isExpanded(node) ? 'expand_more' : 'chevron_right'}}
              </mat-icon>
            </button>
            {{node.name}}
          </div>
          <ul [hidden]="!tc.isExpanded(node)">
            <ng-container matTreeNodeOutlet></ng-container>
          </ul>
        </li>
      </mat-nested-tree-node>
    </mat-tree>
  `,
  styles: [],
})
export class VersionInfoComponent {
  @Select(CoreState.version) version$: Observable<Version>;
  @Select(CoreState.changelog) changelog$: Observable<Changelog>;

  tc = TC;

  hasChild(_: number, node: Changelog) {
    return node.children != null && node.children.length > 0;
  }

}
