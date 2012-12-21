about sphinx...
=======================

> [Sphinx Search](http://sphinxsearch.com/) 是由俄罗斯人Andrew Aksyonoff 开发的高性能全文搜索软件包，在GPL与商业协议双许可协议下发行。

安装sphinx
----------

网站下载: [http://sphinxsearch.com](http://sphinxsearch.com),下载最新的安装包,以下为ubuntu 12.04为例.首先需要安装mysqlclient

    $ sudo apt-get install libmysqlclient-dev
    $ sudo apt-get install sphinxsearch

配置文件在`/etc/sphinxsearch/sphinx.conf`

    #分次查询
    sql_query_range = SELECT MIN(id),MAX(id) FROM documents
    sql_range_step = 1000
    sql_query = SELECT * FROM documents WHERE id>=$start AND id<=$end

CREATE TABLE `rt` (
`id` int(11) unsigned NOT NULL,
`weight` int(11) NOT NULL,
`query` varchar(255) NOT NULL,
`rtime` timestamp NOT NULL,
`stime` timestamp NOT NULL,
`ctime` timestamp NOT NULL,
`SYSUSERID` INT NOT NULL,
`CCID` INT NOT NULL,
`BILLID` INT NOT NULL,
`UPLOADERID` INT NOT NULL,
`WRONG` INT NOT NULL,
KEY `Query` (`Query`)
) ENGINE=SPHINX DEFAULT CHARSET=utf8 CONNECTION='sphinx://localhost:3312/test';

SELECT CRMSELLID as id,UNIX_TIMESTAMP(RENEWTIME) as rtime,UNIX_TIMESTAMP(SELLTIME) as stime,UNIX_TIMESTAMP(COMFTIME) as ctime,SYSUSERID,CCID,BILLID,UPLOADERID,WRONG FROM crm_logsell where CRMSELLID <= ( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )

indexer --merge test delta --rotate
indexer --merge main delta --merge-dst-range deleted 0 0    //删除重复

indexer --rotate --all


END,GOOD LUCK!
--------------
