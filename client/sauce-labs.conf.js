'use strict';

var common = require('./common');

// Browsers to run on Sauce Labs
var customLaunchers = {
  'sl_win7_chrome': {
    base: 'SauceLabs',
    platform: 'Windows 7',
    browserName: 'chrome'
  },
  'sl_win7_firefox': {
    base: 'SauceLabs',
    platform: 'Windows 7',
    browserName: 'firefox'
  },
  'sl_win7_ie8': {
    base: 'SauceLabs',
    platform: 'Windows 7',
    browserName: 'internet explorer',
    version: '8'
  },
  'sl_win7_ie9': {
    base: 'SauceLabs',
    platform: 'Windows 7',
    browserName: 'internet explorer',
    version: '9'
  },
  'sl_win7_ie10': {
    base: 'SauceLabs',
    platform: 'Windows 7',
    browserName: 'internet explorer',
    version: '10'
  },
  'sl_win7_ie11': {
    base: 'SauceLabs',
    platform: 'Windows 7',
    browserName: 'internet explorer',
    version: '11'
  },
  // sl_ios_safari: {
  //   base: 'SauceLabs',
  //   platform: 'OS X 10.11',
  //   browserName: 'iphone'
  // },
  sl_osx_safari: {
    base: 'SauceLabs',
    platform: 'OS X 10.11',
    browserName: 'safari'
  }
};

module.exports = function(config) {
  config.set({
    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',

    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],

    // list of files / patterns to load in the browser
    files: []
      .concat(common.JS_VENDOR)
      .concat(common.JS_IE)
      .concat(common.JS)
      .concat(common.JS_TESTS),

    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['dots', 'saucelabs'],

    // web server port
    port: 9876,

    // enable / disable colors in the output (reporters and logs)
    colors: true,

    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,

    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: Object.keys(customLaunchers),

    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: true,

    sauceLabs: {
      testName: 'Radar Unit Tests',
      recordScreenshots: false
    },
    customLaunchers: customLaunchers,
    captureTimeout: 120000
  });
};
