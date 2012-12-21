about nginx...
==============

> [Nginx ("engine x")](http://nginx.org) 是一个高性能的 HTTP 和 反向代理 服务器


安装nginx
---------

网站下载: http://nginx.org 解压.

    ./configure
    make
    make install

如果安装过程出现错误,可能是缺少某些模块,configure的时候可以设置一些编译选项,如:

    ./configure --prefix=/usr/local/nginx-1.0.14 \      #指定路径
                --with-http_stub_status_module  \       #监控模块
                --with-http_gzip_static_module  \       #静态压缩
                --with-http_realip_module   \           #
                --add-module=/root/nginx_module/nginx_upload_module-2.2.0   #第三方模块 上传处理

如果编译过程缺少`pcre`,需要下载`pcre`源代码,网站: [www.pcre.org](http://www.pcre.org),解压既可,然后指定路径:

    --with-pcre=path-of-pcre


配置nginx
---------

安装完以后,简单的配置文件:

    user www-data www-data;
    worker_processes  2;

    error_log  logs/error.log;

    events {
        use epoll;      #linux 2.6 内核
        worker_connections  10240;
    }


    http {
        include       mime.types;
        default_type  text/plain;

        sendfile        on;     #sendfile指令指定 nginx 是否调用sendfile 函数（zero copy 方式）来输出文件

        keepalive_timeout  60;

        gzip  on;
        gzip_types text/plain application/x-javascript text/css application/xml;
        gzip_min_length  1000;
     
        include ng.conf;
    }

`ng.conf`:


    upstream www {
        server 192.168.1.10:80;
        server 192.168.1.20:80;
    }
    server {
        listen       80;
        server_name  *.xxx.com;
        charset gbk;

        proxy_buffering off;
        proxy_store off;
        location / {

            #屏蔽爬虫
            if ( $http_user_agent ~* "qihoobot|Baiduspider|Googlebot|Googlebot-Mobile|Googlebot-Image|Mediapartners-Google|Adsbot-Google|Feedfetcher-Google|Yahoo! Slurp|Yahoo! Slurp China|YoudaoBot|Sosospider|Sogou spider|Sogou web spider|MSNBot|ia_archiver|Tomato Bot") {
                return 403;
            }
            proxy_set_header   host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $remote_addr;
            client_max_body_size    50m;        #限制上传文件大小,默认是1m
            proxy_pass http://www;
        }

        location /nginxstatus {
            stub_status on;
            access_log on;
        }
        error_page   404 500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

其他设置
-------

nginx做反向代理的时候,后端的apache获取的客户端ip都是nginx所在服务器ip,要获得真实的客户端ip,apache需要安装一个模块:

    wget http://stderr.net/apache/rpaf/download/mod_rpaf-0.6.tar.gz
    tar xzf mod_rpaf-0.6.tar.gz
    cd mod_rpaf-0.6
    /usr/local/apache/bin/apxs -i -c -n mod_rpaf-2.0.so mod_rpaf-2.0.c

然后修改 `apache` 的配置文件:

    LoadModule rpaf_module modules/mod_rpaf-2.0.so
    RPAFenable On
    RPAFsethostname On
    RPAFproxy_ips 192.168.0.1       #nginx ip,如果前端有多个,可以空格间隔
    RPAFheader X-Forwarded-For

禁止图片外链,`none`表示直接访问的,`blocked`表示被防火墙修改过的:

    location ~* \.(gif|jpg|png|swf|flv) {
        valid_referers none blocked *.xxx.com;
        if ($invalid_referer) {
            return 403;
        }
    }

设置过期时间:

    location ~ \.(gif|jpg|jpeg|png|ico|css|js|txt)$ {
        expires 3d;
    }
    
禁止爬虫:

    if ( $http_user_agent ~* "qihoobot|Baiduspider|Googlebot|Googlebot-Mobile|Googlebot-Image|Mediapartners-Google|Adsbot-Google|Feedfetcher-Google|Yahoo! Slurp|Yahoo! Slurp China|YoudaoBot|Sosospider|Sogou spider|Sogou web spider|MSNBot|ia_archiver|Tomato Bot") {
            return 403;
    }

域名跳转,如果访问 `xxx.com` 自动跳转到 `www.xxx.com` ,或其他域名:

    if ($host = 'xxx.com') {
        rewrite ^/(.*)$ http://www.xxx.com/$1 permanent;
    }

优化
----

多核cpu,可以使用下面命令查看服务器cpu:

    $ cat /proc/cpuinfo | grep processor
    processor       : 0
    processor       : 1
    processor       : 2
    processor       : 3

nginx设置:

    worker_processes 4;
    worker_cpu_affinity 0001 0010 0100 1000;

减小Nginx编译后的文件大小,在编译Nginx时，默认以debug模式进行，而在debug模式下会插入很多跟踪和ASSERT之类的信息，编译完成后，一个Nginx要有好几兆。在编译前取消Nginx的debug模式，编译完成后Nginx只有几百k，因此可以在编译之前，修改相关源码，取消debug模式，具体方法如下：

在Nginx源码文件被解压后，找到源码目录下的 `auto/cc/gcc` 文件，在其中找到如下几行：

    # debug  
    CFLAGS=”$CFLAGS -g” 

注释掉或删掉这两行，即可取消debug模式。

启动nginx:

    /usr/local/nginx/sbin/nginx

停止:

    /usr/local/nginx/sbin/nginx -s quit


重载配置文件:

    /usr/local/nginx/sbin/nginx -s reload


END,GOOD LUCK!
--------------



