about screen
=======================
    
> GNU Screen是一个基于文本的全屏窗口管理器，一个Screen会话可以在一个物理终端上模拟多个窗口，每个窗口中可以运行不同的进程。Screen一个典型的应用就是在其创建的虚拟终端窗口中运行交互性的Shell程序，例如bash，这样就可以在一个终端上打开多个bash进行不同的操作了。

查看属于当前用户的所有Screen会话

    root@hostname:~# screen -ls
    There is a screen on:
        1718.pts-0.bank82   (2012年04月05日 13时53分51秒) (Detached)
    1 Socket in /var/run/screen/S-root.

其中每个会话的都由其PID和名称来标识，可以通过指定PID或名称来恢复指定的Screen会话：

    screen -r 1718
    screen -r pts-0

下面可以实现会话共享,意思就是在不同地方登陆,就像面对同一个显示器

    screen -x

退出当前screen,而不是杀死:

    Ctrl+a d

如果显示使用下面命令强制将这个会话从它所在的终端分离，转移到新的终端上来：

    screen -d


快捷键: 其中的 `Ctrl+a c` ,表示先按 `ctrl+a` , 松开再按 `c`

<table>
<tr><td><b>Key</b></td><td><b>Action</b></td><td><b>Notes</b></td></tr>
  <tr><td nowrap>Ctrl+a c</td><td>new window</td><td>&nbsp;</td></tr>
  <tr><td nowrap>Ctrl+a n</td><td>next window</td><td>I bind F12 to this</td></tr>
  <tr><td nowrap>Ctrl+a p</td><td>previous window</td><td>I bind F11 to this</td></tr>
  <tr><td nowrap>Ctrl+a &quot;</td><td>select window from list</td><td>I have window list in the status line</td></tr>
  <tr><td nowrap>Ctrl+a Ctrl+a</td><td>previous window viewed</td><td>&nbsp;</td></tr>
<tr><td><b>&nbsp;</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>
  <tr><td nowrap>Ctrl+a S</td><td>split terminal horizontally into regions</td><td>Ctrl+a c to create new window there</td></tr>
  <tr><td nowrap>Ctrl+a |</td><td>split terminal vertically into regions</td><td>Requires debian/ubuntu patched screen 4.0</td></tr>
  <tr><td nowrap>Ctrl+a :resize</td><td>resize region</td><td>&nbsp;</td></tr>
  <tr><td nowrap>Ctrl+a :fit</td><td>fit screen size to new terminal size</td><td>Ctrl+a F is the same. Do after resizing xterm</td></tr>
  <tr><td nowrap>Ctrl+a :remove</td><td>remove region</td><td>Ctrl+a X is the same</td></tr>
  <tr><td nowrap>Ctrl+a tab</td><td>Move to next region</td><td>&nbsp;</td></tr>
<tr><td><b>&nbsp;</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>
  <tr><td nowrap>Ctrl+a d</td><td>detach screen from terminal</td><td>Start screen with -r option to reattach</td></tr>
  <tr><td nowrap>Ctrl+a A</td><td>set window title</td><td>&nbsp;</td></tr>
  <tr><td nowrap>Ctrl+a x</td><td>lock session</td><td>Enter user password to unlock</td></tr>
  <tr><td nowrap>Ctrl+a [</td><td>enter scrollback/copy mode</td><td>Enter to start and end copy region. Ctrl+a ] to leave this mode</td></tr>
  <tr><td nowrap>Ctrl+a ]</td><td>paste buffer</td><td>Supports pasting between windows</td></tr>
  <tr><td nowrap>Ctrl+a &gt;</td><td>write paste buffer to file</td><td>useful for copying between screens</td></tr>
  <tr><td nowrap>Ctrl+a &lt;</td><td>read paste buffer from file</td><td>useful for pasting between screens</td></tr>
<tr><td><b>&nbsp;</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>
  <tr><td nowrap>Ctrl+a ?</td><td>show key bindings/command names</td><td>Note unbound commands only in man page</td></tr>
  <tr><td nowrap>Ctrl+a :</td><td>goto screen command prompt</td><td>up shows last command entered</td></tr>
</table>


END,GOOD LUCK!
--------------
