
var fs = require('fs');
fs.appendFile('mynewfile1.txt', 'Hello content!', function
(err) {
if (err) throw err;
console.log('fs.appendFile() Method Appiled');
});
fs.open('mynewfile2.txt', 'w', function (err, file) {
if (err) throw err;
console.log('fs.open() Method Appiled');
});
fs.writeFile('mynewfile3.txt', 'Hello content!', function (err) {
if (err) throw err;
console.log('fs.writeFile() Method Appiled');
});
