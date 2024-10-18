import {DEFAULT_SETTINGS} from './index';

beforeEach(function () {

  let store = {};

  spyOn(localStorage, 'getItem').and.callFake((key: string): String => {
    return store[key] || null;
  });
  spyOn(localStorage, 'removeItem').and.callFake((key: string): void => {
    delete store[key];
  });
  spyOn(localStorage, 'setItem').and.callFake((key: string, value: string): string => {
    return store[key] = <string>value;
  });
  spyOn(localStorage, 'clear').and.callFake(() => {
    store = {};
  });

  localStorage.clear();
  localStorage.setItem('settings', JSON.stringify(DEFAULT_SETTINGS));

});
