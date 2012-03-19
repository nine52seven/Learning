# keepalived + mysql MM
### mysql 双master配置

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
    
