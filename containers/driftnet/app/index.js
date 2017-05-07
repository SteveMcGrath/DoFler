const parser = require('./lib/parser')
const spawn = require('child_process').spawn
const fs = require('fs')

const PID_FILE = '/var/run/driftnet.pid'

const removePidfile = function (callback) {
  fs.unlink(PID_FILE, (err) => {
    if (err && err.code !== 'ENOENT') {
      return callback(err)
    }

    callback()
  })
}

const startDriftnet = function () {
  console.log('Starting driftnet')
  console.log('Interface:', process.env.SPAN_INTERFACE)
  console.log('Image path:', process.env.IMAGE_PATH)

  var child = spawn('driftnet', ['-a', '-i', process.env.SPAN_INTERFACE, '-d', process.env.IMAGE_PATH])
  console.log('Driftnet: Started child thread')

  // When driftnet outputs data to standard output, we want to capture that
  // data, interpret it, and hand it off to the database.
  child.stdout.on('data', function (data) {
    parser(data)
  })

  child.stderr.on('data', function (data) {
    console.log('Driftnet: (stderr)' + data.toString().replace(/(\r\n|\n|\r)/gm, ''))
  })

  // If driftnet exists for some reason, log the event to the console
  // and then initiate a new instance to work from.
  child.on('close', function (code) {
    console.log('Driftnet child terminated with code ' + code)
    // TODO: Restart
  })

  child.on('error', function () {
    console.log('Driftnet: Failed to start process')
  })

  // Nodemon will send SIGUSR2, shut down gracefully so that it can restart the application
  process.on('SIGUSR2', function () {
    child.stdin.pause() // Pause the stdin so that we can exit without waiting for the debugger
    child.kill()
    process.exit()
  })
}

removePidfile((err) => {
  if (err) {
    console.error('Error removing pidfile', err)
    return process.exit(1)
  }

  startDriftnet()
})
