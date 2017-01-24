var gulp = require('gulp'),
    rename = require('gulp-rename'),
    minify = require('gulp-cssnano');

gulp.task('static', function () {
    return gulp.src(['./content/static/*.css', '!./content/static/*min.css'])
        .pipe(minify())
        .pipe(rename({
            extname: '.min.css'
        }))
        .pipe(gulp.dest('./content/static'));
});


gulp.task('default', ['static']);
