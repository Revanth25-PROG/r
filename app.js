var express = require('express');
var app = express();
app.get('/', function (req, res) {
    res.send('this is demo!');
});
app.listen(5000);