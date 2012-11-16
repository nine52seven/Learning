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



