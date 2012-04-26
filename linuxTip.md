some tip about linux...
=======================

mysql
------

- `ubuntu` 默认安装的`mysql` 连接用户信息在 `/etc/mysql/debian.cnf` 文件里,并且需要注释掉 `/etc/mysql/my.cnf`里的下面一行,才能允许其他主机连接:

    # bind-address           = 127.0.0.1

- 查看`mysql`使用的`my.cnf`

    # mysqld --verbose --help | grep -A 1 'Default options'

- `ubuntu` 修改 `mysql` 的数据文件位置,默认安装在 `/var/lib/mysql/` 下面,如果想修改到别的目录,比如 `/data/mysql/`,重启mysql的时候有可能会报错启动不了,原因是因为ubuntu里的 `apparmor` 服务,详细说明请google之,解决方法如下:

    # vi /etc/apparmor.d/usr.sbin.mysqld
    ...
    # vim:syntax=apparmor
    # Last Modified: Tue Jun 19 17:37:30 2007
    #include <tunables/global>

    /usr/sbin/mysqld {
      #include <abstractions/base>
      #include <abstractions/nameservice>
      #include <abstractions/user-tmp>
      #include <abstractions/mysql>
      #include <abstractions/winbind>

      capability dac_override,
      capability sys_resource,
      capability setgid,
      capability setuid,

      network tcp,

      /etc/hosts.allow r,
      /etc/hosts.deny r,

      /etc/mysql/*.pem r,
      /etc/mysql/conf.d/ r,
      /etc/mysql/conf.d/* r,
      /etc/mysql/*.cnf r,
      /usr/lib/mysql/plugin/ r,
      /usr/lib/mysql/plugin/*.so* mr,
      /usr/sbin/mysqld mr,
      /usr/share/mysql/** r,
      /var/log/mysql.log rw,
      /var/log/mysql.err rw,
      /var/lib/mysql/ r,
      /var/lib/mysql/** rwk,
      /var/log/mysql/ r,
      /var/log/mysql/* rw,
      /var/run/mysqld/mysqld.pid w,
      /var/run/mysqld/mysqld.sock w,
      /etc/my.cnf r,
      /sys/devices/system/cpu/ r,

      #添加如下:
      /data/mysql/ r,
      /data/mysql/** rwk,
      /data/mysql/ r,
      /data/mysql/* rw,

      # Site-specific additions and overrides. See local/README for details.
      #include <local/usr.sbin.mysqld>
    }
    ...
    # /etc/init.d/apparmor restart
    # /etc/init.d/mysql start

- 启动 `mysql 5.5` 的半同步
    
    master  > INSTALL PLUGIN rpl_semi_sync_master soname 'semisync_master.so';
    slave-x > INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so’;
    master  > SET GLOBAL rpl_semi_sync_master_enabled=1;
    slave-x > SET GLOBAL rpl_semi_sync_slave_enabled=1;

如果是更新,需要先:

    mysql> UNINSTALL PLUGIN rpl_semi_sync_master;
    
- 查看网卡的速率:

    # ethtool eth0
    # mii-tool -v eth0



END,GOOD LUCK!
--------------
