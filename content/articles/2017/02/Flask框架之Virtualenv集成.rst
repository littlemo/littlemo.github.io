:title: Flask框架之Virtualenv集成
:author: moore
:date: 2017-02-06 12:01:30
:modified: 2017-02-06 12:01:30
:category: Tips
:tags: Framework, Flask, Virtualenv, Integration
:slug: Flask框架之Virtualenv集成
:summary: 将Flask相关环境配置集成到Virtualenv中，从而减少开发调试时的环境配置操作


痛点
====

由于Flask中的App设置以及一些debug的标志大都通过 ``env`` 设置，每次执行时单独操作难免遗忘


解决
====

进行Python工程开发时，基本上都会使用 `Virtualenv <https://virtualenv.pypa.io/en/stable/>`_ 工具来实现相关依赖安装，故我们可以借用其环境激活时执行的脚本来完成我们 ``Flask`` 的环境配置


操作流程
--------


创建环境
~~~~~~~~

在工程根路径下创建虚拟环境(venv)

.. code-block:: console

    $ cd path/to/project
    $ virtualenv venv


安装项目依赖
~~~~~~~~~~~~

此处为一个 ``Flask`` 项目，故安装命令如下

.. code-block:: console

    $ pip install flask


添加环境配置
~~~~~~~~~~~~

此步为 **重点** ，即将我们需要的环境配置追加到 ``venv/bin/activate`` 文件的末尾，此处我们加入 ``FLASK_APP`` 与 ``FLASK_DEBUG`` 设置。假设我们的项目入口文件名为 ``hello.py``

.. code-block:: sh

    # Flask相关环境配置
    export FLASK_APP=hello
    export FLASK_DEBUG=1


另外，若要在 ``deactivate`` 的时候一同删除我们添加的配置，需在 ``venv/bin/activate`` 文件中的 ``deactivate ()`` 方法末尾追加上相应的 ``unset`` 命令

.. code-block:: sh

    # 删除Flask相关环境配置
    unset FLASK_APP
    unset FLASK_DEBUG


激活环境
~~~~~~~~

以上即完成了虚拟环境的全部设置操作，接下来可以激活环境看看效果啦！

.. code-block:: console

    $ source venv/bin/activate
    $ flask run
     * Serving Flask app "hello"
     * Forcing debug mode on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger pin code: 126-266-749

激活环境后可以直接运行 ``Flask`` 项目，不用再手动设置环境变量了^_^


.. rubric:: 参考文章

#. `Flask: Command Line Interface <http://flask.pocoo.org/docs/0.12/cli/#virtualenv-integration>`_
