some tip about mac...
=====================

- 卸载xcode

        $ sudo /Developer/Library/uninstall-devtools --mode=all

- 下载ssh-copy-id

        $ sudo curl https://raw.github.com/gist/1639381/eea46277ba544fcbd0a0768e8b3f854880ddb772/ssh-copy-id -o /usr/bin/ssh-copy-id
        $ sudo chmod +x /usr/bin/ssh-copy-id

    eg:

        $ ssh-copy-id -i ~/.ssh/id_rsa.pub 'username@host'

    如果默认端口不是22,则:

        $ ssh-copy-id -i ~/.ssh/id_rsa.pub "-p port username@host"

- 安装macports
    下载:

    [http://www.macports.org](http://www.macports.org/)

    需要先安装`xcode`,还有`xcode`里的`Command Line Tools`,因为需要编译软件,里面包含`make`等工具

    安装完以后,需要在环境路径里添加上macports的执行路径

        $ export PATH=/opt/local/bin:/opt/local/sbin:$PATH
        $ export MANPATH=/opt/local/share/man:$MANPATH

    还可以修改`/etc/paths`文件,把路径添加到里面,然后就可以更新了

        $ sudo port selfupdate

    下面是常用命令

        $ port list
        $ port search SOFTNAME
        $ port info SOFTNAME
        $ port deps SOFTNAME
        $ sudo port install SOFTNAME
        $ sudo port clean --all SOFTNAME
        $ sudo port uninstall SOFTNAME
        $ port installed
        $ sudo port upgrade SOFTNAME
        $ port outdated

- Mac excel 单元格换行

    按option+command+enter


END,GOOD LUCK!
--------------