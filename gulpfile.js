var gulp = require('gulp');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var gulpFilter = require('gulp-filter');
var mainBowerFiles = require('main-bower-files');
var rename = require('gulp-rename');
var flatten = require('gulp-flatten');
var minifycss = require('gulp-minify-css');

var config = {
    bower: 'bower_components',
    bootstrap: 'bower_components/bootstrap-sass',
    static: 'radar/static'
};

gulp.task('libs', function() { 
    var jsFilter = gulpFilter('*.js');
    var cssFilter = gulpFilter('*.css');
    var fontFilter = gulpFilter(['*.eot', '*.woff', '*.svg', '*.ttf']);

    var jsDest = config.static + '/js/libs';
    var cssDest = config.static + '/css';
    var fontDest = config.static + '/fonts';

    return gulp.src(mainBowerFiles().concat([
        config.bower + '/jquery-ui/themes/smoothness/jquery-ui.css'
    ]))

    // JavaScript
    .pipe(jsFilter)
    .pipe(gulp.dest(jsDest))
    //.pipe(uglify())
    //.pipe(rename({
    //    suffix: '.min'
    //}))
    //.pipe(gulp.dest(jsDest))
    .pipe(jsFilter.restore())

    // CSS
    .pipe(cssFilter)
    .pipe(gulp.dest(cssDest))
    //.pipe(minifycss())
    //.pipe(rename({
    //    suffix: '.min'
    //}))
    //.pipe(gulp.dest(cssDest))
    .pipe(cssFilter.restore())

    // Fonts
    .pipe(fontFilter)
    .pipe(flatten())
    .pipe(gulp.dest(fontDest));
});

gulp.task('sass', function() {
    return gulp.src('radar/sass/**/*.scss')
    .pipe(sass({
        includePaths: [config.bootstrap + '/assets/stylesheets']
    }))
    .pipe(gulp.dest(config.static + '/css'));
});

gulp.task('watch', function() {
    gulp.watch('radar/sass/**/*.scss', ['sass']);
});

gulp.task('default', ['libs', 'sass']);