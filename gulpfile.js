var gulp = require('gulp'),
    rename = require('gulp-rename'),
    minify = require('gulp-cssnano');

gulp.task('static', function () {
    return gulp.src(['./content/static/css/*.css', '!./content/static/css/*min.css'])
        .pipe(minify())
        .pipe(rename({
            extname: '.min.css'
        }))
        .pipe(gulp.dest('./content/static/css'));
});


gulp.task('default', ['static']);
