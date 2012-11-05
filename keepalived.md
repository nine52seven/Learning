keepalived + mysql MM
=====================

此文档主要是实现用keepalived来实现对mysqlMM的ha处理,实现当一台Mysql出现故障的时候,自动切换到备用Mysql上,两个Mysql实现互为Master数据同步.

两台mysql realserver: `192.168.1.201`, `192.168.1.202`, 虚拟ip `192.168.1.200`



mysql 双master配置
---------------------

两台 mysql 均如要开启 `binlog` 日志功能,两台 mysql 的 `server-ID` 不能一样

`192.168.1.201 /etc/my.cnf`:

    server-id               = 1
    log_bin                 = /var/log/mysql/mysql-bin.log

`192.168.1.202 /etc/my.cnf`:

    server-id               = 2
    log_bin                 = /var/log/mysql/mysql-bin.log


将 `192.168.1.201` 设为 `192.168.1.202` 的主服务器, 在 `192.168.1.201` 添加同步授权账号

    mysql> grant replication slave on *.* to 'replication'@'%' identified by 'replication';
    Query OK, 0 rows affected (0.00 sec)
    mysql> show master status;
    +------------------+----------+--------------+------------------+
    | File | Position | Binlog_Do_DB | Binlog_Ignore_DB | +------------------+----------+--------------+------------------+
    | mysql-bin.000003 | 374 | | | +------------------+----------+--------------+------------------+
    1 row in set (0.00 sec)

在 `192.168.1.202` 上将 `192.168.1.201` 设为自己的主服务器:

    mysql> change master to master_host='`192.168.1.201`',master_user='replication',master_password='replication',master_log_file='mysql-bin.000003',master_log_pos=374;
    Query OK, 0 rows affected (0.05 sec)
    mysql> start slave;
    Query OK, 0 rows affected (0.00 sec)
    mysql> show slave status\G

将 `192.168.1.202` 设为 `192.168.1.201` 的主服务器, 在 `192.168.1.202` 上新建授权用户:


    mysql> grant replication slave on *.* to 'replication'@'%' identified by 'replication';
    Query OK, 0 rows affected (0.00 sec)
    mysql> show master status;
    +------------------+----------+--------------+------------------+
    | File | Position | Binlog_Do_DB | Binlog_Ignore_DB | +------------------+----------+--------------+------------------+
    | mysql-bin.000003 | 374 | | | +------------------+----------+--------------+------------------+
    1 row in set (0.00 sec)

在 `192.168.1.201` 上,将 `192.168.1.202` 设为自己的主服务器:

    mysql> change master to master_host='`192.168.1.202`',master_user='replication',master_password='replication',master_log_file='mysql-bin.000003',master_log_pos=374;
    Query OK, 0 rows affected (0.05 sec)
    mysql> start slave;
    Query OK, 0 rows affected (0.00 sec)
    mysql> show slave status\G

mysql 同步测试

如上述均正确配置,现在任何一台 mysql 上更新数据都会同步到另一台 mysql, 在此不再演示.



安装keepalived
------------------

下载: [keepalived](http://www.keepalived.org/), 安装keepalived:

    #tar zxvf keepalived-1.1.20.tar.gz
    #cd keepalived-1.1.20
    #./configure --prefix=/usr/local/keepalived --with-kernel-dir=/usr/src/linux    //指定安装路径和内核
    ......

    Keepalived configuration
    ------------------------
    Keepalived version       : 1.2.2
    Compiler                 : gcc
    Compiler flags           : -g -O2 -DETHERTYPE_IPV6=0x86dd
    Extra Lib                : -lpopt -lssl -lcrypto 
    Use IPVS Framework       : No
    IPVS sync daemon support : No
    Use VRRP Framework       : Yes
    Use Debug flags          : No

IPVS显示为No的话,需要安装 `ipvsadm` ,以及 `kernel-devel` :

    yum install ipvsadm
    yum install kernel-devel
    ln -s /usr/src/kernels/2.6.18-308.1.1.el5-i686 linux

配置成功显示:

    Keepalived configuration
    ------------------------
    Keepalived version       : 1.2.2
    Compiler                 : gcc
    Compiler flags           : -g -O2 -DETHERTYPE_IPV6=0x86dd
    Extra Lib                : -lpopt -lssl -lcrypto 
    Use IPVS Framework       : Yes
    IPVS sync daemon support : Yes
    IPVS use libnl           : No
    Use VRRP Framework       : Yes
    Use Debug flags          : No

然后编译安装:

    make & make install



如果编译的时候出现:

    !!!OpenSSL is not properly installed on your system. !!!


需要安装openssl

    yum install openssl-devel openssl

如果是unbuntu:

    apt-get install openssl libssl-dev


出现:

    configure: error: Popt libraries is required


安装:

    apt-get install libpopt0 libpopt-dev

注意：make步骤中若出现 `fd_set` 、`blkcnt_t` 类型冲突之类的错误，可以修改 `./keepalived/libipvs-2.6/ip_vs.h` 文件，将 `#include linux/types.h` 行移到 `#include sys/types.h` 行之后，然后重新执行make进行编译即可。

    # vi keepalived/libipvs-2.6/ip_vs.h
    ……
    #include sys/types.h
    #include linux/types.h 
    ……
    #make & make install


拷贝keepalived的配置文件到 `/etc` 目录下:

    # cp /usr/local/keepalived/etc/rc.d/init.d/keepalived /etc/rc.d/init.d/ 
    # cp /usr/local/keepalived/etc/sysconfig/keepalived /etc/sysconfig 
    # mkdir /etc/keepalived 
    # cp /usr/local/keepalived/etc/keepalived/keepalived.conf /etc/keepalived 
    # cp /usr/local/keepalived/sbin/keepalived /usr/sbin



keepalived 配置文件 `/etc/keepalived/keepalived.conf`
-------------------------------------------------------

keepalived启动的时候会查找 `/etc/keepalived/keepalived.conf` , 配置样例如下:

    ! Configuration File for keepalived
    global_defs {
        notification_email {
            xxx@xxx.com
        }
        notification_email_from xxx@xxx.com
        smtp_server 127.0.0.1 
        smtp_connect_timeout 30
        router_id mysql-ha
    }

    vrrp_instance VI_1 {
        state BACKUP    # 都是BACKUP
        interface eth0
        virtual_router_id 60    # 一样
        priority 100            # 优先级, 另一个要小于这个值
        advert_int 1
        nopreempt               # 无抢占设置, 另一个要去掉
        authentication {
            auth_type PASS
            auth_pass 4321
        }
        virtual_ipaddress { 
            192.168.1.200       #虚拟ip,可以有多个
            192.168.1.300       #虚拟ip2
        }
    }

    virtual_server 192.168.1.200 3306 {
        delay_loop 2    # 每2s检查
        lb_algo wrr     # lvs算法
        lb_kind DR
        persistence_timeout 60      # (同一IP的连接60秒内被分配到同一台realserver, 此例用不到)
        protocol TCP
        sorry_server 127.0.0.1 80    #realserver全down则转发到这里
        real_server `192.168.1.201` 3306 {       # 本机ip
            weight 3
            notify_down /usr/local/mysql/bin/mysql.sh   # 检测到服务停止时触发的脚本
            TCP_CHECK {
                connect_timeout 10      # 几秒连接超时
                nb_get_retry 3
                delay_before_retry 3
                connect_port 3306
            }
        }
    }


触发脚本 `/usr/local/mysql/bin/mysql.sh` :

    #!/bin/sh  
    pkill keepalived

这个脚本很简单,就是结束keepalived的进程,从而告知备用机托管虚拟ip,其实这个脚本里可以编写更复杂的脚本,比如

- 结束keepalived
- 重启mysql
- 启动keepalived

以上安装完以后,两台机器分别先启动mysql,再启动keepalived:

    #/etc/rc.d/init.d/mysql start
    #/etc/rc.d/init.d/keepalived start

还要检查`iptables`,否则两机之间的心跳检测会有问题

查看日志:

    #tail -n 100 /var/log/messages
    Mar 19 12:19:59 bank7 Keepalived: Terminating on signal
    Mar 19 12:19:59 bank7 Keepalived: Stopping Keepalived v1.1.20 (02/22,2012) 
    Mar 19 12:19:59 bank7 Keepalived_vrrp: Terminating VRRP child process on signal
    Mar 19 12:19:59 bank7 Keepalived_healthcheckers: Terminating Healthchecker child process on signal
    Mar 19 12:19:59 bank7 Keepalived_vrrp: VRRP_Instance(VI_1) removing protocol VIPs.
    Mar 19 12:20:00 bank7 Keepalived: Starting Keepalived v1.1.20 (02/22,2012) 
    Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Netlink reflector reports IP `192.168.1.202` added
    Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Registering Kernel netlink reflector
    Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Registering Kernel netlink command channel
    Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Opening file '/etc/keepalived/keepalived.conf'. 
    Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Configuration is using : 9803 Bytes
    Mar 19 12:20:00 bank7 Keepalived: Starting Healthcheck child process, pid=11581
    Mar 19 12:20:00 bank7 Keepalived_vrrp: Netlink reflector reports IP `192.168.1.202` added
    Mar 19 12:20:00 bank7 Keepalived_vrrp: Registering Kernel netlink reflector
    Mar 19 12:20:00 bank7 Keepalived_vrrp: Registering Kernel netlink command channel
    Mar 19 12:20:00 bank7 Keepalived: Starting VRRP child process, pid=11583
    Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Using LinkWatch kernel netlink reflector...
    Mar 19 12:20:00 bank7 Keepalived_vrrp: Registering gratutious ARP shared channel
    Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Activating healtchecker for service [`192.168.1.202`:3306]
    Mar 19 12:20:00 bank7 Keepalived_vrrp: Opening file '/etc/keepalived/keepalived.conf'. 
    Mar 19 12:20:00 bank7 Keepalived_vrrp: Configuration is using : 36214 Bytes
    Mar 19 12:20:00 bank7 Keepalived_vrrp: Using LinkWatch kernel netlink reflector...
    Mar 19 12:20:00 bank7 Keepalived_vrrp: VRRP_Instance(VI_1) Entering BACKUP STATE
    Mar 19 12:20:00 bank7 Keepalived_vrrp: VRRP sockpool: [ifindex(2), proto(112), fd(10,11)]

可以用下面命令查看当前虚拟ip在哪个机器上:

    # ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
        inet6 ::1/128 scope host 
           valid_lft forever preferred_lft forever
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
        link/ether 00:13:72:fb:da:8f brd ff:ff:ff:ff:ff:ff
        inet `192.168.1.201`/24 brd 192.168.1.255 scope global eth0
        inet 192.168.1.200/32 scope global eth0
        inet6 fe80::213:72ff:fefb:da8f/64 scope link 
           valid_lft forever preferred_lft forever
    3: eth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop qlen 1000
        link/ether 00:13:72:fb:da:91 brd ff:ff:ff:ff:ff:ff
    4: sit0: <NOARP> mtu 1480 qdisc noop 
        link/sit 0.0.0.0 brd 0.0.0.0

keepalived 主备iptables设置
-------------------------

需要在iptables里添加下面两行

    -A   INPUT   -d   224.0.0.0/8   -j   ACCEPT
    -A   INPUT    -p   vrrp   -j   ACCEPT


测试
----

在另外的机器上连接虚拟ip的mysql服务,停止mysql,备用机会自动托管虚拟ip,时间很短.

**注意** : 这样的切换是在两台mysql服务器能够瞬时同步的基础上的,如果两台服务器同步很慢,那切换的时候会出问题的,特别是有自增长字段的时候.所以还需要对mysql的同步状态做进一步的检查.

**注意** : 检查mysql是否同步的时候可以使用 `show slave status;` ,显示的信息里有个 `Seconds_Behind_Master`, 可以判断是否同步一致

**注意** : 还要检查各机器的防火墙设置
    
END,GOOD LUCK!
--------------
    
