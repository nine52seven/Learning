about Bash...
==============

---

- 得到字符串md5

        # echo -n 123 | md5sum | awk '{print $1}'
        # printf 123 | md5sum | awk '{print $1}'

- 截取字符串

        # str1=${string:0:3}
        # echo 'file.jpg' | cut -d . -f 1   // -> file

- 获取日期

        t=`date +%Y%m%d -d " -15 day"`
        Y=`expr substr $t 1 4`
        M=`expr substr $t 5 2`
        t=`date +"%Y-%m-%d %T"`

- 去除重复行

        awk '!a[$0]++' $file > $uniqfile

- for循环

        for ((i=$maxid;i>=$minid;i--));do
            echo $i
        done;

        #死循环
        while :
        do
            ...
            break;
        done

- if

        if [ $a -eq 0 ];then
            ...
        fi

- 取随机数

        # `echo $RANDOM | md5sum | cut -b 1-6`

- 取文件的crc

        # cksum file | awk '{print $1}'

- 比较

        -eq 等于
        -ne 不等于
        -gt 大于
        -ge 大于等于
        -lt 小于
        -le 小于等于

- 分割文件

        # split -a 3 -l 1000 file prefix    //-a 指定后缀索引的长度,-l 按行来分割,prefix 前缀
        # split -b 1k file prefix   //-b 按字节数分割

- 查看打开的文件

        # lsof -c mysql     //查看mysql进程打开的文件

- 查看目录下的文件数,包括子目录

        # find ./ -type f | wc -l
        # ls -l | grep '^-' | wc -l

- 删除空行

        # sed '/^$/d' file.txt

- find

        # find /tmp -type f -iname "*.jpg" -ctime +100 | wc -l        //查找100天以前的jpg文件  -ctime -n指n天以内，+n指n天以前

        # find /tmp -size 0 -exec rm {} \;      // 产出大小为0的文件

        # find /tmp -iname "*.jpg" -exec /usr/bin/gm convert +profile "*" -quality 85 {} {} \;      //查找jpg文件并做convert

        # find . -exec grep 'hello' {} \; -print  //当前目录查找包含hello内容的文件并打印

- 按行数截取文件

        # sed -n '3,10p' myfile > newfile

- 命令行参数

    *    $0 ： ./test.sh,即命令本身，相当于C/C++中的argv[0]
    *    $1 ： -f,第一个参数.
    *    $2 ： config.conf
    *    $3, $4 ... ：类推。
    *    $#  参数的个数，不包括命令本身，上例中$#为4.
    *    $@ ：参数本身的列表，也不包括命令本身，如上例为 -f config.conf -v --prefix=/home
    *    $* ：和$@相同，但"$*" 和 "$@"(加引号)并不同，"$*"将所有的参数解释成一个字符串，而"$@"是一个参数数组。
