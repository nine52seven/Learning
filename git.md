git 使用
========

权限管理器 `Gitosis` 安装
---------------------

    $ yum install python-setuptools      //python工具
    $ git clone git://github.com/res0nat0r/gitosis.git
    $ cd gitosis
    $ sudo python setup.py install
    $ sudo -H -u git gitosis-init < /tmp/id_dsa.pub
    $ sudo chmod 755 /home/git/gitosis-admin.git/hooks/post-update


    /git/repositories/gitosis-admin.git/gitosis-export/gitosis.conf 
    文件是用来设置用户、仓库和权限的控制文件。
    /git/repositories/gitosis-admin.git/keydir
    目录则是保存所有具有访问权限用户公钥的地方

    $ git clone git@SERVER:gitosis-admin.git

        
clone分支
---------

  clone获取的git库,只包含了当前工作分支,如想获取其他分支信息,需要使用 `git branch -r` 来查看,
    然后 `git checkout -b 本地分支名 远程分支名` ,如果本地分支已经存在,则不需要 `-b` 参数.
    eg: 

    git branch -r
    git checkout -b 本地分支名 origin/远程分支名

常用命令
-------
    
    $ git remote prune remote_branch    # 删除远程all stale tracking分支
    $ git remote rm remote_branch   #删除所有分支
    $ git remote
        origin
    $ git branch -r
        origin/master
    $ git remote add linux-nfs git://linux-nfs.org/pub/linux/nfs-2.6.git
    $ git remote
        linux-nfs
        origin
    $ git fetch
        * refs/remotes/linux-nfs/master: storing branch 'master' ...
        commit: bf81b46
    $ git branch -r
        origin/master
        linux-nfs/master
    $ git checkout -b nfs linux-nfs/master


gitHub上的操作
-------------

Download and install Git

    $ git config --global user.name "chaing"
    $ git config --global user.email chaing@gmail.com


Next steps:

    $ mkdir myGit
    $ cd myGit
    $ git init
    $ touch README
    $ git add README
    $ git commit -m 'first commit'
    $ git remote add origin git@github.com:chaing/myGit.git
    $ git push origin master

Existing Git Repo?

    $ cd existing_git_repo
    $ git remote add origin git@github.com:chaing/myGit.git
    $ git push origin master


初始化一个本地库:

    $ git init myGit

查看状态:

    $ git status

添加跟踪文件:

    $ git add file-name

提交到本地库:

    $ git commit -m "init mygit"
  
创建分支:

    $ git branch branch-name

  
转换到分支:

    $ git checkout branch-name

  
删除分支:

    $ git branch -D branch-name     #强制删除
    $ git branch -d branch-name     #如果没有合并到主分支,则删除不了

  
查看分支:

    $ git branch

详细情况:

    $ git show-branch

比较当前工作目录和版本库中数据的差别:

    $ git diff

合并两个分支:

    $ git checkout master
    $ git merge "Merge work in robin" HEAD branch-name
    $ git merge branch-name

拉取远程上的变化:
    
    $ git pull

提交到远程服务器上:

    $ git push


**注意:** **git不能添加空目录到索引里**,可以在空目录下添加一个 `.gitignore` 的空文件,然后 `git add dir/.gitignore`

使用下面的目录可以遍历添加:

    $ find . \( -type d -empty \) -and \( -not -regex ./\.git.* \) -exec touch {}/.gitignore \;

新手开始使用的问题
---------------

- 初始化一个库

        $ mkdir myrepo
        $ cd myrepo
        $ git init

- 添加文件到库中

        $ touch readme
        $ git add readme

- 提交代码
    
    提交到本地库

        $ git commit -am 'add readme'

    提交到远程git服务器
    
        $ git remote add origin <server>
        $ git push origin master

- 从git服务器拉取最新的代码

        $ git pull

    相当于

        $ git fetch
        $ git merge

- 建立分支,切换分支,合并分支,删除分支

        $ git branch dev
        $ git checkout dev
        Switched to branch 'dev'
        $ git merge dev     #当前分支是master
        ...
        $ git branch -d dev
        Deleted branch dev (was 4541233).
        $ git push origin :dev       # 删除远端分支

    查看远程分支

        $ git branch -r


- 回溯到前一版本
        
        $ git revert HEAD

- 查看提交日志
        
        $ git log # 查看提交信息
        $ git log --pretty=oneline  # 以整洁的单行形式显示提交信息
        $ git log --stat            # 查看提交信息及更新的文件

- 其他
    
    设置自己的名称和邮箱,全局

        $ git config --global user.name "Your name"
        $ git config --global user.email “Your email"

    本地库

        $ git config --local user.name "Your name"
        $ git config --local user.email “Your email"

- 自动分发

    自动分发可以有两种方法:

        # cat hooks/post-receive
        #!/bin/sh
        GIT_WORK_TREE=<分发到的目录> git checkout -f

    另一种
    
        #cat hooks/post-receive
        #!/bin/sh
        DEPLOY_DIR=<分发到的目录>
        cd $DEPLOY_DIR
        env -i git pull

    注意,两者分发到的目录的权限都需要对运行git的用户有读写权限,可以把git用户加入到apache的组里

- 生成报告

    [https://github.com/trybeee/GitStats](https://github.com/trybeee/GitStats)

        # git clone git://github.com/trybeee/GitStats.git
        # python ~/dev/gitstats/git-stats /youproject public


Link:
----
- [GitStats](https://github.com/trybeee/GitStats) 
- [a guide to using git](https://github.com/blynn/gitmagic)
- [gitlab.org](http://gitlab.org/)
- [.gitignore](https://github.com/GitHub/gitignore)
- [介绍一个成功的 Git 分支模型](http://www.oschina.net/translate/a-successful-git-branching-model)
- [gitosis](https://github.com/res0nat0r/gitosis)


END,GOOD LUCK!
--------------
