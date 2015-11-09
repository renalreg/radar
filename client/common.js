var JS = [
  'src/app/**/*.module.js',
  'src/app/!(*.spec).js',
  'src/app/!(config)/**/!(*.spec).js'
];

var JS_TESTS = [
  'bower_components/angular-mocks/angular-mocks.js',
  'src/app/**/*.spec.js'
];

var JS_VENDOR = [
  'bower_components/es5-shim/es5-shim.js',
  'bower_components/es5-shim/es5-sham.js',
  'bower_components/jquery/dist/jquery.js',
  'bower_components/jquery-ui/jquery-ui.js',
  'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
  'bower_components/lodash/lodash.js',
  'bower_components/moment/moment.js',
  'bower_components/angular/angular.js',
  'bower_components/ui-router/release/angular-ui-router.js',
  'bower_components/blueimp-md5/js/md5.js',
  'bower_components/highcharts/highcharts.js',
  'bower_components/angular-local-storage/dist/angular-local-storage.js',
  'bower_components/tinymce/tinymce.js',
  'bower_components/zxcvbn/dist/zxcvbn.js'
];

var JS_IE = [
  'bower_components/html5shiv/dist/html5shiv.js',
  'bower_components/respond/dest/respond.src.js'
];

var CSS_VENDOR = [
  'bower_components/jquery-ui/themes/smoothness/jquery-ui.css',
  'bower_components/font-awesome/css/font-awesome.css'
];

var FONTS_VENDOR = [
  'bower_components/bootstrap-sass/**/*.{eot,svg,ttf,woff,woff2}',
  'bower_components/font-awesome/fonts/*.{otf,eot,svg,ttf,woff,woff2}'
];

var IMAGES = [
  'src/images/**/*',
  'bower_components/jquery-ui/themes/smoothness/images/*.{gif,png}'
];

module.exports = {
  JS: JS,
  JS_TESTS: JS_TESTS,
  JS_VENDOR: JS_VENDOR,
  JS_IE: JS_IE,
  CSS_VENDOR: CSS_VENDOR,
  FONTS_VENDOR: FONTS_VENDOR,
  IMAGES: IMAGES
};
