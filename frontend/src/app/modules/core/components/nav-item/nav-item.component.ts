import { animate, state, style, transition, trigger } from '@angular/animations';
import { Component, HostBinding, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngxs/store';
import { CoreActions, LayoutActions } from '../../actions';
import { NavItem } from '../../models/nav-item';
import { NavigationService } from '../../services/navigation.service';


@Component({
  selector: 'app-nav-item',
  templateUrl: './nav-item.component.html',
  styleUrls: ['./nav-item.component.scss'],
  animations: [
    trigger('indicatorRotate', [
      state('collapsed', style({transform: 'rotate(0deg)'})),
      state('expanded', style({transform: 'rotate(180deg)'})),
      transition('expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4,0.0,0.2,1)')
      ),
    ])
  ]
})
export class NavItemComponent implements OnInit {
  @Input() depth: number;
  @Input() item: NavItem;

  expanded: boolean;

  @HostBinding('attr.aria-expanded') ariaExpanded = this.expanded;

  constructor(public navigationService: NavigationService,
              public router: Router,
              public store: Store) {
    if (this.depth === undefined) {
      this.depth = 0;
    }
  }

  ngOnInit() {
    this.navigationService.currentUrl.subscribe((url: string) => {
      if (this.item.children && url) {
        this.expanded = this.item.children.some((item: NavItem) => {
          return url === `/${item.routerLink}`;
        });
        this.ariaExpanded = this.expanded;
      }
    });
  }

  onItemSelected(item) {
    if (!item.children || !item.children.length) {
      this.store.dispatch(new LayoutActions.CloseSidenav());
      this.store.dispatch(new CoreActions.RedirectTo(item.routerLink));
    }
    if (item.children && item.children.length) {
      this.expanded = !this.expanded;
    }
  }
}
