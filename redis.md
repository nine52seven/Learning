about Redis...
==============

> [Redis](http://redis.io/) is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain strings, hashes, lists, sets and sorted sets.

安装
----

网站下载,解压,编译

    $ wget http://redis.googlecode.com/files/redis-2.4.17.tar.gz
    $ tar xzf redis-2.4.17.tar.gz
    $ cd redis-2.4.17
    $ make

运行

    $ src/redis-server

命令行

    $ src/redis-cli
    redis> set foo bar
    OK
    redis> get foo
    "bar"



Link: 
    - [redis commands](http://redis.io/commands) 
    - [十五分钟介绍 Redis数据结构](http://blog.nosqlfan.com/html/3202.html)

END,GOOD LUCK!
--------------
