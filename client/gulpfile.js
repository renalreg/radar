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
var express = require('express');
var del = require('del');
var browserSync = require('browser-sync').create();
var argv = require('yargs').argv;
var stylish = require('gulp-jscs-stylish');
var karma = require('karma');
var gutil = require('gulp-util');

var common = require('./common');

var config = argv.config || 'production';
gutil.log('config: ' + config + ' (--config NAME)');

function noop() {}

gulp.task('clean', function() {
  return del(['dist', '.tmp']);
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
    .on('error', noop) // continue despite linting errors
    .pipe(stylish.combineWithHintResults())
    .pipe(jshint.reporter('jshint-stylish'))
    .pipe(browserSync.reload({stream: true}));
});

gulp.task('inject', function() {
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

gulp.task('html', function() {
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

gulp.task('build', gulp.series(gulp.parallel('scripts', 'sass'), 'inject'));

gulp.task('build:dist', gulp.series(
  'clean',
  gulp.parallel('scripts', 'sass', 'templates'),
  'inject',
  gulp.parallel('html', 'fonts', 'images'),
  'size'
));

gulp.task('reload', function(done) {
  browserSync.reload();
  done();
});

gulp.task('watch', function() {
  function watch(glob, opt, task) {
    return gulp.watch(glob, opt, task)
      .on('add', function(path) {
        gutil.log(gutil.colors.green('Added ' + path));
      })
      .on('change', function(path) {
        gutil.log(gutil.colors.yellow('Modified ' + path));
      })
      .on('unlink', function(path) {
        gutil.log(gutil.colors.red('Deleted ' + path));
      });
  }

  watch('src/app/**/*.js', gulp.series('scripts'))
    .on('add', gulp.series('inject'))
    .on('unlink', gulp.series('inject'));

  watch('src/sass/**/*.scss', gulp.series('sass'))
    .on('add', gulp.series('inject'))
    .on('unlink', gulp.series('inject'));

  watch('src/index.html', gulp.series('inject'));

  watch(['src/app/**/*.html', '!src/index.html'], gulp.series('reload'));
});

gulp.task('browser-sync', function() {
  browserSync.init({
    proxy: 'http://localhost:8082',
    open: false
  });
});

gulp.task('express', function() {
  var app = express();

  app.use(express.static('.tmp/serve'));
  app.use(express.static('src'));
  app.use('/bower_components', express.static('bower_components'));

  app.get('/', function(req, res) {
    res.sendFile('.tmp/serve/index.html');
  });

  app.listen(8082);
});

gulp.task('express:dist', function() {
  var app = express();

  app.use(express.static('dist'));

  app.get('/', function(req, res) {
    res.sendFile('dist/index.html');
  });

  app.listen(8081);
});

gulp.task('lint', function() {
  return gulp.src('src/app/**/*.js')
    .pipe(jshint())
    .pipe(jscs())
    .pipe(stylish.combineWithHintResults())
    .pipe(jshint.reporter('jshint-stylish'))
    .pipe(jshint.reporter('fail'));
});

gulp.task('test', function(cb) {
  new karma.Server({
    configFile: __dirname + '/karma.conf.js',
    singleRun: true,
    browsers: ['PhantomJS'],
    reporters: ['dots']
  }, cb).start();
});

gulp.task('coverage', function(cb) {
  new karma.Server({
    configFile: __dirname + '/karma.conf.js',
    singleRun: true,
    browsers: ['PhantomJS'],
    reporters: ['dots', 'coverage']
  }, cb).start();
});

gulp.task('sauce-labs', function(cb) {
  new karma.Server({
    configFile: __dirname + '/sauce-labs.conf.js',
    singleRun: true
  }, cb).start();
});

gulp.task('serve', gulp.series('build', gulp.parallel('watch', 'browser-sync', 'express')));

gulp.task('serve:dist', gulp.series('build:dist', 'express:dist'));

gulp.task('default', gulp.series('serve'));
