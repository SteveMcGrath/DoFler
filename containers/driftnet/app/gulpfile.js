var gulp = require('gulp')
var plugins = require('gulp-load-plugins')()
var runSequence = require('run-sequence')
var merge = require('merge-stream')
var glob = require('glob')

var watch = false

const PATHS = {
  lib: [
    'index.js',
    'lib/**/*.js'
  ],

  test: [
    'test/**/*_test.js'
  ]
}

const MOCHA_OPTIONS = {
  reporter: 'spec'
}

const TEST_PATH_MAP = {
  'index.js': function () {
    return 'test/index_test.js'
  },
  'lib/(.+).js': function (result) {
    return 'test/lib/' + result[1] + '_test.js'
  }
}

var sequenceError = function (callback, error) {
  if (error) {
    plugins.util.log(plugins.util.colors.red('There was an error running the sequence!'))
    process.exit(1)
  }

  callback()
}

var deriveTestPaths = function (path) {
  var paths = []

  Object.keys(TEST_PATH_MAP).forEach(function (key) {
    var expression = new RegExp(key)
    var result = expression.exec(path)

    if (result) {
      var fullPath = TEST_PATH_MAP[key](result)
      if (fullPath && glob.sync(fullPath).length) {
        paths.push(fullPath)
      }
    }
  })

  return paths
}

var plumbing = function (error) {
  plugins.util.log(plugins.util.colors.red('Error (' + error.plugin + '): ' + error.message))
  this.emit('end')
}

var addLinting = function (pipe) {
  var reporter = plugins.standard.reporter('default', {
    breakOnError: !watch,
    breakOnWarning: !watch,
    quiet: true
  })

  pipe = pipe
    .pipe(plugins.standard())
    .pipe(reporter)

  reporter.on('error', function (error) {
    return new plugins.util.PluginError(error)
  })

  return pipe
}

var tasks = {
  lib: function (event) {
    var streams = []

    if (event && event.path) {
      var testPaths = deriveTestPaths(event.path)
      if (testPaths.length) {
        var tests = gulp.src(testPaths)
          .pipe(!watch ? plugins.util.noop() : plugins.plumber(plumbing))
          .pipe(plugins.mocha(MOCHA_OPTIONS))

        streams.push(tests)
      }
    }

    streams.push(addLinting(gulp.src(PATHS.lib)))

    return merge(streams)
  },

  test: function (event) {
    var streams = []

    var testPath = event && event.path ? event.path : PATHS.test

    var tests = gulp.src(testPath)
      .pipe(!watch ? plugins.util.noop() : plugins.plumber(plumbing))
      .pipe(plugins.mocha(MOCHA_OPTIONS))

    streams.push(tests)

    streams.push(addLinting(gulp.src(testPath)))

    return merge(streams)
  }
}

Object.keys(tasks).forEach(function (task) {
  gulp.task(task, tasks[task])
})

gulp.task('default', function (callback) {
  watch = true
  return runSequence('build', ['watch', 'serve'], function (error) {
    sequenceError(callback, error)
  })
})

gulp.task('watch', function () {
  watch = true
  Object.keys(PATHS).forEach(function (task) {
    gulp.watch(PATHS[task], tasks[task])
  })
})

gulp.task('build', function (callback) {
  return runSequence(Object.keys(PATHS), function (error) {
    sequenceError(callback, error)
  })
})

gulp.task('serve', function () {
  plugins.nodemon({
    script: 'index.js',
    nodeArgs: ['--inspect=0.0.0.0:4001'],
    env: process.env,
    tasks: ['build']
  })
})
