# keepalived + mysql MM
### keepalived

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
    state BACKUP    //都是BACKUP
    interface eth0
    virtual_router_id 60    //一样
    priority 100            //另一个要小于这个值
    advert_int 1
    nopreempt               //另一个不需要
    authentication {
        auth_type PASS
        auth_pass 4321
    }
    virtual_ipaddress { 
        211.103.155.45
    }
}

virtual_server 211.103.155.45 3306 {
    delay_loop 2
    lb_algo wrr
    lb_kind DR
    persistence_timeout 60
    protocol TCP
    real_server 211.103.155.43 3306 {
    weight 3
    notify_down /usr/local/mysql/bin/mysql.sh 
    TCP_CHECK {
        connect_timeout 10
        nb_get_retry 3
        delay_before_retry 3
        connect_port 3306
    }
}
```

    
***
END
    
