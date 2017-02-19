:title: Flask框架之Jinja2模板设计文档
:author: moore
:date: 2017-02-18 14:43:15
:modified: 2017-02-18 14:43:15
:category: Documentation
:tags: Flask, Jinja2, Template, Design, Translation
:slug: Flask框架之Jinja2模板设计文档
:summary: [翻译向]对Jinja2官方文档中的模板设计语法进行翻译，并添加部分个人领悟说明


.. note:: 本博文基于Jinja2 v2.9官方文档的相关内容


.. _template-designer-documentation:

模板设计文档
============

本文档描述了Jinja2模板引擎的语法以及语义，有助于Jinja模板创建者作为参考文档查阅使用。
作为模板引擎来说，Jinja非常灵活，故这里展示的代码可能由于您应用配置的细微不同而最终效果不同，
这些不同可能来自于 `分隔符(delimiters)` 或 `未定义值(undefined values)` 的行为。


.. _synopsis:

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

* ``{% ... %}`` 用于语句 ( `Statements <#list-of-control-structures>`_ )
* ``{{ ... }}`` 用于打印模板输出的表达式 ( `Expressions <#expressions>`_ )
* ``{# ... #}`` 用于不包含在模板输出中的注释 ( `Comments <#section-comments>`_ )
* ``#  ... ##`` 用于行语句 ( `Line Statements <#line-statements>`_ )


.. _variables:

变量 (Variables)
----------------

模板变量是通过上下文字典传入模板从而被定义的。

你可以所以改变应用传入到模板中的变量。你也可以访问变量中可能存在的属性或元素。
变量的属性很大程度上取决于提供变量的应用。

除了标准的Python ``__getitem__`` "下标"语法( ``[]`` )外，
你还可以使用一个( ``.`` )来访问变量的属性。

下面两行功能相同：

.. code-block:: jinja

    {{ foo.bar }}
    {{ foo['bar'] }}

重要的是要知道外部的双大括号( *{{}}* )不是变量的一部分，而是打印语句的。
如果你要访问标签内的变量，不用带上外面的大括号。

如果一个变量或属性不存在，你讲得到一个未定义的值( `undefined object`_ )。
你可以用这种值做什么取决于应用配置：如果被打印或迭代，默认的操作是将其输出为一个空字串，
并且对其的所有其他操作都会失败。

.. admonition:: 实现
    :class: note
    :name: notes-on-subscriptions

    为了方便， Jinjia2中的 ``foo.bar`` 在Python层做了如下操作：

    * 检查 *foo* 中被称为 *bar* 的属性 ( ``getattr(foo, 'bar')`` )
    * 如果没有，检查 *foo* 中的 ``'bar'`` 条目 ( ``foo.__getitem__('bar')`` )
    * 如果没有，返回一个未定义对象( `undefined object`_ )

    ``foo['bar']`` 的实现大体相同，但在判断顺序上有一点差异：

    * 检查 *foo* 中的 ``'bar'`` 条目 ( ``foo.__getitem__('bar')`` )
    * 如果没有，检查 *foo* 中被称为 *bar* 的属性 ( ``getattr(foo, 'bar')`` )
    * 如果没有，返回一个未定义对象( `undefined object`_ )

    如果对象拥有同名的条目和属性，那上述的操作执行顺序就非常重要了。
    另外， `attr() <#attr>`_ 过滤器仅查找属性。

    .. _undefined object: http://jinja.pocoo.org/docs/2.9/api/#undefined-types


.. _filters:

过滤器 (Filters)
----------------

变量可以被 **过滤器** 修改。过滤器通过一个管道符号( ``|`` )从变量中分离开，
并且可以通过小括号传入可选参数。多个过滤器可以级联。一个过滤器的输出将被用于下个过滤器的输入。

例如， ``{{ name|striptags|title }}`` 将删除变量 *name* 中的所有HTML
标签，并且作为标题(title-case)输出( ``title(striptags(name))`` )。

接受参数的过滤器在参数周围用小括号包裹，就像函数调用那样。比如：
``{{ listx|join(', ') }}`` 将使用逗号连接一个列表( ``str.join(', ', listx)`` )。

下文的 `内建过滤器列表 <#builtin-filters>`_ 将描述所有内建的过滤器。


.. _tests:

测试 (Tests)
------------

除了过滤器，也有所谓的"测试"可用。测试可用于根据常用表达式测试变量。为了测试一个变量或表达式，
你需要在变量后添加一个 ``is`` 和测试名。例如，为了找出一个变量是否被定义，
你可以添加 ``name is defined`` ，根据当前模板上下文中 ``name`` 是否被定义，表达式将返回
``true`` 或者 ``false`` 。

测试也可以接受参数。如果测试仅接受一个参数，你可以省略小括号。例如，下面的两个表达式效果相同：

.. code-block:: jinja

    {% if loop.index is divisibleby 3 %}
    {% if loop.index is divisibleby(3) %}

下文的 `内建测试列表 <#builtin-tests>`_ 将描述所有内建的测试。


.. _section-comments:

注释 (Comments)
---------------

模板中块注释的默认语法为 ``{# ... #}`` 。这对于注释掉部分模板从而便于调试，
或者为自己或其他模板设计者添加说明信息非常有用：

.. code-block:: jinja

    {# note: commented-out template because we no longer use this
        {% for user in users %}
            ...
        {% endfor %}
    #}


.. _whitespace-control:

空白控制 (Whitespace Control)
-----------------------------

在默认配置中：

* 如果存在单个的行尾换行符，则去除
* 其他空白字符将原样返回，如：空格、制表符、换行符等

如果一个应用配置 Jinja 为块修剪( *trim_blocks* )，模板标签后的第一个换行将被自动移除
（像PHP那样）。也可以设置 *lstrip_blocks* 选项，来去除从一行开始到块开始的制表符和空格。
（如果在块开始前有其他字符，则不会去除任何内容。）

通过开启 *trim_blocks* 和 *lstrip_blocks* ，你可以将块标记放在其自己的杭上，
整个块行将在呈现时被删除，仅保留内容中的空白字符。例如：不设置 *trim_blocks*
和 *lstrip_blocks* 选项，这个模板：

.. code-block:: html+jinja

    <div>
        {% if True %}
            yay
        {% endif %}
    </div>

在 div 中将被渲染为空白行：

.. code-block:: html

    <div>

            yay

    </div>

但是同时开启 *trim_blocks* 和 *lstrip_blocks* ，模板块所在行将被移除，
其余空白字符被保留：

.. code-block:: html

    <div>
            yay
    </div>

你可以通过在块首增加一个加号( ``+`` )从而手动禁用 *lstrip_blocks* 行为：

.. code-block:: html+jinja

    <div>
            {%+ if something %}yay{% endif %}
    </div>

你也可以手动去除模板中的空白。如果你在一个块（如： `For <#for-loop>`_ 标签块），注释，
或变量表达式的开始或结尾添加一个减号( ``-`` )，那么块前或后的空白将被移除：

.. code-block:: jinja

    {% for item in seq -%}
        {{ item }}
    {%- endfor %}

这将产生所有元素，且之间没有空白字符。如果 *seq* 是一个从 ``1`` 到 ``9`` 的数字列表，
输出将为 ``123456789`` 。

如果开启行语句 ( `Line Statements <#line-statements>`_ )，
将自动去除行首前的空白字符。

Jinja2 默认删除行尾换行。为了保留单独的行尾换行，
配置 Jinja 的 *keep_trailing_newline* 。

.. note::

    不要在标签和减号间加空格。

    **有效** ：

    .. code-block:: jinja

        {%- if foo -%}...{% endif %}

    **无效** ：

    .. code-block:: jinja

        {% - if foo - %}...{% endif %}
