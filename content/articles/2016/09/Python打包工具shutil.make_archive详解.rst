:title: Python打包工具shutil.make_archive详解
:author: moore
:date: 2016-09-23 21:19:01
:modified: 2017-01-23 16:31:15
:category: Analysis
:tags: Python, Shutil, Archive
:slug: Python打包工具shutil.make_archive详解
:summary: Python源码打包方式(非发布打包)

方法说明
========

.. code-block:: py3

    shutil.make_archive(base_name, format[, root_dir[, base_dir[, verbose[, dry_run[, owner[, group[, logger]]]]]]])

用于创建打包文件(如：zip或tar)，并返回文件的 ``绝对路径`` 名称

参数说明
--------

* ``base_name`` : 创建的目标文件名，包括路径，减去任何特定格式的扩展。
* ``format`` : 压缩包格式。"zip", "tar", "bztar"或"gztar"中的一个。
* ``root_dir`` : 打包时切换到的根路径。也就是说，开始打包前，会先执行路径切换，切换到root_dir所指定的路径。默认值为当前路径
* ``base_dir`` : 开始打包的路径。也就是说，该命令会对base_dir所指定的路径进行打包，默认值为 ``root_dir`` ，即打包切换后的当前目录。亦可指定某一特定子目录，从而实现打包的文件包含此统一的前缀路径
* ``owner`` 和 ``group`` 为创建tar包时使用，默认为用户当前的 ``owner`` & ``group``

测试用例
--------

此处官方文档提供了一个用例为使用默认 ``base_dir`` 的情况，即打包对象为 ``root_dir`` 下的全部文件&目录，如下:

.. code-block:: pycon

    >>> from shutil import make_archive
    >>> import os
    >>> archive_name = os.path.expanduser(os.path.join('~', 'myarchive'))
    >>> root_dir = os.path.expanduser(os.path.join('~', '.ssh'))
    >>> make_archive(archive_name, 'gztar', root_dir)
    '/Users/tarek/myarchive.tar.gz'

压缩包内容结果：

.. code-block:: console

    $ tar -tzvf /Users/tarek/myarchive.tar.gz
    drwx------ tarek/staff       0 2010-02-01 16:23:40 ./
    -rw-r--r-- tarek/staff     609 2008-06-09 13:26:54 ./authorized_keys
    -rwxr-xr-x tarek/staff      65 2008-06-09 13:26:54 ./config
    -rwx------ tarek/staff     668 2008-06-09 13:26:54 ./id_dsa
    -rwxr-xr-x tarek/staff     609 2008-06-09 13:26:54 ./id_dsa.pub
    -rw------- tarek/staff    1675 2008-06-09 13:26:54 ./id_rsa
    -rw-r--r-- tarek/staff     397 2008-06-09 13:26:54 ./id_rsa.pub
    -rw-r--r-- tarek/staff   37192 2010-02-06 18:23:10 ./known_hosts

此处Moore补充一个使用指定 ``base_dir`` 的测试用例，用来打出包含前缀路径的压缩包(毕竟打出一个没有前缀目录的压缩包，某些情况下解包到当前路径是件比较崩溃的事情)，如下：

.. code-block:: pycon

    >>> from shutil import make_archive
    >>> import os
    >>> archive_name = os.path.expanduser(os.path.join('~', 'myarchive'))
    >>> root_dir = os.path.expanduser('~')
    >>> base_dir = '.ssh'
    >>> make_archive(archive_name, 'gztar', root_dir, base_dir)
    '/Users/tarek/myarchive.tar.gz'

压缩包内容结果：

.. code-block:: console

    $ tar -tzvf /Users/tarek/myarchive.tar.gz
    drwx------ tarek/staff       0 2010-02-01 16:23:40 .ssh/
    -rw-r--r-- tarek/staff     609 2008-06-09 13:26:54 .ssh/authorized_keys
    -rwxr-xr-x tarek/staff      65 2008-06-09 13:26:54 .ssh/config
    -rwx------ tarek/staff     668 2008-06-09 13:26:54 .ssh/id_dsa
    -rwxr-xr-x tarek/staff     609 2008-06-09 13:26:54 .ssh/id_dsa.pub
    -rw------- tarek/staff    1675 2008-06-09 13:26:54 .ssh/id_rsa
    -rw-r--r-- tarek/staff     397 2008-06-09 13:26:54 .ssh/id_rsa.pub
    -rw-r--r-- tarek/staff   37192 2010-02-06 18:23:10 .ssh/known_hosts

.. tip:: 由于此处的 ``.ssh`` 是隐藏文件夹，所以解压后从文件管理器中可能是看不到的

.. rubric:: 参考文章

#. `Python官方文档 <https://docs.python.org/2/library/shutil.html#archiving-operations>`_
