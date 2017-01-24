:title: Docker创建Container时的Restart策略设置
:author: moore
:date: 2016-12-09 11:22:14
:modified: 2017-01-24 16:39:54
:category: Analysis
:tags: Docker, Container, Restart, Config
:slug: Docker创建Container时的Restart策略设置
:summary: 分析Docker的Restart策略，以及列举设置方式
:status: draft


.. note::

    #. 该文章基于的 ``Docker`` 版本为: ``1.12.3, build 6b644ec``

命令行工具参数 --restart
========================

.. rubric:: 参考文章

#. `Docker run reference <https://docs.docker.com/engine/reference/run/#restart-policies---restart>`_
#. `docker run <https://docs.docker.com/engine/reference/commandline/run/#/restart-policies---restart>`_
