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


    indexer --merge test delta --rotate
    indexer --merge main delta --merge-dst-range deleted 0 0    //删除重复

    indexer --rotate --all


END,GOOD LUCK!
--------------
