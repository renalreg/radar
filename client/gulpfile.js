var gulp = require('gulp');
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var size = require('gulp-size');
var imagemin = require('gulp-imagemin');
var ngAnnotate = require('gulp-ng-annotate');
var jshint = require('gulp-jshint');
var gulpif = require('gulp-if');
var templateCache = require('gulp-angular-templatecache');
var minifyHtml = require('gulp-minify-html');
var minifyCss = require('gulp-minify-css');
var sass = require('gulp-sass');

var del = require('del');
var runSequence = require('run-sequence');
var browserSync = require('browser-sync').create();

var paths = {
	scripts: [
		'app/app.module.js',
		'app/**/*.js'
	],
	images: 'img/**/*',
	index: 'index.html',
	templates: 'app/**/*.html',
	sass: 'sass/**/*.scss',
	vendor: {
		scripts: [
			'bower_components/jquery/dist/jquery.js',
			'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
			'bower_components/angular/angular.js'
		],
		fonts: [
			'bower_components/bootstrap-sass/assets/fonts/bootstrap/*'
		],
	}
};

gulp.task('clean', function(cb) {
	del(['build'], cb);
});

gulp.task('scripts', function() {
	return gulp.src(paths.scripts)
		.pipe(sourcemaps.init())
		.pipe(ngAnnotate())
		.pipe(uglify())
		.pipe(concat('app.min.js'))
		.pipe(sourcemaps.write('.'))
		.pipe(size({title: 'scripts'}))
		.pipe(gulp.dest('build/js'));
});

gulp.task('jshint', function() {
	return gulp.src(paths.scripts)
		.pipe(jshint())
		.pipe(jshint.reporter('jshint-stylish'))
		.pipe(gulpif(browserSync.active, jshint.reporter('fail')));
});

gulp.task('sass', function() {
    return gulp.src(paths.sass)
		.pipe(sourcemaps.init())
		.pipe(sass({
			includePaths: ['bower_components/bootstrap-sass/assets/stylesheets']
		}))
		.pipe(concat('style.min.css'))
		.pipe(minifyCss())
		.pipe(sourcemaps.write('.'))
		.pipe(gulp.dest('build/css'));
});

gulp.task('templates', function() {
	return gulp.src(paths.templates)
		.pipe(minifyHtml({conditionals: true}))
		.pipe(templateCache({
			'module': 'radar',
			'filename': 'app.templates.min.js'
		}))
		.pipe(uglify())
		.pipe(size({'title': 'templates'}))
		.pipe(gulp.dest('build/js'));
});

gulp.task('vendor', ['vendor:scripts', 'vendor:fonts']);

gulp.task('vendor:scripts', function() {
	return gulp.src(paths.vendor.scripts)
		.pipe(uglify())
		.pipe(concat('vendor.min.js'))
		.pipe(size({title: 'vendor:scripts'}))
		.pipe(gulp.dest('build/js'));
});

gulp.task('vendor:fonts', function() {
	return gulp.src(paths.vendor.fonts)
		.pipe(size({title: 'vendor:fonts'}))
		.pipe(gulp.dest('build/fonts'));
});

gulp.task('images', function() {
	return gulp.src(paths.images)
		.pipe(imagemin({optimizationLevel: 5}))
		.pipe(size({title: 'images'}))
		.pipe(gulp.dest('build/img'));
});

gulp.task('index', function() {
	return gulp.src(paths.index)
		.pipe(size({title: 'index'}))
		.pipe(gulp.dest('build'));
});

gulp.task('build', function(cb) {
	runSequence(
		'clean',
		['scripts', 'jshint', 'sass', 'images', 'index', 'templates', 'vendor'],
		cb
	);
});

gulp.task('serve', ['build'], function() {
	browserSync.init({
		server: {
			baseDir: 'build'
		}
	});

	gulp.watch(paths.scripts, ['scripts', 'jshint', browserSync.reload]);
	gulp.watch(paths.sass, ['sass', browserSync.reload]);
	gulp.watch(paths.images, ['images', browserSync.reload]);
	gulp.watch(paths.index, ['index', browserSync.reload]);
	gulp.watch(paths.templates, ['templates', browserSync.reload]);
	gulp.watch(paths.vendor.scripts, ['vendor:scripts', browserSync.reload]);
	gulp.watch(paths.vendor.fonts, ['vendor:fonts', browserSync.reload]);
});

gulp.task('default', ['serve']);