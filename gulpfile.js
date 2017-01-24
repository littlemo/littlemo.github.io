var gulp = require('gulp'),
    rename = require('gulp-rename'),
    minify = require('gulp-cssnano');

gulp.task('extra', function () {
    return gulp.src(['./content/extra/*.css', '!./content/extra/*min.css'])
        .pipe(minify())
        .pipe(rename({
            extname: '.min.css'
        }))
        .pipe(gulp.dest('./content/extra'));
});


gulp.task('default', ['extra']);
