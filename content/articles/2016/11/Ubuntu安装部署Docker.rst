:title: Ubuntu安装部署Docker
:author: moore
:date: 2016-11-05 12:11:16
:modified: 2017-01-24 15:03:43
:category: Tutorial
:tags: Ubuntu, Docker, Install
:slug: Ubuntu安装部署Docker
:summary: 安装部署官方repo的docker-engine


Docker安装需求
==============

1. Ubuntu版本为为64bit
2. 内核版本大于3.10

.. code-block:: console

    $ uname -r
    3.13.0-95-generic

3. 更新系统软件包列表

.. code-block:: console

    $ sudo apt-get update

4. 验证APT是否从正确的Repo获取到目标app

.. code-block:: console

    $ sudo apt-cache policy docker-engine

    docker-engine:
        Installed: 1.12.2-0~trusty
        Candidate: 1.12.2-0~trusty
        Version table:
       *** 1.12.2-0~trusty 0
              500 https://apt.dockerproject.org/repo/ ubuntu-trusty/main amd64 Packages
              100 /var/lib/dpkg/status
           1.12.1-0~trusty 0
              500 https://apt.dockerproject.org/repo/ ubuntu-trusty/main amd64 Packages
           1.12.0-0~trusty 0
              500 https://apt.dockerproject.org/repo/ ubuntu-trusty/main amd64 Packages

若返回 ``N: Unable to locate package docker-engine`` 则需根据下述方法手动设置Repo源

5. 确保 ``APT`` 工作在 ``https`` 下，且 ``CA`` 证书已被安装

.. code-block:: console

    $ sudo apt-get install apt-transport-https ca-certificates

6. 添加新的 ``GPG`` 密钥

.. code-block:: console

    $ sudo apt-key adv \
                   --keyserver hkp://ha.pool.sks-keyservers.net:80 \
                   --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

7. 查找当前Ubuntu版本对应的Repo链接

===================  ==========
Ubuntu version       Repository
===================  ==========
Precise 12.04 (LTS)  deb https://apt.dockerproject.org/repo ubuntu-precise main
Trusty 14.04 (LTS)   deb https://apt.dockerproject.org/repo ubuntu-trusty main
Wily 15.10           deb https://apt.dockerproject.org/repo ubuntu-wily main
Xenial 16.04 (LTS)   deb https://apt.dockerproject.org/repo ubuntu-xenial main
===================  ==========

8. 执行下属命令，使用本地的Repo链接取代 ``<REPO>``

.. code-block:: console

    $ echo "<REPO>" | sudo tee /etc/apt/sources.list.d/docker.list

9. 更新 ``APT`` 包索引

.. code-block:: console

    $ sudo apt-get update

10. 重复第4步，验证是否从正确的Repo获取到app


安装
====

1. 安装Docker

.. code-block:: console

    $ sudo apt-get install docker-engine

2. 开启Docker守护进程

.. code-block:: console

    $ sudo service docker start

3. 验证Docker以正确安装

.. code-block:: console

    $ sudo docker run hello-world

    Hello from Docker!
    This message shows that your installation appears to be working correctly.

    To generate this message, Docker took the following steps:
     1. The Docker client contacted the Docker daemon.
     2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
     3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
     4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.

    To try something more ambitious, you can run an Ubuntu container with:
     $ docker run -it ubuntu bash

    Share images, automate workflows, and more with a free Docker Hub account:
     https://hub.docker.com

    For more examples and ideas, visit:
     https://docs.docker.com/engine/userguide/

这个命令会下载一个测试镜像并在容器中运行，当容器运行时，将打印一些消息，然后退出

可选配置
========

这章节将包含一些可以使你的Docker在Ubuntu下工作的更好的操作

创建一个Docker群组
------------------

Docker守护进程和Unix socket绑定在一起，而不是TCP端口。默认情况下，Unix socket是属于 ``root`` 用户的，其他用户只能通过 ``sudo`` 访问。所以Docker的守护进程总是运行在 ``root`` 用户下。

为了避免当你使用Docker命令时不得不使用 ``sudo`` ，创建一个名为 ``docker`` 的群组，并将你的用户加到组中。当Docker的守护进程开始时，该用户可以通过 ``docker`` 群组获取到Unix socket的读写权限。

.. caution::

    ``docker`` 群组相当于 ``root`` 用户；关于系统安全性影响的细节，可以查看 `Docker Daemon Attack Surface <https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface>`_

创建 ``docker`` 群组，并加入用户：

1. 使用一个有 ``sudo`` 权限的用户登录到Ubuntu
2. 创建 ``docker`` 群组

.. code-block:: console

    $ sudo groupadd docker

3. 将指定用户加入到 ``docker`` 群组

.. code-block:: console

    $ sudo usermod -aG docker $USER

4. 注销并重新登录

确保你的用户以正确的权限运行

5. 通过不使用 ``sudo`` 运行 ``docker`` 验证是否成功

.. code-block:: console

    $ docker run hello-world

如果获取到类似下面的失败信息：

.. code-block:: console

    Cannot connect to the Docker daemon. Is 'docker daemon' running on this host?

检查你的Shell中 ``DOCKER_HOST`` 环境变量是否为未设置状态。如果设置了， ``unset`` 掉。


.. rubric:: 参考文章

#. `Install Docker on Ubuntu <https://docs.docker.com/engine/installation/linux/ubuntulinux/>`_
#. `在Ubuntu 14.04安装和使用Docker <http://blog.csdn.net/chszs/article/details/47122005>`_
