import {AutoApplyModule} from './auto-apply.module';

describe('AutoApplyModule', () => {
  let autoApplyModule: AutoApplyModule;

  beforeEach(() => {
    autoApplyModule = new AutoApplyModule();
  });

  it('should create an instance', () => {
    expect(autoApplyModule).toBeTruthy();
  });
});
