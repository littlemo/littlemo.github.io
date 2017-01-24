:title: 设置SublimeText的Markdown相关配置
:date: 2016-09-05
:modified: 2017-01-21 20:59:33
:Category: Tools
:Tags: SublimeText, Markdown
:slug: 设置SublimeText的Markdown相关配置
:author: moore
:summary: 设置SublimeText的Markdown配置，便于预览、查看

配置Sublime的预览快捷键
=======================

添加 ``sublime-keymap`` ，内容如下：

.. code-block:: json

    {
        "keys": ["alt+m"],
        "command": "markdown_preview",
        "args": {
            "target": "browser",
            "parser": "markdown"
        }
    }

配置MarkdownEditing的配色方案
=============================

默认为亮色系，看时间久了，实在对眼镜眼里太大，故此处将其修改为暗色系配色，写入配色方案如下：

.. hint:: 打开： ``Preferences`` -> ``Package Settings`` -> ``Markdown Editing`` -> ``Markdown GFM Settings`` - ``User``

.. code-block:: json

    {
        "color_scheme": "Packages/MarkdownEditing/MarkdownEditor-Dark.tmTheme",
    }

保存文件，打开一个 ``md`` 文件，看是否生效，若未生效，可能是被SublimeText编辑器的配色方案覆盖掉了，可以尝试修改编辑器配色方案的忽略列表，增加如下条目：

.. hint:: 打开： ``Preferences`` -> ``Settings - User``

.. code-block:: json

    {
        "ignored_packages":
        [
            "Markdown",
        ]
    }

.. rubric:: 参考文章

#. `Sublime Text3的Markdown配置 <http://www.jianshu.com/p/049e2fdb55ae>`_
#. `如何使用Sublime Text 3作为Markdown编辑器 <http://jingyan.baidu.com/article/f006222838bac2fbd2f0c87d.html?st=2&net_type=&bd_page_type=1&os=0&rst=&word=feifeidown>`_
