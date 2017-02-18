:title: Flask框架之Jinja2模板设计文档
:author: moore
:date: 2017-02-18 14:43:15
:modified: 2017-02-18 14:43:15
:category: Documentation
:tags: Flask, Jinja2, Template, Design, Translation
:slug: Flask框架之Jinja2模板设计文档
:summary: [翻译向]对Jinja2官方文档中的模板设计语法进行翻译，并添加部分个人领悟说明


.. note:: 本博文基于Jinja2 v2.9官方文档的相关内容



模板设计师文档
==============

本文档描述了Jinja2模板引擎的语法以及语义，有助于Jinja模板创建者作为参考文档查阅使用。
作为模板引擎来说，Jinja非常灵活，故这里展示的代码可能由于您应用配置的细微不同而最终效果不同，
这些不同可能来自于 `分隔符(delimiters)` 或 `未定义值(undefined values)` 的行为。


摘要
----

Jinja模板是一个简单的纯文本文件。Jinja可以生成任何基于文本格式的文件，如：HTML，XML，CSV，
LaTex等。Jinja模板不需要有特定的扩展名，如 ``.html`` ， ``.xml`` 或任何其他扩展名皆可。

一个模板文件包含 **变量** (variables) 和/或 **表达式** (expressions)，
他们将在模板文件被渲染时替换为值。Jinja模板语法受启发于 **Django** 和 **Python** 。

下面是一个最简单的模板，使用默认的Jinja配置，来阐明一些基本要素。稍后将在本文档的中进行详细说明:

.. code-block:: html+jinja

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>My Webpage</title>
    </head>
    <body>
        <ul id="navigation">
        {% for item in navigation %}
            <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
        {% endfor %}
        </ul>

        <h1>My Webpage</h1>
        {{ a_variable }}

        {# a comment #}
    </body>
    </html>

下面的例子将展示默认配置设置。开发者可以将语法配置从 ``{% foo %}`` 修改为
``<% foo %>`` ，或者其他类似的语法规则。

存在很多各种各样的分隔符。Jinja默认的分隔符配置如下：

* ``{% ... %}`` 用于语句 (Statements)
* ``{{ ... }}`` 用于打印模板输出的表达式 (Expressions)
* ``{# ... #}`` 用于不包含在模板输出中的注释 (Comments)
* ``#  ... ##`` 用于行注释 (Line Statements)
