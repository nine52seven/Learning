some tip about mac...
=====================

卸载xcode
---------

    $ sudo /Developer/Library/uninstall-devtools --mode=all

下载ssh-copy-id
---------------

    $ sudo curl ‘https://raw.github.com/gist/1639381/eea46277ba544fcbd0a0768e8b3f854880ddb772/ssh-copy-id’ -o /usr/bin/ssh-copy-id
    $ sudo chmod +x /usr/bin/ssh-copy-id
eg:

    $ ssh-copy-id -i ~/.ssh/id_rsa.pub username@host


ubuntu重新配置locale
-------------------

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

    $ sudo cat /usr/share/i18n/SUPPORTED | grep 'en_US' > /var/lib/locales/supported.d/local
    $ sudo cat /usr/share/i18n/SUPPORTED | grep 'zh_CN' >> /var/lib/locales/supported.d/local
    $ sudo locale-gen --purge

安装

    $ cd /usr/share/locales
    $ sudo ./install-language-pack en_US


查看系统内安装的locale

    $ locale -a

修改locale
    
    $ export LC_ALL='en_US.UTF-8'

参考: http://wiki.ubuntu.org.cn/Locale



END,GOOD LUCK!
--------------