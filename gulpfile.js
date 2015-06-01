var gulp = require('gulp');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var gulpFilter = require('gulp-filter');
var mainBowerFiles = require('main-bower-files');
var rename = require('gulp-rename');
var flatten = require('gulp-flatten');
var minifycss = require('gulp-minify-css');
var replace = require('gulp-replace');

var config = {
    bower: 'bower_components',
    bootstrap: 'bower_components/bootstrap-sass',
    static: 'radar/web/static'
};

gulp.task('libs', function() { 
    var jsFilter = gulpFilter('*.js');
    var cssFilter = gulpFilter('*.css');
    var fontFilter = gulpFilter(['*.eot', '*.woff', '*.woff2', '*.svg', '*.ttf']);
    var imgFilter = gulpFilter(['*.png', '*.gif']);

    var jsDest = config.static + '/libs/js';
    var cssDest = config.static + '/libs/css';
    var fontDest = config.static + '/libs/fonts';
    var imgDest = config.static + '/libs/img';

    return gulp.src(mainBowerFiles().concat([
        config.bower + '/jquery-ui/themes/smoothness/jquery-ui.css',
        config.bower + '/jquery-ui/themes/smoothness/images/*.png',
        config.bower + '/jquery-ui/themes/smoothness/images/*.gif',
        config.bower + '/chosen/chosen.min.css',
        config.bower + '/chosen/chosen-sprite.png',
        config.bower + '/chosen/chosen-sprite@2x.png',
        config.bower + '/bootstrap-sortable/Contents/bootstrap-sortable.css',
    ]))

    /*
    JavaScript
    */

    .pipe(jsFilter)
    .pipe(gulp.dest(jsDest))

    // Minification
    //.pipe(uglify())
    //.pipe(rename({
    //    suffix: '.min'
    //}))
    //.pipe(gulp.dest(jsDest))

    .pipe(jsFilter.restore())

    /* CSS */

    .pipe(cssFilter)

    // Rewrite Chosen image paths
    .pipe(replace('url(chosen-sprite.png)', 'url(../img/chosen-sprite.png)'))
    .pipe(replace('url(chosen-sprite@2x.png)', 'url(../img/chosen-sprite@2x.png)'))

    // Rewrite smoothness image paths
    .pipe(replace('url("images/', 'url("../img/'))

    .pipe(gulp.dest(cssDest))

    // Minification
    //.pipe(minifycss())
    //.pipe(rename({
    //    suffix: '.min'
    //}))
    //.pipe(gulp.dest(cssDest))

    .pipe(cssFilter.restore())

    /*
    Fonts
    */

    .pipe(fontFilter)
    .pipe(flatten())
    .pipe(gulp.dest(fontDest))
    .pipe(fontFilter.restore())

    /*
    Images
    */

    .pipe(imgFilter)
    .pipe(gulp.dest(imgDest));
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