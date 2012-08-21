about MooseFS...
=======================

> 分布式文件系统MFS(MooseFS),分为主控服务器Master server,存储块服务器 Chunk servers,客户端主机 (clients),主控备份服务器 Metalogger server,

安装MooseFS
----------

网站下载: [http://www.moosefs.org/](http://www.moosefs.org/),下载最新的安装包,以下为ubuntu 12.04为例.需要安装的软件包

    $ sudo apt-get install libfuse-dev
    $ sudo apt-get install pkg-config
    $ sudo apt-get install zlib1g-dev
    
当我们安装主控服务器时，在配置过程中(./configure)，可以取消安装 chunk server
（--disable-mfschunkserver）以及 MooseFS 客户端（--disable-mfsmount）. 安装主控服务器 master 的具体步骤为：

    # groupadd mfs
    # useradd -g mfs mfs
    # tar -zxvf mfs-1.6.25.tar.gz
    # cd mfs-1.6.25
    # ./configure --prefix=/usr/local/mfs-1.6.25 --with-default-user=mfs --with-default-group=mfs --disable-mfschunkserver --disable-mfsmount
    # make
    # make install
    # cd /usr/local/mfs-1.6.25/etc
    # cp mfsmaster.cfg.dist mfsmaster.cfg
    # cp mfsmetalogger.cfg.dist mfsmetalogger.cfg
    # cp mfsexports.cfg.dist mfsexports.cfg
    # cd /usr/local/mfs-1.6.25/var/mfs/
    # cp metadata.mfs.empty metadata.mfs

Mfsmaster.cfg 配置文件包含主控服务器 master 相关的设置，mfsexports.cfg 指定那些客户端主机可以远程挂接 MooseFS 文件系统，以及授予挂接客户端什么样的访问权限。

修改/etc/hosts 文件，以绑定主机名 mfsmaster 与 ip 地址 192.168.1.1:
    
    192.168.1.1 mfsmaster

启动

    # /usr/local/mfs-1.6.25/sbin/mfsmaster start

为了监控 MooseFS 当前运行状态，我们可以运行 CGI 监控服务，这样就可以用浏览器查看整个MooseFS 的运行情况:

    #/usr/sbin/mfscgiserv

现在，我们在浏览器地址栏输入 http://192.168.1.1:9425 即可查看 master 的运行情况（这个时候，是不能看见 chunk server 的数据）。

存储块服务器Chunk servers

    #cp  mfschunkserver.cfg.dist mfschunkserver.cfg 
    #cp  mfshdd.cfg.dist mfshdd.cfg

在配置文件 mfshdd.cfg 中，我们给出了用于客户端挂接 MooseFS 分布式文件系统根分区所使用的共享空间位置。

在启动 chunk  server 前，需确保用户 mfs 有权限读写将要被挂接的分区（因为 chunk server 运行时要在此创建一个.lock 的文件）

    #chown -R mfs:mfs /mnt/mfschunks1
    #chown -R mfs:mfs /mnt/mfschunks2

启动
    
    # /usr/local/mfs-1.6.25/sbin/mfschunkserver start

web监控程序启动,通过 `http://10.10.100:9425` 查看

    # /usr/local/mfs-1.6.25/sbin/mfscgiserv start

客户端挂载
    
    # /usr/local/mfs-1.6.25/bin/mfsmount /mnt/mfs -H 10.10.1.100

设置副本份数

    # /usr/local/mfs-1.6.25/bin/mfssetgoal -r 3 /mnt/mfs

    # /usr/local/mfs-1.6.25/bin/mfsgetgoal -r /mnt/mfs

恢复meta

    # /usr/local/mfs-1.6.25/sbin/mfsmetarestore -a

开启日志服务器

    # /usr/local/mfs/sbin/mfsmetalogger start
    # /usr/local/mfs/sbin/mfsmetalogger stop


END,GOOD LUCK!
--------------
