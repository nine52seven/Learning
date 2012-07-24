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
        $ sudo apt-get autoremove
        $ sudo apt-get autoclean

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

    修改 `DEFAULT_FORWARD_POLICY="ACCEPT"`

- centos新建隧道,打开转发和NAT
    
        # ip tunnel add tunnel0 mode ipip remote yyy.yyy.yyy.yyy local xxx.xxx.xxx.xxx
        # ip link set tunnel0 up
        # ip addr add 10.10.9.2/24 dev tunnel0

        # iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE
        # iptables --append FORWARD --in-interface eth1 -j ACCEPT

        # iptables -t nat -A POSTROUTING -s 10.10.9.0/24 -j MASQUERAD

        # route
        $远程ip   10.10.9.2       255.255.255.255 UGH   0      0        0 tunnel1

    另外 ip_forward需要打开

- 同步文件
    
    使用inotify+rsync从一个服务器实时同步到多个服务器上,下面是bash脚本,需要安装inotify-tools,rsync服务

        #!/bin/sh 
        srcdir="/var/html/"  #源目录
        ipaddress="192.168.1.100 192.168.1.200"  #目标服务器,可以多个
        dstdir="/var/html/"  #目标目录
        noinclude="tmp"   #忽略目录,相对路径
        if [ -n "$1" ]; then
            for i in $ipaddress; 
            do
                rsync -aqztH --exclude=${noinclude} --delete --progress ${srcdir} root@${i}:${dstdir}
            done
            exit;
        fi

        /usr/bin/inotifywait -mrq --exclude=${noinclude} --timefm '%d/%m/%y-%H:%M' --format '%T %w%f' -e modify,delete,create,attrib ${srcdir} | while read file 
        do 
            for i in $ipaddress; do
                rsync -aqztH --exclude=${noinclude} --delete --progress ${srcdir} root@${i}:${dstdir}
            done    
        done

    此脚本是预先做了ssh密钥登陆设置,所以同步的时候不需要数据登陆密码,加个参数(任意)可以预先同步过去,然后再在后台运行此程序即可

- 优化linux
    
    内核优化

        net.ipv4.tcp_max_syn_backlog = 65536
        net.core.netdev_max_backlog =  32768
        net.core.somaxconn = 32768

        net.core.wmem_default = 8388608
        net.core.rmem_default = 8388608
        net.core.rmem_max = 16777216
        net.core.wmem_max = 16777216

        net.ipv4.tcp_timestamps = 0
        net.ipv4.tcp_synack_retries = 2
        net.ipv4.tcp_syn_retries = 2

        net.ipv4.tcp_tw_recycle = 1
        #net.ipv4.tcp_tw_len = 1
        net.ipv4.tcp_tw_reuse = 1

        net.ipv4.tcp_mem = 94500000 915000000 927000000
        net.ipv4.tcp_max_orphans = 3276800

        #net.ipv4.tcp_fin_timeout = 30
        #net.ipv4.tcp_keepalive_time = 120
        net.ipv4.ip_local_port_range = 1024  65535

    打开连接数

        # ulimit -n
        1024
        # echo "ulimit -SHn 65536" >> /etc/profile

- 安装

END,GOOD LUCK!
--------------
