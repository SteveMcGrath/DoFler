var parser = require('./lib/parser')
var spawn = require('child_process').spawn

console.log('Interface:', process.env.SPAN_INTERFACE)
console.log('Image path:', process.env.IMAGE_PATH)

// TODO: Remove pid file in /var/run/driftnet.pid if it exists
// TODO: Kill driftnet on exit..Set pid file to something we can delete? always clean it up before?
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

// Nodemon restart
process.on('SIGUSR2', function () {
  console.log('Sigusr!')
  child.kill()
})
