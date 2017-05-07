module.exports = function parse (input, callback) {
  console.log(input.toString())

  /* // First thing we went to do is strip out the line endings
     // from the output.
     var filenames = data.toString().split('\n')
     // var filenames = data.toString().replace(/(\r\n|\n|\r)/gm, '');

     // Next we will attempt to open the file that driftnet
     // output the location to.
     filenames.forEach(function (filename) {
       // var filename = filenames[f];
       if (filename.length > 4) {
         // console.log('Driftnet: found ' + filename);
         fs.readFile(filename, function (e, data) {
           if (e) { console.log('Driftnet: ' + e) } else {
             // If the file opened correctly, then we will compute
             // an md5 hash.  The ext regex is designed to get the
             // file extension from the filename.
             var hash = md5File(data)
             var ext = /(?:\.([^.]+))?$/.exec(filename)[1]
             if (ext === 'jpeg') {
               ext = 'jpg'
             }
             if (ext === 'tiff') {
               ext = 'tif'
             }
             var newFilename = hash + '.' + ext
             // Next we will attempt to move the file to its new home.
             // If the file already exists, then the move will fail.
             mv(filename, config.AppServer.images + '/' + newFilename,
               { clobber: false }, function (err) {
                 if (err && err.code !== 'EEXIST') {
                   console.log('Driftnet: attempt to move ' + filename + ' failed. ' + err)
                   fs.unlink(filename, function () { })
                 } else {
                   if (err) {
                     // console.log('Driftnet: ' + hash + ' already exists, so removing duplicate.')
                     fs.unlink(filename, function () { })
                   }
                   // Now lets query the database and see if an image exists
                   // with the same md5sum as what we computed.  If there is
                   // an existing image, then we'll increment the counter and
                   // update the date timestamp.  If one doesn't exist, then
                   // we will create a new image with the information we have.
                   db.Image.findOrCreate({
                     where: { hash: hash },
                     defaults: {
                       type: ext,
                       filename: newFilename,
                       url: 'DRIFTNET',
                       count: 1
                     }
                   }).spread(function (image, created) {
                     // We need to attempt to avoid double-counting if possible. as driftnet will
                     // always fall behing ngrep here, we want to check to see if we already saw
                     // the image within the last 10 seconds.  if we have, then dont bother to
                     // to update.
                     if (!(created) && ((new Date().getTime() - image.date.getTime()) >= 1000)) {
                       image.updateAttributes({
                         count: image.count++,
                         date: new Date()
                       }).then(function (result) { })
                       io.emit('images', image)
                       console.log('Driftnet: ' + image.filename + ' updated!')
                     }// else {
                     // console.log('Driftnet: ngrep already got ' + image.hash);
                     // }
                     if (created) {
                       nude.scan(config.AppServer.images + '/' + image.filename, function (_, res) {
                         image.updateAttributes({
                           nsfw: res,
                           complete: true
                         }).then(function (result) {
                           console.log('Driftnet: ' + image.filename + ' added to the database with nsfw score of ' + image.nsfw)
                           if (!image.nsfw || !config.Monitoring.Driftnet.nsfw_filter) {
                             io.emit('images', image)
                           }
                         })
                       })
                     }
                   })
                 }
               })
           }
         })
       }
     }) */
}
