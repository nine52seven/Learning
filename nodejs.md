about Nodejs...
==============

> [Node.js](http://nodejs.org/) is a platform built on Chrome's JavaScript runtime for easily building fast, scalable network applications. Node.js uses an event-driven, non-blocking I/O model that makes it lightweight and efficient, perfect for data-intensive real-time applications that run across distributed devices.


AN EXAMPLE: WEBSERVER
---------------------

    var http = require('http');
    http.createServer(function (req, res) {
      res.writeHead(200, {'Content-Type': 'text/plain'});
      res.end('Hello World\n');
    }).listen(1337, '127.0.0.1');
    console.log('Server running at http://127.0.0.1:1337/');

    # node example.js
    Server running at http://127.0.0.1:1337/



Link:
----
- [nodejs](http://nodejs.org/) 
- [cnodejs.org 中文社区](http://cnodejs.org/)


END,GOOD LUCK!
--------------
