var express = require('express');
var http = require('http');

var PORT = process.env.PORT || 4000;

var LINES = [
    "LOL"
];

var lineIndex = 0;

var app = express();
app.get('/', function(req, res) {
    var message = LINES[lineIndex];

    lineIndex += 1;
    if (lineIndex > LINES.length) {
        lineIndex = 0;
        message = LINES[lineIndex];
    }

    res.send({message: message});
});

http.Server(app).listen(PORT, function() {
    console.log("HTTP server listening on port %s", PORT);
});