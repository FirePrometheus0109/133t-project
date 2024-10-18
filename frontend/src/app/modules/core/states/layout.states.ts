import { Action, Selector, State, StateContext } from '@ngxs/store';
import { LayoutActions } from '../actions';


export class LayoutStateModel {
  showSidenav: boolean;
}


@State<LayoutStateModel>({
  name: 'layout',
  defaults: {
    showSidenav: false,
  },
})
export class LayoutState {
  @Selector()
  static showSidenav(state: LayoutStateModel) {
    return state.showSidenav;
  }

  @Action(LayoutActions.OpenSidenav)
  openSidenav(ctx: StateContext<LayoutStateModel>) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      showSidenav: true,
    });
  }

  @Action(LayoutActions.CloseSidenav)
  closeSidenav(ctx: StateContext<LayoutStateModel>) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      showSidenav: false,
    });
  }
}
