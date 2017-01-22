:title: Ubuntu系统升级异常处理
:author: moore
:date: 2016-09-07 15:20:42
:modified: 2016-09-07 15:20:42
:category: Tutorial
:tags: Ubuntu, Server, Update
:slug: Ubuntu系统升级异常处理
:summary: Ubuntu跨小版本升级时遇到的依赖缺失

升级异常
========

The required dependency 'apt (>= 1.0.1ubuntu2.13)' is not installed.
--------------------------------------------------------------------

遇到此异常一般是由于从14.04直接跨小版本升级造成的系统工具缺失，需要先升级到`14.04`的最新小版本`14.04.5`再进行跨版本升级即可，具体操作方法见参考文章

.. rubric:: 参考文章

#. `14.04 --> 16.04 failed; apt (>= 1.0.1ubuntu2.13)' is not installed <http://askubuntu.com/questions/777013/14-04-16-04-failed-apt-1-0-1ubuntu2-13-is-not-installed>`_
