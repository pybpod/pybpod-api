// http://stackoverflow.com/questions/6084360/using-node-js-as-a-simple-web-server
// https://www.npmjs.com/package/node-watch
// https://nodejs.org/api/child_process.html

var watch = require('node-watch');
const exec = require('child_process').exec;

watch('source', { recursive: true }, function(evt, name) {
//	exec('make clean && make html',
        exec('make html',

  		function (error, stdout, stderr) {
    		console.log('output: ' + stdout);
    		//console.log('error: ' + error);
    		console.error('warnings: ' + stderr);
		})
});


var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic("build/html/")).listen(8080, function(){
    console.log('Server running on 8080...');
});

