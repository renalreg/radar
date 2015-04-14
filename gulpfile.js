var gulp = require('gulp'),
    sass = require('gulp-sass'),
    bower = require('gulp-bower'),
    uglify = require('gulp-uglify');

var config = {
    bower: 'bower_components',
    bootstrap: 'bower_components/bootstrap-sass',
    static: 'radar/static'
};

gulp.task('bower', function() { 
    return bower().pipe(gulp.dest(config.bower)) 
});

gulp.task('css', function() {
    return gulp.src(
        'sass/style.scss'
    )
    .pipe(sass({
        includePaths: [config.bootstrap + '/assets/stylesheets']
    }))
    .pipe(gulp.dest(config.static + '/css'));
});

gulp.task('js', function() {
    return gulp.src([
        config.bower + '/jquery/dist/jquery.js',
        config.bower + '/bootstrap-sass/assets/javascripts/bootstrap.js'
    ])
    .pipe(uglify())
    .pipe(gulp.dest(config.static + '/js'));
});

gulp.task('fonts', function() {
    return gulp.src(
        config.bootstrap + '/assets/fonts/**/*'
    )
    .pipe(gulp.dest(config.static + '/fonts'));
});

gulp.task('watch', function() {
    gulp.watch('sass/**/*.scss', ['css']);
});

gulp.task('default', ['bower', 'css', 'js', 'fonts']);