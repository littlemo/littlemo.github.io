:title: Linux磁盘分区&挂载&同步
:author: moore
:date: 2016-12-14 11:09:21
:modified: 2017-01-24 16:49:29
:category: Tutorial
:tags: Ubuntu, VPS, Linux, Disk, Partition, Mount
:slug: Linux磁盘分区&挂载&同步
:summary: Linux磁盘设置实操指导


磁盘分区
========


显示硬盘及所属分区情况
----------------------

.. code-block:: console

    $ sudo fdisk -l
    Disk /dev/vda: 21.5 GB, 21474836480 bytes
    255 heads, 63 sectors/track, 2610 cylinders, total 41943040 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000e8237

       Device Boot      Start         End      Blocks   Id  System
    /dev/vda1   *        2048    41943039    20970496   83  Linux

    Disk /dev/vdb: 53.7 GB, 53687091200 bytes
    16 heads, 63 sectors/track, 104025 cylinders, total 104857600 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x00000000

    Disk /dev/vdb doesn't contain a valid partition table


对新硬盘进行分区
----------------

此处将一块50G硬盘创建为扩展分区，并在其中平分两个逻辑分区

.. code-block:: console

    $ sudo fdisk /dev/
    Display all 194 possibilities? (y or n)
    $ sudo fdisk /dev/vdb
    Device contains neither a valid DOS partition table, nor Sun, SGI or OSF disklabel
    Building a new DOS disklabel with disk identifier 0x392faad4.
    Changes will remain in memory only, until you decide to write them.
    After that, of course, the previous content won't be recoverable.

    Warning: invalid flag 0x0000 of partition table 4 will be corrected by w(rite)

    Command (m for help): m
    Command action
       a   toggle a bootable flag
       b   edit bsd disklabel
       c   toggle the dos compatibility flag
       d   delete a partition
       l   list known partition types
       m   print this menu
       n   add a new partition
       o   create a new empty DOS partition table
       p   print the partition table
       q   quit without saving changes
       s   create a new empty Sun disklabel
       t   change a partition's system id
       u   change display/entry units
       v   verify the partition table
       w   write table to disk and exit
       x   extra functionality (experts only)

    Command (m for help): p

    Disk /dev/vdb: 53.7 GB, 53687091200 bytes
    16 heads, 63 sectors/track, 104025 cylinders, total 104857600 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x392faad4

       Device Boot      Start         End      Blocks   Id  System

    Command (m for help): n
    Partition type:
       p   primary (0 primary, 0 extended, 4 free)
       e   extended
    Select (default p): e
    Partition number (1-4, default 1):
    Using default value 1
    First sector (2048-104857599, default 2048):
    Using default value 2048
    Last sector, +sectors or +size{K,M,G} (2048-104857599, default 104857599):
    Using default value 104857599

    Command (m for help): p

    Disk /dev/vdb: 53.7 GB, 53687091200 bytes
    16 heads, 63 sectors/track, 104025 cylinders, total 104857600 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x392faad4

       Device Boot      Start         End      Blocks   Id  System
    /dev/vdb1            2048   104857599    52427776    5  Extended

    Command (m for help): n
    Partition type:
       p   primary (0 primary, 1 extended, 3 free)
       l   logical (numbered from 5)
    Select (default p): l
    Adding logical partition 5
    First sector (4096-104857599, default 4096):
    Using default value 4096
    Last sector, +sectors or +size{K,M,G} (4096-104857599, default 104857599): +52426751

    Command (m for help): n
    Partition type:
       p   primary (0 primary, 1 extended, 3 free)
       l   logical (numbered from 5)
    Select (default p): l
    Adding logical partition 6
    First sector (52432896-104857599, default 52432896):
    Using default value 52432896
    Last sector, +sectors or +size{K,M,G} (52432896-104857599, default 104857599):
    Using default value 104857599

    Command (m for help): p

    Disk /dev/vdb: 53.7 GB, 53687091200 bytes
    16 heads, 63 sectors/track, 104025 cylinders, total 104857600 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x392faad4

       Device Boot      Start         End      Blocks   Id  System
    /dev/vdb1            2048   104857599    52427776    5  Extended
    /dev/vdb5            4096    52430847    26213376   83  Linux
    /dev/vdb6        52432896   104857599    26212352   83  Linux

    Command (m for help): w
    The partition table has been altered!

    Calling ioctl() to re-read partition table.
    Syncing disks.


硬盘格式化
==========


分别格式化两个新创建的逻辑分区为ext4格式
----------------------------------------

.. code-block:: console

    $ sudo mkfs.ext4 /dev/vdb5
    mke2fs 1.42.9 (4-Feb-2014)
    Filesystem label=
    OS type: Linux
    Block size=4096 (log=2)
    Fragment size=4096 (log=2)
    Stride=0 blocks, Stripe width=0 blocks
    1638400 inodes, 6553344 blocks
    327667 blocks (5.00%) reserved for the super user
    First data block=0
    Maximum filesystem blocks=4294967296
    200 block groups
    32768 blocks per group, 32768 fragments per group
    8192 inodes per group
    Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
        4096000

    Allocating group tables: done
    Writing inode tables: done
    Creating journal (32768 blocks): done
    Writing superblocks and filesystem accounting information: done

    $ sudo mkfs.ext4 /dev/vdb6
    mke2fs 1.42.9 (4-Feb-2014)
    Filesystem label=
    OS type: Linux
    Block size=4096 (log=2)
    Fragment size=4096 (log=2)
    Stride=0 blocks, Stripe width=0 blocks
    1638400 inodes, 6553088 blocks
    327654 blocks (5.00%) reserved for the super user
    First data block=0
    Maximum filesystem blocks=4294967296
    200 block groups
    32768 blocks per group, 32768 fragments per group
    8192 inodes per group
    Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
        4096000

    Allocating group tables: done
    Writing inode tables: done
    Creating journal (32768 blocks): done
    Writing superblocks and filesystem accounting information: done


重新查看磁盘信息
----------------

确保之前操作正确无误

.. code-block:: console

    $ sudo fdisk -l

    Disk /dev/vda: 21.5 GB, 21474836480 bytes
    255 heads, 63 sectors/track, 2610 cylinders, total 41943040 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000e8237

       Device Boot      Start         End      Blocks   Id  System
    /dev/vda1   *        2048    41943039    20970496   83  Linux

    Disk /dev/vdb: 53.7 GB, 53687091200 bytes
    7 heads, 22 sectors/track, 680893 cylinders, total 104857600 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x392faad4

       Device Boot      Start         End      Blocks   Id  System
    /dev/vdb1            2048   104857599    52427776    5  Extended
    /dev/vdb5            4096    52430847    26213376   83  Linux
    /dev/vdb6        52432896   104857599    26212352   83  Linux

.. caution:: 此步验证十分重要，如果之前的操作存在错误，如：误格式化，将造成此处的磁盘分区表与预期不同


挂载磁盘分区
============


挂载逻辑分区到/mnt下
--------------------

将准备使用的逻辑分区暂时挂载到 ``/mnt`` 下，便于之后操作数据同步

.. code-block:: console

    # 挂载分区到一个目录下，此处使用/mnt
    $ sudo mount /dev/vdb5 /mnt/

    # 查看挂载结果，是否成功
    $ sudo df -lh
    Filesystem      Size  Used Avail Use% Mounted on
    udev            487M  4.0K  487M   1% /dev
    tmpfs           100M  352K  100M   1% /run
    /dev/vda1        20G  3.4G   16G  19% /
    none            4.0K     0  4.0K   0% /sys/fs/cgroup
    none            5.0M     0  5.0M   0% /run/lock
    none            497M   24K  497M   1% /run/shm
    none            100M     0  100M   0% /run/user
    /dev/vdb5        25G   44M   24G   1% /mnt


同步分区数据
============


将现有数据同步到刚挂载的逻辑分区中
----------------------------------

此处为演示，将 ``/var/www`` 内容同步到挂载分区后的 ``/mnt`` 中，一般情况下，Web服务器的此目录经常单独挂载

.. code-block:: console

    # 执行同步操作
    $ sudo rsync -a /var/www/ /mnt/

    # 将原路径改名备份
    $ sudo mv /var/www /var/www_bk


设置启动挂载配置文件
====================


修改系统启动挂载配置文件
------------------------

其中第二行即为新添加的挂载配置，具体每列的配置方法&可选项，可查看开头提供的参考文档

.. code-block:: console

    $ sudo cat /etc/fstab
    /dev/vda1            /                    ext3       noatime,acl,user_xattr 1 1
    /dev/vdb5            /var/www             ext4       defaults              0 0
    proc                 /proc                proc       defaults              0 0
    sysfs                /sys                 sysfs      noauto                0 0
    debugfs              /sys/kernel/debug    debugfs    noauto                0 0
    devpts               /dev/pts             devpts     mode=0620,gid=5       0 0


执行挂载配置命令
----------------

执行刚修改的 ``/etc/fstab`` 文件，验证是否成功

.. code-block:: console

    # 记得先将之前为了同步操作而挂载的分区先卸载
    $ sudo umount /dev/vdb5

    # 确认目标分区已正确卸载
    $ sudo df -lh
    Filesystem      Size  Used Avail Use% Mounted on
    udev            487M  4.0K  487M   1% /dev
    tmpfs           100M  352K  100M   1% /run
    /dev/vda1        20G  3.4G   16G  19% /
    none            4.0K     0  4.0K   0% /sys/fs/cgroup
    none            5.0M     0  5.0M   0% /run/lock
    none            497M   24K  497M   1% /run/shm
    none            100M     0  100M   0% /run/user

    # 执行 /etc/fstab 挂载配置
    $ sudo mount -a

    # 验证是否挂载成功
    $ sudo df -lh
    Filesystem      Size  Used Avail Use% Mounted on
    udev            487M  4.0K  487M   1% /dev
    tmpfs           100M  352K  100M   1% /run
    /dev/vda1        20G  3.4G   16G  19% /
    none            4.0K     0  4.0K   0% /sys/fs/cgroup
    none            5.0M     0  5.0M   0% /run/lock
    none            497M   24K  497M   1% /run/shm
    none            100M     0  100M   0% /run/user
    /dev/vdb5        25G  216M   24G   1% /var/www


确认无误，重启服务器
--------------------

.. code-block:: console

    $ sudo reboot


.. rubric:: 参考文章

#. `Ubuntu环境下挂载新硬盘 <http://zwkufo.blog.163.com/blog/static/258825120141283942244/>`_
#. `rsync同步常用命令 <http://blog.csdn.net/niushuai666/article/details/16880061>`_
#. `Linux命令-自动挂载文件/etc/fstab功能详解 <http://www.cnblogs.com/qiyebao/p/4484047.html>`_
