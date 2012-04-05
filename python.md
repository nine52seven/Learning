python 学习笔记
--------------

### 数据的结构
- **列表 list**
  
    list是处理一组有序项目的数据结构,"[]"包围

        shoplist = ['apple', 'mango', 'carrot', 'banana']
        print 'my shopping list is ', shoplist
    
- **元组**
  
    元组和列表十分类似，只不过元组和字符串一样是 不可变的 即你不能修改元组。
    
    元组通过"()"中用逗号分割的项目定义。
    
    元组通常用在使语句或用户定义的函数能够安全地采用一组值的时候，即被使用的元组的值不会改变。
    
        zoo = ('wolf', 'elephant', 'penguin')
        print 'In zoo have', zoo
    
    含有0个或1个项目的元组:
    
        myempty = ()
        myone = ('one', )   #只有单个元素的必须后面跟","

    
- **字典**
  
    只能使用不可变的对象（比如字符串）来作为字典的键，但是你可以不可变或可变的对象作为字典的值。
    
    key: 必须是不可不变的对象
    
    value: 可以不可变或可变的对象
    
    ``
d = {key1 : value1, key2 : value2 }
    ``
- **序列**
  
    列表、元组和字符串都是序列,序列的两个主要特点是索引操作符和切片操作符
    
  - - -

### 类 class
- **self**
  
    class中的function必须带有self参数,为第一个参数,python中的self等同于java/php中的this
    
    ``
class Person:
        def sayHi(self):
            print 'Hello, how are you?'
p = Person()
p.sayHi()
    ``

- **\_\_init\_\_方法**
  
    \_\_init\_\_方法在类的一个对象被建立时，马上运行

- **\_\_del\_\_方法**
  
    它在对象消逝的时候被调用。对象消逝即对象不再被使用，它所占用的内存将返回给系统作它用。

- **"\_\_"开头**
  
    Python的名称管理体系会有效地把它作为私有变量。
    自己定义的私有变量或方法一般以"_"开头

- **类的继承**
  
    子类的名称后面加上父类的名称
    注意: 子类不会自动调用父类的\_\_init\_\_函数
    
    ``
class member:
    ...
class student(member):
    ...
    ``
    支持多重继承
    
    ``
class member:
    ...
class class:
    ...
class student(member,class):
    ...
    ``

### 方法 method

- **关键字 def**

- **用缩进来表示范围**

- **每个方法,如果没有返回值,都默认的 return None**

- **DocStrings**
    
    文档字符串的惯例是一个多行字符串.
    
    它的首行以大写字母开始，句号结尾。
    
    第二行是空行.
    
    从第三行开始是详细的描述。
    
    可以使用"\_\_doc\_\_"调用
        
    ``
def  testfun():
    """
Testfun().
    ``
    This  function  do  nothing,  just  demostrate  the  use  of  the
    doc  string.
    """
        pass

- **参数默认值**
    
    不能在声明函数形参的时候，先声明有默认值的形参而后声明没有默认值的形参。
    right:
        
    ``
def printValues(name, height = 170, weight = 60)
    ...
error:
def printValues(name, height = 170, weight)
        ...
    ``

- **多参数传递**
    
    关键参数: 方法调用的时候可以不用传递所有参数,使用名字而不是位置来指定
        
    ``
def func(a, b=5, c=10):
    print 'a is', a, 'and b is', b, 'and c is', c
func(3, 7)              # a=3, b=7, c=10
func(25, c=24)          # a=25, b=5, c=24
func(c=50, a=100)       # a=100, b=5, c=50    
    ``

- **任意参数**

    ``
def  printf(format,*arg):
    ...
    ``

    \*arg必须为方法的最后一个参数

    \*表示接受任意多个参数,除了前面的参数,多余的参数都作为一个元组传递,可以通过arg来访问

    ``
def  printf(format,**keyword):
    ...
    ``
    \*\*表示接受任意多个参数,并作为一个"字典"传递.
    
    如果有*arg必须放在**keyword前面

- **方法参数接受顺序**
        
    先接受固定参数,
    
    然后是可选参数,
    
    然后接受任意参数,
    
    最后是带名字的任意参数.

- **静态方法 static**
    
    利用staticmehod(function)的重定义实现，而非关键字
        
    ``
>>> class Clazz:
        def methodA():     #不能有self
            print "Hello, World."
        methodA = staticmethod(methodA)
>>> Clazz.methodA()
Hello, World.
>>> clazz = Clazz()
>>> clazz.methodA()
Hello, World.
    ``

- **特殊的方法**
    
    在类中有一些特殊的方法具有特殊的意义，比如:
    
    - \_\_init\_\_(self,...)
    
        这个方法在新建对象恰好要被返回使用之前被调用。

    - \_\_del\_\_(self)
    
        恰好在对象要被删除之前调用。
        
    - \_\_str\_\_(self)
    
        在我们对对象使用print语句或是使用str()的时候调用。
        
    - \_\_lt\_\_(self,other)
    
        当使用 小于 运算符（<）的时候调用。类似地，对于所有的运算符（+，>等等）都有特殊的方法。
    - \_\_getitem\_\_(self,key)
    
        使用x[key]索引操作符的时候调用。
        
    - \_\_len\_\_(self)	
    
        对序列对象使用内建的len()函数的时候调用。

    这些方法可以实现操作符重载
        
    ``
class P:
    def __call__(self, *arg):   #让class像方法一样,可以调用
        for k in arg:
            print k
p = P()
p("hello","world")
hello
world
    ``

- **and和or的特殊性质**

    ''、[]、()、{}、None在布尔环境中为假,其它任何东西都为真
    
    在布尔环境中从左到右演算表达式的值。
    
    and:返回第一个假值,否则返回最后一个真值
        
    or:返回第一个真值,否则返回最后一个假值
        
    ``
>>> 'a' and 'b'
'b'
>>> '' and 'b'
''
>>> 'a' and 'b' and 'c'
'c'
>>> 'a' or 'b'
'a'
>>> '' or 'b'
'b'
>>> '' or [] or {}
{}
    ``
    and 和 or 的技巧:
    
    bool ? a : b 表达式
    
    ``
>>> a = "first"
>>> b = "second"
>>> 1 and a or b 1
'first'
>>> 0 and a or b 2
'second'
    ``

- **python连接mysql**
    
    使用: [http://mysql-python.sourceforge.net/](http://mysql-python.sourceforge.net/)
    
    api: [http://mysql-python.sourceforge.net/MySQLdb-1.2.2/](http://mysql-python.sourceforge.net/MySQLdb-1.2.2/)
    
    ``
conn = MySQLdb.connect (host = "dbserver",
                        user = "dbusername",
                        passwd = "dbpassword",
                        db = "db")
cursor = conn.cursor()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone()
print "server version:", row[0]
cursor.close ()
conn.close ()
    ``
    
***
END
    
