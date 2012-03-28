# some tip about nginx...

    [Nginx \("engine x"\)](http://nginx.org) 是一个高性能的 HTTP 和 反向代理 服务器


### 安装nginx

网站下载: http://nginx.org,解压.

```ruby
./configure
make
make install
```

如果安装过程出现错误,可能是缺少某些模块,configure的时候可以设置一些编译选项,如:

```ruby
./configure --prefix=/usr/local/nginx-1.0.14 \      #指定路径
            --with-http_stub_status_module  \       #监控模块
            --with-http_gzip_static_module  \       #静态压缩
            --with-http_realip_module   \           #
            --add-module=/root/nginx_module/nginx_upload_module-2.2.0   #第三方模块 上传处理
```

安装完以后,简单的配置文件:

```ruby
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

    sendfile        on;     #上传文件需要打开

    keepalive_timeout  60;

    gzip  on;
    gzip_types text/plain application/x-javascript text/css application/xml;
    gzip_min_length  1000;
 
    include ng.conf;
}
```
ng.conf:

```ruby
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
```

nginx做反向代理的时候,后端的apache获取的客户端ip都是nginx所在服务器ip,要获得真实的客户端ip,apache需要安装一个模块:

```ruby
wget http://stderr.net/apache/rpaf/download/mod_rpaf-0.6.tar.gz
tar xzf mod_rpaf-0.6.tar.gz
cd mod_rpaf-0.6
/usr/local/apache/bin/apxs -i -c -n mod_rpaf-2.0.so mod_rpaf-2.0.c
```
然后修改apache的配置文件:

```ruby
LoadModule rpaf_module modules/mod_rpaf-2.0.so
RPAFenable On
RPAFsethostname On
RPAFproxy_ips 192.168.0.1       #nginx ip,如果前端有多个,可以空格间隔
RPAFheader X-Forwarded-For
```



