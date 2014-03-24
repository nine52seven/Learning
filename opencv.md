study opencv...
==============

> [OpenCV](http://www.opencv.org/) 的全称是Open Source Computer Vision Library，是一个跨平台的计算机视觉库。OpenCV是由英特尔公司发起并参与开发，以BSD许可证授权发行，可以在商业和研究领域中免费使用。OpenCV可用于开发实时的图像处理、计算机视觉以及模式识别程序。该程序库也可以使用英特尔公司的IPP进行加速处理。

安装
----
下载最新的源代码,解压,比如: opencv-2.4.8

    $ cd ~/opencv.2.4.8  # the directory should contain CMakeLists.txt, INSTALL etc.
    $ mkdir  build       # create the output directory
    $ cd build
    $ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
    $ make      # long time
    $ sudo make install

如果`/etc/ld.so.conf.d/libc.conf`中没有`/usr/local/lib`路径,添加上

    $ sudo ldconfig      #

或者:

    $ export LD_LIBRARY_PATH=/usr/local/lib
    $ sudo ldconfig

依赖软件:

    $ apt-get install make cmake pkg-config python python-dev python-numpy g++


编译安装gearman:

    $ ./configure
    $ make
    $ make install

依赖软件:

    $ apt-get install libboost1.48-dev libboost-program-options-dev gperf uuid-dev libevent-dev

    $ apt-get install libreadline-dev libncurses5-dev libpcre3-dev libssl-dev

安装gearman for php:

    $ pecl install gearman

安装supervisor:

    $ apt-get install supervisor

配置样例

[program:gearman]
command= /usr/sbin/gearmand -L 100.79.118.89 -d
process_name=%(program_name)s
numprocs=1
#process_name=%(program_name)s_%(process_num)02d
#numprocs=2
#directory=/my/worker/direct
autostart=true
autorestart=true
user=root
stdout_logfile=/var/log/supervisor/gearman_stdout.log
stdout_logfile_maxbytes=1MB
stderr_logfile=/var/log/supervisor/gearman_stderr.log
stderr_logfile_maxbytes=1MB

[program:getfeature_worker]
command= /usr/bin/php /home/worksinfo/getfeature_bat_worker.php
#process_name=%(program_name)s
#numprocs=1
process_name=%(program_name)s_%(process_num)02d
numprocs=2
#directory=/my/worker/direct
autostart=true
autorestart=true
user=root
stdout_logfile=/var/log/supervisor/getfeature_worker_stdout.log
stdout_logfile_maxbytes=1MB
stderr_logfile=/var/log/supervisor/getfeature_worker_stderr.log
stderr_logfile_maxbytes=1MB

控制命令:

    $ supervisorctl status
    $ supervisorctl status gearman
    $ supervisorctl stop gearman
    $ supervisorctl start gearman

配置选项:

    process_name=%(program_name)s ＃进程名称，默认是程序名称
    numprocs=1 ＃进程数量
    directory=/tmp ＃路径
    umask=022 ＃掩码
    priority=999 ＃优先级，越大,最后启动,首先关闭
    autorestart=true ＃自动重启
    startsecs=10 ＃启动等待时间（秒）
    startretries=3 ＃启动重试次数
    stopsignal=TERM ＃关闭信号
    stopwaitsecs=10 ＃关闭前等待时间
    user=chrism ＃监控用户权限
    redirect_stderr=false ＃重定向报错输出
    stdout_logfile=/a/path ＃输入重定向为日志
    stdout_logfile_maxbytes=1MB ＃日志大小
    stdout_logfile_backups=10 ＃日志备份
    stdout_capture_maxbytes=1MB
    stderr_logfile=/a/path
    stderr_logfile_maxbytes=1MB
    stderr_logfile_backups=10
    stderr_capture_maxbytes=1MB
    environment=A=1,B=2 ＃预定义环境变量
    serverurl=AUTO ＃系统URL

安装php-handlersocket:

    $ phpize
    $ ./configure  or  ./configure --disable-handlersocket-hsclient
    $ make
    # make install

读取文件
----

    Mat image = imread( argv[1] ,CV_LOAD_IMAGE_GRAYSCALE);

or:

    IplImage * image;
    image=cvLoadImage(argv[1],-1);

存储文件
----

    imwrite(const string& , image);

缩放
----

    int width = image.cols;
    int height = image.rows;
    double dst_size = 200.0;
    double scale = dst_size/max(width,height);
    Size dsize = Size(width*scale,height*scale);
    Mat image2 = Mat(dsize,CV_32S);
    resize(image, image2, dsize);

特征点检查器
----

    int minHessian = 480;
    Ptr<FeatureDetector> detector = Ptr<FeatureDetector>(new SurfFeatureDetector(minHessian));
    vector<KeyPoint> kp;
    detector->detect( image, kp );

描述子
----

    #define DESCRIPTOR_TYPE "SURF" // SURF,SIFT,BRIEF,
    Mat dp;
    Ptr<DescriptorExtractor> de = DescriptorExtractor::create( DESCRIPTOR_TYPE );//描述子
    de->compute( image, kp, dp );

查找匹配点
----

    #define MATCHER_TYPE "FlannBased"    // BruteForce,FlannBased,BruteForce-L1,...
    Ptr<DescriptorMatcher> matcher = DescriptorMatcher::create( MATCHER_TYPE );
    vector< vector<DMatch> > matches;
    matcher->knnMatch( dpL, dpR, matches, 2 ); // L:query, R:train

转换
----

Mat类型侧重于计算，数学性较高，openCV对Mat类型的计算也进行了优化。而CvMat和IplImage类型更侧重于“图像”，openCV对其中的图像操作（缩放、单通道提取、图像阈值操作等）进行了优化。

    - Mat -> IplImage

        IplImage pImg= IplImage(imgMat);    // 假设Mat类型的imgMat图像数据存在



    - IplImage -> Mat

        Mat img(pImg,0);    // 0是不复制

行列转换
----

    cv:Mat mat;
    int rows = mat.rows;
    int cols = mat.cols;

    cv::Size s = mat.size();
    rows = s.height;
    cols = s.width;

END,GOOD LUCK!
--------------
