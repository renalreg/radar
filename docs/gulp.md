# Gulp

Gulp is used to build the RaDaR client (source code is in the `client` folder).
These notes refer to `client/gulpfile.js`. You should run the commands from the
`client` folder.

## Development Build

During development you will probably want to run `gulp watch`. This will build
a development version of the application and watch for any changes to the
source code. You can use `gulp build` if you just want to build a development
version without watching for changes afterwards.

The terminal output will show any JavaScript lint errors. You can also check for
lint errors using `gulp lint`.

## Distribution Build

You can build a distribution version of the application using `gulp build:dist`.
This builds an optimised version of the application in the `dist` folder. Source
files are concatenated and minified.

## Tasks

* `clean` - delete built files
* `build` - build the application for development
* `build:dist` - build the application for distribution
* `watch` - build the application and watch for changes
* `lint` - lint the JavaScript files
* `test` - run the tests
* `coverage` - run the tests and produce a coverage report
