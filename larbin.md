about Larbin...
=======================


- 配置
    
    
- 提高特定网站的爬行速度

    - 将larbin.conf里面的waitDuration设置为1
    - 将types.h里面的maxUrlsBySite修改为254；
    - 将main.cc里面的代码做如下修改：

            // see if we should read again urls in fifowait
            if ((global::now % 30) == 0) {
                global::readPriorityWait = global::URLsPriorityWait->getLength();
                global::readWait = global::URLsDiskWait->getLength();
            }
            if ((global::now % 30) == 15) {
                global::readPriorityWait = 0;
                global::readWait = 0;
            }



