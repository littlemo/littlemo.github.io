:title: Linux根据类型快速设置访问权限
:author: moore
:date: 2016-12-07 21:55:02
:modified: 2017-01-24 16:31:44
:category: Tips
:tags: Linux, Authority
:slug: Linux根据类型快速设置访问权限
:summary: 一个根据类型快速区分设置权限的方法


小技巧
======

在查看MediaWiki部署中发现一个快速设置文件&路径访问权限的方法，如下：

.. code-block:: console

    $ find . -type f -exec chmod 644 {} \;
    $ find . -type d -exec chmod 755 {} \;

原理为 ``find`` 指定类型的文件/路径，执行 ``chmod`` 操作设置访问权限

.. attention:: 由于此方法为查找指定类型文件并分别执行 ``chmod`` 操作，故效率较低， **切忌** 对大量文件使用

.. rubric:: 参考文章

#. `手册:安装 MediaWiki <https://www.mediawiki.org/wiki/Manual:Installing_MediaWiki/zh>`_
