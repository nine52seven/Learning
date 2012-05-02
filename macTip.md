some tip about mac...
=====================

卸载xcode
---------

    sudo /Developer/Library/uninstall-devtools --mode=all

下载ssh-copy-id
---------------

    sudo curl ‘https://raw.github.com/gist/1639381/eea46277ba544fcbd0a0768e8b3f854880ddb772/ssh-copy-id’ -o /usr/bin/ssh-copy-id
    sudo chmod +x /usr/bin/ssh-copy-id
eg:

    ssh-copy-id -i ~/.ssh/id_rsa.pub username@host



END,GOOD LUCK!
--------------