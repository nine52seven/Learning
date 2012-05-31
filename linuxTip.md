some tip about linux...
=======================


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

- centos 设置开机自动启动服务

        # chkconfig --list
        # chkconfig --list mysqld
        # chkconfig --add mysqld
        # chkconfig --del mysqld
        # chkconfig mysqld on
        # chkconfig mysqld off

- ufw 防火墙简单设置

        # ufw enable            //启用ufw
        # ufw disable           //仅用ufw
        # ufw default deny      //全部禁止
        # ufw allow from 192.168.1.1            //允许此IP访问所有的本机端口
        # ufw delete allow from 192.168.1.1         //删除上一条规则
        # ufw allow 80          //允许外部访问80端口
        # ufw delete allow 80   //禁止外部访问80 端口
        # ufw allow smtp    //允许smtp服务
        # ufw delete allow smtp     //禁止smtp服务

- ubuntu重新配置locale

    相关文件:

        $ cat /etc/default/locale
        $ cat /etc/environment

    优先级

        LC_ALL > LC_* > LANG

    12大类

    - 语言符号及其分类(LC_CTYPE)
    - 数字(LC_NUMERIC)
    - 比较和排序习惯(LC_COLLATE)
    - 时间显示格式(LC_TIME)
    - 货币单位(LC_MONETARY)
    - 信息主要是提示信息,错误信息, 状态信息, 标题, 标签, 按钮和菜单等(LC_MESSAGES)
    - 姓名书写方式(LC_NAME)
    - 地址书写方式(LC_ADDRESS)
    - 电话号码书写方式(LC_TELEPHONE)
    - 度量衡表达方式(LC_MEASUREMENT)
    - 默认纸张尺寸大小(LC_PAPER)
    - 对locale自身包含信息的概述(LC_IDENTIFICATION)。
        

    安装
    
        $ sudo cat /usr/share/i18n/SUPPORTED | grep 'en_US' > /var/lib/locales/supported.d/local
        $ sudo cat /usr/share/i18n/SUPPORTED | grep 'zh_CN' >> /var/lib/locales/supported.d/local
        $ sudo locale-gen --purge

    或者

        $ cd /usr/share/locales
        $ sudo ./install-language-pack en_US


    查看系统内安装的locale

        $ locale -a

    修改locale
        
        $ export LC_ALL='en_US.UTF-8'

    参考: http://wiki.ubuntu.org.cn/Locale

- ubuntu 升级

    先升级下各软件
        
        $ sudo apt-get update
        $ sudo apt-get upgrade

    之后备份各种配置文件,然后运行

        $ sudo apt-get install update-manager-core
        $ sudo do-release-upgrade

    完成以后重启,运行下面命令,就可以看到新版本的信息了

        $ lsb_release -a 


- ubuntu 安装deb包

    - dpkg -i package.deb   安装包
    - dpkg -r package   删除包
    - dpkg -P package   删除包（包括配置文件）
    - dpkg -L package   列出与该包关联的文件
    - dpkg -l package   显示该包的版本
    - dpkg –unpack package.deb    解开 deb 包的内容
    - dpkg -S keyword   搜索所属的包内容
    - dpkg -l   列出当前已安装的包
    - dpkg -c package   列出 deb 包的内容

- ubuntu 禁用ipv6

    适用9.04以后版本,查看是否启用

        $ cat /proc/sys/net/ipv6/conf/all/disable_ipv6

    显示
        
        - 0 --> Enabled
        - 1 --> Disabled

    或者

        $ ip a | grep inet6

    如果没有显示任何内容,说明已经禁用. 下面是禁用方法

        $ sudo vi /etc/sysctl.conf

    添加下面内容

        # IPv6
        net.ipv6.conf.all.disable_ipv6 = 1
        net.ipv6.conf.default.disable_ipv6 = 1
        net.ipv6.conf.lo.disable_ipv6 = 1

    保存退出,然后

        $ sudo sysctl -p

    禁用完成,可以用上面来查看是否禁用.还有一种修改grub的方法,可以上网查找.


- 关闭selinux

        $ sudo setenforece 0    //关闭selinux
        $ sudo setenforece 1    //启用selinux

    或者修改配置

        $ sudo vi /etc/selinux/config

    修改为 `SELINUX=disabled`


- Mysql 5.5

    日志里显示

        120510  1:51:36 [Warning] Unsafe statement written to the binary log using statement format since BINLOG_FORMAT = STATEMENT. The statement is unsafe because it uses a LIMIT clause. This is unsafe because the set of rows included cannot be predicted. Statement: delete from tablename where id='1' limit 1

    解决方法,修改 `/etc/my.cnf` 中binlog的格式

        binlog_format=MIXED

    binlog的记录格式有下面三种

    - STATEMENT 基于SQL语句的复制(statement-based replication, SBR)

    - ROW 基于行的复制(row-based replication, RBR)

    - MIXED 混合模式复制(mixed-based replication, MBR)

    也可以在运行时动态修改binlog的格式。例如

        mysql> SET SESSION binlog_format = 'STATEMENT';
        mysql> SET SESSION binlog_format = 'ROW';
        mysql> SET SESSION binlog_format = 'MIXED';
        mysql> SET GLOBAL binlog_format = 'STATEMENT';
        mysql> SET GLOBAL binlog_format = 'ROW';
        mysql> SET GLOBAL binlog_format = 'MIXED';

- 添加sudo用户

    修改文件 `/etc/sudoers`

        # chmod u+w /etc/sudoers      #修改文件可写
        # vi /etc/sudoers

    在 `root    ALL=(ALL:ALL) ALL` 行下面添加一行

        newuser    ALL=(ALL:ALL) ALL    #newuser为要添加sudo权限的用户
        # chmod u-w /etc/sudoers 

- ubuntu做网关,ufw需要打开转发功能
    
    # echo 1 > /proc/sys/net/ipv4/ip_forward
    # vi /etc/default/ufw

    修改 DEFAULT_FORWARD_POLICY="ACCEPT"



END,GOOD LUCK!
--------------
