about Bash...
==============

eg
---

    - 得到字符串md5

        # echo -n 123 | md5sum | awk '{print $1}'
        # printf 123 | md5sum | awk '{print $1}'

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

    - if

        if [ $a -eq 0 ];then
            ...
        fi

    - 取随机数

        `echo $RANDOM | md5sum | cut -b 1-6`

    - 取文件的crc

        cksum file | awk '{print $1}'

    - 


