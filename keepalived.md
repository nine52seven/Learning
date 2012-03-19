# keepalived + mysql MM
此文档主要是实现用keepalived来实现对mysqlMM的ha处理,实现当一台Mysql出现故障的时候,自动切换到备用Mysql上,两个Mysql实现互为Master数据同步.

### mysql 双master配置
两台 mysql 均如要开启 binlog 日志功能,开启方法:在 mysql 配置文件[mysqld]段中加上 log-bin=mysql-bin 选项

两台 mysql 的 server-ID 不能一样,默认情况下两台 mysql 的 serverID 都是 1,需将其中一台 修改为 2 即可

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


### keepalived 配置文件 /etc/keepalived/keepalived.conf

keepalived启动的时候会查找/etc/keepalived/keepalived.conf, 配置样例如下:

```ruby
! Configuration File for keepalived
global_defs {
    notification_email {
        chaing@163.com
    }
    notification_email_from chaing@163.com
    smtp_server 127.0.0.1 
    smtp_connect_timeout 30
    router_id mysql-ha 
}

vrrp_instance VI_1 {
    state BACKUP    # 都是BACKUP
    interface eth0
    virtual_router_id 60    # 一样
    priority 100            # 另一个要小于这个值
    advert_int 1
    nopreempt               # 另一个要去掉
    authentication {
        auth_type PASS
        auth_pass 4321
    }
    virtual_ipaddress { 
        211.103.155.45
    }
}

virtual_server 211.103.155.45 3306 {
    delay_loop 2    # 每2s检查
    lb_algo wrr     # lvs算法
    lb_kind DR
    persistence_timeout 60      ##(同一IP的连接60秒内被分配到同一台realserver, 此例用不到)
    protocol TCP
    real_server 211.103.155.43 3306 {
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



    
***
END
    
