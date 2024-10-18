// Karma configuration file, see link for more information
// https://karma-runner.github.io/1.0/config/configuration-file.html

module.exports = function (config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-chrome-launcher'),
      require('karma-jasmine-html-reporter'),
      require('karma-coverage-istanbul-reporter'),
      require('@angular-devkit/build-angular/plugins/karma'),
      require('karma-teamcity-reporter')
    ],
    browsers: ['ChromiumNoSandbox'], // You may use 'ChromeCanary', 'Chromium' or any other supported browser
    customLaunchers: {
      ChromiumNoSandbox: {
        base: 'ChromiumHeadless',
        flags: [
          '--no-sandbox', // required to run without privileges in docker
          '--headless',
          '--disable-gpu',
          '--disable-translate',
          '--disable-extensions'
        ]
      }
    },
    client:{
      clearContext: false // leave Jasmine Spec Runner output visible in browser
    },
    coverageIstanbulReporter: {
      reports: [ 'html', 'lcovonly', 'teamcity' ],
      fixWebpackSourcePaths: true
    },
    angularCli: {
      environment: 'dev'
    },
    reporters: config.angularCli && config.angularCli.codeCoverage
              ? ['progress', 'teamcity', 'coverage-istanbul']
              : ['progress', 'teamcity', 'kjhtml'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['ChromeHeadless'],
    singleRun: false,
    browserNoActivityTimeout: 60000
  });
};
