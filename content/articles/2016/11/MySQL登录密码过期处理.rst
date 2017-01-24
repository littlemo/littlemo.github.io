:title: MySQL登录密码过期处理
:author: moore
:date: 2016-11-16 23:22:29
:modified: 2017-01-24 11:15:43
:category: Fix
:tags: MySQL, Login, Password, Expired
:slug: MySQL登录密码过期处理
:summary: 在MySQL 5.6版本后增加了安全机制，故DB登录密码会在一定时间后过期


异常说明
========

由于MySQL在5.6版本增加了安全机制，故账户的登录密码会在一定时间后过期，此时需要重新设置密码，以确保可以正常连接数据库

表现为像 ``phpmyadmin`` 这类的数据库管理工具无法正常连接数据库；应用连接时返回异常信息如下：

.. code-block:: console

    Mysql Error 1862: Your password has expired. To log in you must change it using a client that supports expired passwords.

通过终端登录，执行任何命令皆会返回如下信息：

.. code-block:: console

    ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.


解决办法
========

首先我们应重置root账号的密码，终端连接并执行如下命令：（此处以root账户举例，其他账户类似）

.. code-block:: console

    $ mysql -u root -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 4
    Server version: 5.7.9

    Copyright (c) 2000, 2015, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> SET PASSWORD = PASSWORD('XXOOXXOOXXOO');
    Query OK, 0 rows affected, 1 warning (0.00 sec)

    mysql> ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;
    Query OK, 0 rows affected (0.00 sec)

    mysql> flush privileges;
    Query OK, 0 rows affected (0.00 sec)

    mysql> exit
    Bye

.. note::

    #. 此处第二条语句为了方便，牺牲了安全性，即设置root账户密码永不过期
    #. 其中第一条语句的 ``密码`` 与第二条语句的 ``账号信息`` 根据自己实际情况修改

退出后，即可以通过该账号正常连接操作了

.. rubric:: 参考文章

#. `ALTER USER Syntax <https://dev.mysql.com/doc/refman/5.6/en/alter-user.html>`_
#. `Password Expiration Policy <http://dev.mysql.com/doc/refman/5.7/en/password-expiration-policy.html>`_
#. `Reset MySQL root password using ALTER USER statement after install on Mac <http://stackoverflow.com/questions/33467337/reset-mysql-root-password-using-alter-user-statement-after-install-on-mac>`_
