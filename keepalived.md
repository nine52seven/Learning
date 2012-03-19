# keepalived + mysql MM
此文档主要是实现用keepalived来实现对mysqlMM的ha处理,实现当一台Mysql出现故障的时候,自动切换到备用Mysql上,两个Mysql实现互为Master数据同步.

### mysql 双master配置
两台 mysql 均如要开启 binlog 日志功能,两台 mysql 的 server-ID 不能一样,默认情况下两台 mysql 的 serverID 都是 1,需将其中一台 修改为 2 即可

两台mysql realserver: 192.168.1.201, 192.168.1.202, 虚拟ip 192.168.1.200

192.168.1.201 /etc/my.cnf:

```ruby
server-id               = 1
log_bin                 = /var/log/mysql/mysql-bin.log
```

192.168.1.202 /etc/my.cnf:

```ruby
server-id               = 2
log_bin                 = /var/log/mysql/mysql-bin.log
```

将 192.168.1.201 设为 192.168.1.202 的主服务器, 在192.168.1.201添加同步授权账号

```ruby
mysql> grant replication slave on *.* to 'replication'@'%' identified by 'replication';
Query OK, 0 rows affected (0.00 sec)
mysql> show master status;
+------------------+----------+--------------+------------------+
| File | Position | Binlog_Do_DB | Binlog_Ignore_DB | +------------------+----------+--------------+------------------+
| mysql-bin.000003 | 374 | | | +------------------+----------+--------------+------------------+
1 row in set (0.00 sec)

```

在 192.168.1.202 上将 192.168.1.201 设为自己的主服务器:

```ruby
mysql> change master to master_host='192.168.1.201',master_user='replication',master_password='replication',master_log_file='mysql-bin.000003',master_log_pos=374;
Query OK, 0 rows affected (0.05 sec)
mysql> start slave;
Query OK, 0 rows affected (0.00 sec)
mysql> show slave status\G
```

将 192.168.1.202 设为 192.168.1.201 的主服务器, 在 192.168.1.202 上新建授权用户

```ruby
mysql> grant replication slave on *.* to 'replication'@'%' identified by 'replication';
Query OK, 0 rows affected (0.00 sec)
mysql> show master status;
+------------------+----------+--------------+------------------+
| File | Position | Binlog_Do_DB | Binlog_Ignore_DB | +------------------+----------+--------------+------------------+
| mysql-bin.000003 | 374 | | | +------------------+----------+--------------+------------------+
1 row in set (0.00 sec)

```
在 192.168.1.201 上,将 192.168.1.202 设为自己的主服务器:

```ruby
mysql> change master to master_host='192.168.1.202',master_user='replication',master_password='replication',master_log_file='mysql-bin.000003',master_log_pos=374;
Query OK, 0 rows affected (0.05 sec)
mysql> start slave;
Query OK, 0 rows affected (0.00 sec)
mysql> show slave status\G
```

mysql 同步测试

如上述均正确配置,现在任何一台 mysql 上更新数据都会同步到另一台 mysql,mysql 同步 在此不再演示


### 安装keepalived

下载: [keepalived](http://www.keepalived.org/), 需要先安装 ipvsadm,

```ruby
yum install ipvsadm
```
安装keepalived:

```ruby
#tar zxvf keepalived-1.1.20.tar.gz
#cd keepalived-1.1.20
#./configure --prefix=/usr/local/keepalived --with-kernel-dir=/usr/src/kernels/2.6.18-164.el5-i686 
#make && make install
```

如果没有/usr/src/kernels/2.6.18-164.el5-i686此目录,需要安装 kernel-devel ,

如果没有找到内核文件,会出现以下信息

```ruby
IPVS sync daemon support : No
```

如果编译的时候出现:

```ruby
!!!OpenSSL is not properly installed on your system. !!!
```

需要安装openssl

```ruby
yum install openssl-devel
```



### keepalived 配置文件 /etc/keepalived/keepalived.conf

keepalived启动的时候会查找/etc/keepalived/keepalived.conf, 配置样例如下:

```ruby
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
        192.168.1.200       #虚拟ip
    }
}

virtual_server 192.168.1.200 3306 {
    delay_loop 2    # 每2s检查
    lb_algo wrr     # lvs算法
    lb_kind DR
    persistence_timeout 60      # (同一IP的连接60秒内被分配到同一台realserver, 此例用不到)
    protocol TCP
    real_server 192.168.1.201 3306 {       # 本机ip
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
```

触发脚本/usr/local/mysql/bin/mysql.sh:

```ruby
#!/bin/sh  
pkill keepalived
```


这个脚本很简单,就是结束keepalived的进程,从而告知备用机托管虚拟ip,其实这个脚本里可以编写更复杂的脚本,比如

- 结束keepalived
- 重启mysql
- 启动keepalived


以上安装完以后,两台机器分别先启动mysql,在启动keepalived:

```ruby
#/etc/rc.d/init.d/mysql start
#/etc/rc.d/init.d/keepalived start
```

查看日志:

```ruby
#tail -n 100 /var/log/messages
Mar 19 12:19:59 bank7 Keepalived: Terminating on signal
Mar 19 12:19:59 bank7 Keepalived: Stopping Keepalived v1.1.20 (02/22,2012) 
Mar 19 12:19:59 bank7 Keepalived_vrrp: Terminating VRRP child process on signal
Mar 19 12:19:59 bank7 Keepalived_healthcheckers: Terminating Healthchecker child process on signal
Mar 19 12:19:59 bank7 Keepalived_vrrp: VRRP_Instance(VI_1) removing protocol VIPs.
Mar 19 12:20:00 bank7 Keepalived: Starting Keepalived v1.1.20 (02/22,2012) 
Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Netlink reflector reports IP 192.168.1.202 added
Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Registering Kernel netlink reflector
Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Registering Kernel netlink command channel
Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Opening file '/etc/keepalived/keepalived.conf'. 
Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Configuration is using : 9803 Bytes
Mar 19 12:20:00 bank7 Keepalived: Starting Healthcheck child process, pid=11581
Mar 19 12:20:00 bank7 Keepalived_vrrp: Netlink reflector reports IP 192.168.1.202 added
Mar 19 12:20:00 bank7 Keepalived_vrrp: Registering Kernel netlink reflector
Mar 19 12:20:00 bank7 Keepalived_vrrp: Registering Kernel netlink command channel
Mar 19 12:20:00 bank7 Keepalived: Starting VRRP child process, pid=11583
Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Using LinkWatch kernel netlink reflector...
Mar 19 12:20:00 bank7 Keepalived_vrrp: Registering gratutious ARP shared channel
Mar 19 12:20:00 bank7 Keepalived_healthcheckers: Activating healtchecker for service [192.168.1.202:3306]
Mar 19 12:20:00 bank7 Keepalived_vrrp: Opening file '/etc/keepalived/keepalived.conf'. 
Mar 19 12:20:00 bank7 Keepalived_vrrp: Configuration is using : 36214 Bytes
Mar 19 12:20:00 bank7 Keepalived_vrrp: Using LinkWatch kernel netlink reflector...
Mar 19 12:20:00 bank7 Keepalived_vrrp: VRRP_Instance(VI_1) Entering BACKUP STATE
Mar 19 12:20:00 bank7 Keepalived_vrrp: VRRP sockpool: [ifindex(2), proto(112), fd(10,11)]
```

可以用下面命令查看当前虚拟ip在哪个机器上:

```ruby
ip a
```

### 测试
在另外的机器上连接虚拟ip的mysql服务,停止mysql,备用机会自动托管虚拟ip,时间很短

此应用还可以用于其他应用,比如负载均衡的ha.
    
***
END, good luck!
    
