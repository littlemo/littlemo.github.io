:title: 修复远程登录Linux服务器时遇到的Perl本地警告
:author: moore
:date: 2016-09-08 14:09:06
:modified: 2016-09-08 14:09:06
:category: Fix
:tags: Ubuntu, Linux, Perl
:slug: 修复远程登录Linux服务器时遇到的Perl本地警告
:summary: 部署VPS时遇到的一个警告

warning: Falling back to the standard locale ("C").
===================================================

异常信息
--------

.. code-block:: BASH

    perl: warning: Setting locale failed.
    perl: warning: Please check that your locale settings:
            LANGUAGE = "en_US:",
            LC_ALL = (unset),
            LC_CTYPE = "zh_CN.UTF-8",
            LANG = "en_US.UTF-8"
        are supported and installed on your system.
    perl: warning: Falling back to the standard locale ("C").

原因分析
--------

一般情况下尝发生在MacOS通过SSH远程登录Linux服务器时

主要是因为 ``sshd_config`` 中有一条配置项为 ``AcceptEnv LANG LC_*`` ，这使得shell的session使用了本地主机的Env，而如果本地主机没有设置这些参数，就会报出如上错误。

分析验证
--------

SSH远程登录后尝试执行如下命令：

.. code-block:: BASH

    $ perl -e exit
    perl: warning: Setting locale failed.
    perl: warning: Please check that your locale settings:
            LANGUAGE = "en_US:",
            LC_ALL = (unset),
            LC_CTYPE = "zh_CN.UTF-8",
            LANG = "en_US.UTF-8"
        are supported and installed on your system.
    perl: warning: Falling back to the standard locale ("C").
    $ LC_ALL=C perl -e exit

手动添加 ``LC_ALL=C`` 前缀，执行结果为空，不再报错，则证明我们已找到问题原因所在

问题解决
--------

既然是由于缺少环境变量定义造成的异常，解决方法就很简单了，增加定义或链接时传入即可

方法一：增加环境变量定义
^^^^^^^^^^^^^^^^^^^^^^^^

向宿主机的Profile文件中增加如下定义：

.. code-block:: BASH

    # Setting for the new UTF-8 terminal
    export LC_ALL=C

这样就会在远程登录shell的时候自动执行profile文件，定义缺失的环境变量了，弥补客户机提供的变量不全的情况。这种方法也是网上大部分文章提供的，然而明白前因后果的您一定也发现了，这并不是一个很好的解决方法。这种解法等于一部分配置是客户机提供的，一部分配置是客户机登录后，用户Shell的profile提供的，而且后者会对前者造成覆盖，还有一点，这只解决的当前账户的问题，本机使用其他账户登录该宿主机的时候依旧会遇到此问题，非吾之所求也

方法二：关闭接受客户机env功能
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

即使用宿主机的环境配置，这样所需的环境变量自然都是系统已定义好的，不会出现未定义的情况，设置方式如下：

.. code-block:: BASH

    sudo emacs /etc/ssh/sshd_config # 在AcceptEnv LANG LC_*行首增加注释符'#'


这样的好处是，解决了所有账户/客户机登录此服务器时的问题，毕竟已经使用服务器自认的环境变量了。但依旧存在一个小问题，即等于写死了配置，所以当客户机环境(尤其是编码)与服务器存在较大差异时，问题就大了，此时我们还是需要服务器使用客户机环境的，故下述方法三方为正道！

[推荐]方法三：修改本地Env配置，加入目标变量
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

既然如此，我们可以把方法一中增加的环境变量定义在客户机中，这样就可以兼顾到两者了，既满足本机多账户登录时不用重复设置，又可以灵活的使用本地Env，方法如下：

.. code-block:: BASH

    # 对于Bash用户，修改~/.bash_profile
    export LC_ALL=C

    # 对于zsh用户，修改~/.zshrc
    LC_ALL=C

.. rubric:: 参考文章

#. `How can I fix a locale warning from Perl? <http://stackoverflow.com/questions/2499794/how-can-i-fix-a-locale-warning-from-perl>`_
