"""
#=========================================
#     FileName: auto_eyun.py
#   说明: 法师厄运无限刷小鬼自动脚本
#   用法: 卡小鬼成功后,进洞, 套寒冰护体, 法力护盾, 等第一波小鬼全部刷新后, 运行这个脚本
#       此脚本30秒一个循环,可以事先做几组水,设置的5分钟做一次水,正常情况30秒一瓶, 做一次水10瓶,正好够用5分钟
#=========================================
"""
import pyautogui as p
import time as t,random

p.FAILSAFE = False

# 三秒后运行
t.sleep(1)

# 寒冰护体 9, 法力盾 8
def Hanbing():
    #冰盾
    p.press("9")
    t.sleep(1.3)
    #法力盾
    p.press("8")
    t.sleep(1.3)

# 奥爆 5键
def Aobao():
    obtime = random.randint(4,5)
    for i in range(1, obtime):
        #奥爆 2键
        p.press("5")
        t.sleep(1.4)

#冰甲术 7键 智力 6
def Bingjia():
    p.press("7")
    t.sleep(1.5)
    p.press("6")
    t.sleep(1.3)

#吃喝 4,3
def Chihe():
    p.press("4")
    t.sleep(1.4)
    p.press("3")

#移动鼠标, 控制挂机小号
def MoveMouse():
    a,b = p.size()
    p.moveTo(3*a/4, 3*b/4)
    t.sleep(1)
    p.click()
    t.sleep(0.5)
    p.press("space")
    p.press(random.choice("123"))
    t.sleep(0.5)
    p.moveTo(a/4, b/4)
    p.click()

#随机走动,调整视角
def RandGo():
    p.press(random.choice("wasd"))
    p.dragRel(random.randint(-50,50), 0,button="right")

t_mj = t.time()
t_zs = t.time()
#多少秒循环一次
circle_time = 30
i = 1
print('Press Ctrl-C to quit.')
try:
    while (True):
        this_time = t.time()
        print ("----start : %d 次, at : %s" % (i,t.strftime("%Y-%m-%d %H:%M:%S", t.localtime())))
        print ("    small buff, at:" + t.strftime("%Y-%m-%d %H:%M:%S", t.localtime()))
        Hanbing()

        Aobao()

        #29分钟加智力和冰甲
        if this_time - t_mj >= 29*60 or this_time - t_mj <=1:
            print ("    big buff, at:" + t.strftime("%Y-%m-%d %H:%M:%S", t.localtime()))
            Bingjia()
            t_mj = this_time

        #5分钟做次水
        if this_time - t_zs >= 5*60 :
            print ("    make water, at:" + t.strftime("%Y-%m-%d %H:%M:%S", t.localtime()))
            p.press("1")
            t_zs = this_time
            t.sleep(3)
        RandGo()
        Chihe()
        # MoveMouse()

        #休息
        over_time = t.time() - this_time
        t.sleep(circle_time - over_time)
        i += 1
        print ("----end-----------------------------------")
except KeyboardInterrupt:
    print ('\n')
