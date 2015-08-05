'use strict';

var gulp = require('gulp');
var uglify = require('gulp-uglify');
var size = require('gulp-size');
var imagemin = require('gulp-imagemin');
var ngAnnotate = require('gulp-ng-annotate');
var jshint = require('gulp-jshint');
var gulpIf = require('gulp-if');
var templateCache = require('gulp-angular-templatecache');
var minifyHtml = require('gulp-minify-html');
var minifyCss = require('gulp-minify-css');
var sass = require('gulp-sass');
var inject = require('gulp-inject');
var flatten = require('gulp-flatten');
var useref = require('gulp-useref');
var rev = require('gulp-rev');
var revReplace = require('gulp-rev-replace');
var gulpFilter = require('gulp-filter');
var replace = require('gulp-replace');
var jscs = require('gulp-jscs');
var gutil = require('gulp-util');

var del = require('del');
var runSequence = require('run-sequence');
var browserSync = require('browser-sync').create();

//var argv = require('yargs').argv;
//var environment = argv.environment || 'development';

var paths = {
  vendorJs: [
    'bower_components/es5-shim/es5-shim.js',
    'bower_components/jquery/dist/jquery.js',
    'bower_components/jquery-ui/jquery-ui.js',
    'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
    'bower_components/angular/angular.js',
    'bower_components/lodash/lodash.js',
    'bower_components/restangular/src/restangular.js',
    'bower_components/ui-router/release/angular-ui-router.js',
    'bower_components/humps/humps.js',
    'bower_components/angular-ui-grid/ui-grid.js',
    'bower_components/angular-resource/angular-resource.js',
    'bower_components/moment/moment.js'
  ],
  vendorCss: [
    'bower_components/angular-ui-grid/ui-grid.css',
    'bower_components/jquery-ui/themes/smoothness/jquery-ui.css'
  ],
  ieJs: [
    'bower_components/html5shiv/dist/html5shiv.js',
    'bower_components/respond/dest/respond.src.js'
  ]
};

gulp.task('clean', function(cb) {
  del(['dist', '.tmp'], cb);
});

gulp.task('inject', ['sass', 'scripts'], function() {
  var appStyles = gulp.src('.tmp/serve/css/**/*.css', {read: false});

  var appScripts = gulp.src(
    ['src/app/**/*.module.js', 'src/app/**/*.js'],
    {read: false}
  );

  var vendorScripts = gulp.src(paths.vendorJs, {read: false});

  var vendorStyles = gulp.src(paths.vendorCss, {read: false});

  var ieScripts = gulp.src(paths.ieJs, {read: false});

  return gulp.src('src/index.html')
    .pipe(inject(appStyles, {name: 'app', ignorePath: ['src', '.tmp/serve']}))
    .pipe(inject(appScripts, {name: 'app', ignorePath: ['src', '.tmp/serve']}))
    .pipe(inject(vendorScripts, {name: 'vendor'}))
    .pipe(inject(vendorStyles, {name: 'vendor'}))
    .pipe(inject(ieScripts, {name: 'ie'}))
    .pipe(gulp.dest('.tmp/serve'))
    .pipe(browserSync.reload({stream: true}));
});

gulp.task('sass', function() {
  return gulp.src('src/sass/**/*.scss')
    .pipe(sass({
      includePaths: ['bower_components/bootstrap-sass/assets/stylesheets'],
      style: 'expanded'
    }))
    .pipe(gulp.dest('.tmp/serve/css'))
    .pipe(browserSync.reload({stream: true}));
});

gulp.task('scripts', function() {
  return gulp.src('src/app/**/*.js')
    .pipe(jscs().on('error', gutil.log))
		.pipe(jshint())
		.pipe(jshint.reporter('jshint-stylish'))
		// TODO .pipe(gulpIf(!browserSync.active, jshint.reporter('fail')))
    .pipe(browserSync.reload({stream: true}));
});

gulp.task('dist', function(cb) {
  runSequence(
    'clean',
    ['html', 'fonts', 'images'],
    'dist:size',
    cb
  );
});

gulp.task('html', ['inject', 'templates'], function() {
  var templates = gulp.src('.tmp/templates/*.js', {read: false});

  var assets = useref.assets();

  var jsFilter = gulpFilter('**/*.js', {restore: true});
  var cssFilter = gulpFilter('**/*.css', {restore: true});
  var htmlFilter = gulpFilter('*.html', {restore: true});

  return gulp.src('.tmp/serve/index.html')
    .pipe(inject(templates, {name: 'templates', ignorePath: '.tmp/templates'}))
    .pipe(assets)
    .pipe(rev())
    .pipe(jsFilter)
    .pipe(ngAnnotate())
    .pipe(uglify())
    .pipe(jsFilter.restore)
    .pipe(cssFilter)
    .pipe(replace('/bower_components/bootstrap-sass/assets/fonts/bootstrap/', '../fonts/'))
    .pipe(minifyCss())
    .pipe(cssFilter.restore)
    .pipe(assets.restore())
    .pipe(useref())
    .pipe(revReplace())
    .pipe(htmlFilter)
    .pipe(minifyHtml({
      empty: true,
      spare: true,
      quotes: true,
      conditionals: true
    }))
    .pipe(htmlFilter.restore)
    .pipe(gulp.dest('dist'));
});

gulp.task('templates', function() {
  return gulp.src('src/app/**/*.html')
    .pipe(minifyHtml({
      empty: true,
      spare: true,
      quotes: true,
      conditionals: true
    }))
    .pipe(templateCache({
      root: 'app/',
      module: 'radar',
      filename: 'templates.js'
    }))
    .pipe(gulp.dest('.tmp/templates'));
});

gulp.task('fonts', function() {
  return gulp.src('bower_components/bootstrap-sass/**/*.{eot,svg,ttf,woff,woff2}')
    .pipe(flatten())
    .pipe(gulp.dest('dist/fonts'));
});

gulp.task('images', function() {
  return gulp.src('src/images/**/*')
    .pipe(imagemin({optimizationLevel: 5}))
    .pipe(gulp.dest('dist/images'));
});

gulp.task('dist:size', function() {
  return gulp.src('dist/**/*')
    .pipe(size({title: 'dist', gzip: 'true', showFiles: true}));
});

gulp.task('watch', ['inject'], function() {
  gulp.watch('src/app/**/*.js', function(event) {
    if (event.type === 'changed') {
      gulp.start('scripts');
    } else {
      gulp.start('inject');
    }
  });

  gulp.watch('src/app/**/*.html', function(event) {
    browserSync.reload(event.path);
  });

  gulp.watch('src/sass/**/*.scss', function(event) {
    if (event.type === 'changed') {
      gulp.start('sass');
    } else {
      gulp.start('inject');
    }
  });

  gulp.watch('src/index.html', ['inject']);
});

gulp.task('serve', ['watch'], function() {
  browserSync.init({
    server: {
      baseDir: ['.tmp/serve', 'src'],
      routes: {
        '/bower_components': 'bower_components'
      }
    },
    open: false
  });
});

gulp.task('serve:dist', ['dist'], function() {
  browserSync.init({
    server: {
      baseDir: 'dist'
    },
    open: false
  });
});

gulp.task('default', ['serve']);
