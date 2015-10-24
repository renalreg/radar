'use strict';

var gulp = require('gulp');
var uglify = require('gulp-uglify');
var size = require('gulp-size');
var imagemin = require('gulp-imagemin');
var jshint = require('gulp-jshint');
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
var express = require('express');
var del = require('del');
var runSequence = require('run-sequence');
var browserSync = require('browser-sync').create();
var argv = require('yargs').argv;
var stylish = require('gulp-jscs-stylish');

var common = require('./common');

var config = argv.config || 'production';
console.log('config: ' + config + ' (--config NAME)');

gulp.task('clean', function() {
  return del(['dist', '.tmp']);
});

gulp.task('inject', ['sass', 'scripts'], function() {
  var appStyles = gulp.src('.tmp/serve/css/**/*.css', {read: false});
  var appScripts = gulp.src(common.JS, {read: false});
  var configScript = gulp.src('src/app/config/' + config + '.js');
  var vendorScripts = gulp.src(common.JS_VENDOR, {read: false});
  var vendorStyles = gulp.src(common.CSS_VENDOR, {read: false});
  var ieScripts = gulp.src(common.JS_IE, {read: false});

  return gulp.src('src/index.html')
    .pipe(inject(appStyles, {name: 'app', ignorePath: ['src', '.tmp/serve']}))
    .pipe(inject(appScripts, {name: 'app', ignorePath: ['src', '.tmp/serve']}))
    .pipe(inject(configScript, {name: 'config', ignorePath: ['src']}))
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
    .pipe(jshint())
    .pipe(jscs())
    .on('error', function() {}) // continue despite linting errors
    .pipe(stylish.combineWithHintResults())
    .pipe(jshint.reporter('jshint-stylish'))
    .pipe(browserSync.reload({stream: true}));
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
    .pipe(uglify())
    .pipe(jsFilter.restore)
    .pipe(cssFilter)
    .pipe(replace('/bower_components/bootstrap-sass/assets/fonts/bootstrap/', '../fonts/'))
    .pipe(replace('"images/', '"../images/'))
    .pipe(minifyCss({compatibility: 'ie8'}))
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
  return gulp.src(common.FONTS_VENDOR)
    .pipe(flatten())
    .pipe(gulp.dest('dist/fonts'));
});

gulp.task('images', function() {
  return gulp.src(common.IMAGES)
    .pipe(imagemin({optimizationLevel: 3}))
    .pipe(gulp.dest('dist/images'));
});

gulp.task('size', function() {
  return gulp.src('dist/**/*')
    .pipe(size({showFiles: true}));
});

// TODO watch:dist
gulp.task('watch', function() {
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

gulp.task('browser-sync', function() {
  browserSync.init({
    proxy: 'http://localhost:8082',
    open: false
  });
});

gulp.task('express', function () {
  var app = express();

  app.use(express.static('.tmp/serve'));
  app.use(express.static('src'));
  app.use('/bower_components', express.static('bower_components'));

  app.get('/', function(req, res) {
    res.sendFile('.tmp/serve/index.html');
  });

  app.listen(8082);
});

gulp.task('express:dist', function () {
  var app = express();

  app.use(express.static('dist'));

  app.get('/', function(req, res) {
    res.sendFile('dist/index.html');
  });

  app.listen(8081);
});

gulp.task('build', function(cb) {
  runSequence('inject', cb);
});

gulp.task('build:dist', function(cb) {
  runSequence(
    'clean',
    ['html', 'fonts', 'images'],
    'size',
    cb
  );
});

gulp.task('serve', function(cb) {
  runSequence('build', ['watch', 'browser-sync', 'express'], cb);
});

gulp.task('serve:dist', function(cb) {
  runSequence('build:dist', 'express:dist', cb);
});

gulp.task('default', ['serve']);
