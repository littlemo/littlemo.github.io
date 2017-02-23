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
* ``{{ ... }}`` 用于打印模板输出的表达式 ( `Expressions <#expressions-statements>`_ )
* ``{# ... #}`` 用于不包含在模板输出中的注释 ( `Comments <#section-comments>`_ )
* ``#  ... ##`` 用于行语句 ( `Line Statements <#line-statement>`_ )


.. _variables:

变量 (Variables)
----------------

模板变量是通过上下文字典传入模板从而被定义的。

您可以所以改变应用传入到模板中的变量。您也可以访问变量中可能存在的属性或元素。
变量的属性很大程度上取决于提供变量的应用。

除了标准的Python ``__getitem__`` "下标"语法( ``[]`` )外，
您还可以使用一个( ``.`` )来访问变量的属性。

下面两行功能相同：

.. code-block:: jinja

    {{ foo.bar }}
    {{ foo['bar'] }}

重要的是要知道外部的双大括号( *{{}}* )不是变量的一部分，而是打印语句的。
如果您要访问标签内的变量，不用带上外面的大括号。

如果一个变量或属性不存在，您讲得到一个未定义的值( `undefined object`_ )。
您可以用这种值做什么取决于应用配置：如果被打印或迭代，默认的操作是将其输出为一个空字串，
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
    另外， `attr() <#attr-func>`_ 过滤器仅查找属性。

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
您需要在变量后添加一个 ``is`` 和测试名。例如，为了找出一个变量是否被定义，
您可以添加 ``name is defined`` ，根据当前模板上下文中 ``name`` 是否被定义，表达式将返回
``true`` 或者 ``false`` 。

测试也可以接受参数。如果测试仅接受一个参数，您可以省略小括号。例如，下面的两个表达式效果相同：

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

通过开启 *trim_blocks* 和 *lstrip_blocks* ，您可以将块标记放在其自己的杭上，
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

您可以通过在块首增加一个加号( ``+`` )从而手动禁用 *lstrip_blocks* 行为：

.. code-block:: html+jinja

    <div>
            {%+ if something %}yay{% endif %}
    </div>

您也可以手动去除模板中的空白。如果您在一个块（如： `For <#for-loop>`_ 标签块），注释，
或变量表达式的开始或结尾添加一个减号( ``-`` )，那么块前或后的空白将被移除：

.. code-block:: jinja

    {% for item in seq -%}
        {{ item }}
    {%- endfor %}

这将产生所有元素，且之间没有空白字符。如果 *seq* 是一个从 ``1`` 到 ``9`` 的数字列表，
输出将为 ``123456789`` 。

如果开启行语句 ( `Line Statements <#line-statement>`_ )，
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


.. _escaping:

转义 (Escaping)
---------------

有时我们希望（甚至是必须）让 Jinja 忽略部分内容，否则它将被作为变量或语句块处理。例如：在默认语法下，
如果您想在模板中使用 ``{{`` 作为一个原始字串，而不是一个变量的起始标签，您必须使用一个技巧。

输出一个文字的变量分隔符( ``{{`` )的最简单方法是使用一个变量表达式：

.. code-block:: jinja

    {{ '{{' }}

对于更大的部分，可以标记一个块为 *raw* 。例如：为了在模板中包含 Jinja 语法的例子，
您可以使用这个片段：

.. code-block:: html+jinja

    {% raw %}
        <ul>
        {% for item in seq %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    {% endraw %}


.. _line-statement:

行语句 (Line Statements)
------------------------

如果应用开启了行语句功能，则可以将行标记为语句。例如：如果行语句前缀配置为 ``#`` ，
接下来的两个例子输出效果相同：

.. code-block:: html+jinja

    <ul>
    # for item in seq
        <li>{{ item }}</li>
    # endfor
    </ul>

    <ul>
    {% for item in seq %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>

只要行前没有文本，行语句前缀可以出现在行的任何位置。为了更好的可读性，启动块的语句（例如：
*for* , *if*, *elif* 等。）可以以冒号结尾：

.. code-block:: jinja

    # for item in seq:
        ...
    # endfor

.. note::

    如果有未关闭的圆括号、方括号、花括号，则行语句可以跨多行：

    .. code-block:: html+jinja

        <ul>
        # for href, caption in [('index.html', 'Index'),
                                ('about.html', 'About')]:
            <li><a href="{{ href }}">{{ caption }}</a></li>
        # endfor
        </ul>

从 Jinja 2.2 开始增加了基于行的注释功能。例如：如果行注释前缀被设置为 ``##`` ，
则从 ``##`` 开始到行尾的所有内容会被忽略（除换行符外）：

.. code-block:: html+jinja

    # for item in seq:
        <li>{{ item }}</li>     ## this comment is ignored
    # endfor


.. _template-inheritance:

模板继承 (Template Inheritance)
-------------------------------

模板继承是 Jinja 最强大的部分。模板继承允许您构建一个基础的模板"骨架"，
包含您站点所有共用元素和子模板可以重写的块的定义。

听起来很复杂，但其实很简单。用一个例子来讲解，就很容易理解了。


.. _base-template:

基础模板 (Base Template)
~~~~~~~~~~~~~~~~~~~~~~~~

下述模板定义了一个简单的 HTML 文档骨架，您可能会在一个简单的两栏页面中使用它，
我们把它命名为 ``base.html`` 。"子"模板的工作是使用内容来填充空白块：

.. code-block:: html+jinja

    <!DOCTYPE html>
    <html lang="en">
    <head>
        {% block head %}
        <link rel="stylesheet" href="style.css" />
        <title>{% block title %}{% endblock %} - My Webpage</title>
        {% endblock %}
    </head>
    <body>
        <div id="content">{% block content %}{% endblock %}</div>
        <div id="footer">
            {% block footer %}
            &copy; Copyright 2008 by <a href="http://domain.invalid/">you</a>.
            {% endblock %}
        </div>
    </body>
    </html>

在这个例子中，我们使用 ``{% block %}`` 标签定义了四个可被子模板填充的块。
*块* (block) 标签所做的就是，告诉模板引擎子模板可以重载该模板中的那些占位符。


.. _child-template:

子模板 (Child Template)
~~~~~~~~~~~~~~~~~~~~~~~

子模板可能如下所示：

.. code-block:: html+jinja

    {% extends "base.html" %}
    {% block title %}Index{% endblock %}
    {% block head %}
        {{ super() }}
        <style type="text/css">
            .important { color: #336699; }
        </style>
    {% endblock %}
    {% block content %}
        <h1>Index</h1>
        <p class="important">
          Welcome to my awesome homepage.
        </p>
    {% endblock %}

标签 ``{% extends %}`` 是关键所在。它告诉模板引擎，这个模板"扩展"了另一个模板。
当模板系统处理这个模板时，会首先定位父模板。扩展标签应该作为模板的第一个标签。
在它之前的内容将被正常输出到body下，而非重载相应块，故这可能会造成混乱。
预知此行为的更多细节以及如何利用它，请查看 `Null-Master Fallback`_

.. _Null-Master Fallback: http://jinja.pocoo.org/docs/2.9/tricks/#null-master-fallback

模板的文件名取决于模板的加载程序。例如： ``FileSystemLoader``
允许您通过提供文件名来访问其他模板。您可以使用斜线( ``/`` )来访问子路径下的模板：

.. code-block:: jinja

    {% extends "layout/default.html" %}

但是这个行为取决于应用嵌入 Jinja 的方式。注意：由于子模板没有定义 ``footer`` 块，
将使用父模板中定义的值作为替代。

在同一个模板中，不可以定义多个同名的 ``{% block %}`` 标签。
存在此限制是因为块标记同时在两边作用。这是因为一个块标签不仅提供一个用于填充的占位符，
同时也定义了在父模板中占位符填充的内容。如果模板中有两个同名的 ``{% block %}`` 标签，
父模板将不知道使用哪个块的内容。

然而，如果您想多次打印一个块，您可以使用一个特殊的 ``self`` 变量，通过它调用相应的块名：

.. code-block:: html+jinja

    <title>{% block title %}{% endblock %}</title>
    <h1>{{ self.title() }}</h1>
    {% block body %}{% endblock %}


.. _super-blocks:

超块 (Super Blocks)
~~~~~~~~~~~~~~~~~~~

我们可以通过调用 *super* 来渲染父块的内容。这将返回父块的结果：

.. code-block:: html+jinja

    {% block sidebar %}
        <h3>Table Of Contents</h3>
        ...
        {{ super() }}
    {% endblock %}


.. _named-block-end-tags:

命名的块结束标签 (Named Block End-Tags)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

为了更好地可读性， Jinja2 允许在块结束标签后添加块名称：

.. code-block:: html_jinja

    {% block sidebar %}
        {% block inner_sidebar %}
            ...
        {% endblock inner_sidebar %}
    {% endblock sidebar %}

但是， *endblock* 关键字后的名称必须与块名称匹配。


.. _block-nesting-and-scope:

块嵌套和作用域 (Block Nesting and Scope)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

为了实现更复杂的布局，块可以被嵌套。每个默认块不能访问外部作用域中的变量：

.. code-block:: html+jinja

    {% for item in seq %}
        <li>{% block loop_item %}{{ item }}{% endblock %}</li>
    {% endfor %}

这个例子将输出空白的 ``<li>`` 条目，因为在块中 *item* 是不可用的。这么做的原因是因为，
如果块被子模板重载了，将会出现一个未在块中定义或传递给上下文的变量。

从 Jinja 2.2 开始， 您可以通过在块声明时添加一个作用域修饰符 "scoped"
来明确指定块中的变量可用：

.. code-block:: html+jinja

    {% for item in seq %}
        <li>{% block loop_item scoped %}{{ item }}{% endblock %}</li>
    {% endfor %}

重载块时，不必提供 *scoped* 修饰符。


.. _template-objects:

模板对象 (Template Objects)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

*2.4版本中变更*

如果一个模板对象被传入到模板上下文中，您也可以从该对象扩展。假设调用代码传入了一个名为
*layout_template* 的布局模板到环境中，这段代码便可以工作了：

.. code-block:: jinja

    {% extends layout_template %}

之前， *layout_template* 变量必须是含有布局模板文件名的字符串，以便扩展标签正常工作。


.. _html-escaping:

HTML转义 (HTML Escaping)
------------------------

当从模板生成 HTML 时，总是会存在一定的风险，那就是使用的变量包含了会影响 HTML 结果的字符。
有两个解决办法：

a. 手动转义变量
b. 通过默认自动转义所有内容

Jinja 同时支持这两种方法。使用哪个取决于应用配置。出于各种原因，默认配置下不会自动转义：

* 除了安全值外，转义所有变量意味着一些已知的不包含 HTML （如：数字、布尔）的值也将被
  Jinja 转义，这可能是巨大的性能损失。
* 关于变量的安全性信息是非常脆弱的。强制转义安全和不安全的值，可能会发生返回双重转义的 HTML 。


.. _working-with-manual-escaping:

使用手动转义 (Working with Manual Escaping)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果启动手动转义，则 **您** 有责任根据需要转义变量。转义什么？如果您有一个可能包含以下字符的变量
（ ``>`` , ``<`` , ``&`` 或 ``"``），您 **应该** 转义它，除非该变量包含形式合法且可信的 HTML 。
转义通过传输变量到 ``|e`` 过滤器执行：

.. code-block:: jinja

    {{ user.username|e }}


.. _working-with-automatic-escaping:

使用自动转义 (Working with Automatic Escaping)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当启动自动转义时，除了标记为安全的值外，默认转义所有内容。变量和表达式可以标记为安全，
通过以下方法之一：

a. 应用上下文字典中，使用 *MarkupSafe.Markup*
b. 模板中，使用 ``|safe`` 过滤器

这种方法的主要问题是 Python 本身没有污染值的概念，所以无论值安全与否都可能丢失。

如果一个值没有标记为安全，自动转义将发生；这意味着您可能会得到双重转义的的内容。
然而，双重转义很容易避免：只依靠 Jinja2 提供的工具，不使用 Python 的内建构造器，如
*str.format* 或字符串模运算符( *%* )。

Jinja2 函数(macros, super, self.BLOCKNAME)通常会返回标记为安全的模板数据。

因为本地 Python 字串(str, unicode, basestring)不是含 ``__html__``
属性的 *MarkupSafe.Markup* 字符串，所以模板中的字符串文字被认为是不安全的。


.. _list-of-control-structures:

控制结构列表 (List of Control Structures)
-----------------------------------------

控制结构指的是程序流程控制中的所有东西(如： if/elif/else)， for 循环，
以及宏(macros)和块(blocks)。在默认语法下，控制结构出现在 ``{% ... %}`` 块中。


.. _for-loop:

For
~~~

循环序列中的每个条目(item)。例如：显示一个 *users* 变量中提供的用户列表：

.. code-block:: html+jinja

    <h1>Members</h1>
    <ul>
    {% for user in users %}
      <li>{{ user.username|e }}</li>
    {% endfor %}
    </ul>

由于模板中的变量保留了其对象属性，因此可以对像 *dict* 这样的容器进行迭代：

.. code-block:: html+jinja

    <dl>
    {% for key, value in my_dict.iteritems() %}
        <dt>{{ key|e }}</dt>
        <dd>{{ value|e }}</dd>
    {% endfor %}
    </dl>

但是，注意 **Python 的字典是无序的** ；所以您可能需要传入一个包含内容为元组(
``tuple`` )的有序列表( ``list`` )到模板中，或者一个 ``collections.OrderedDict`` ，
再或者使用 *dictsort* 过滤器。

在一个 for 循环块中，您可以访问一些特殊的变量：

============== ====
变量            描述
============== ====
loop.index     循环迭代的当前索引。(从1开始)
loop.index0    循环迭代的当前索引。(从0开始)
loop.revindex  循环迭代的反向索引。(从1开始)
loop.revindex0 循环迭代的反向索引。(从0开始)
loop.first     如果为首个迭代元素，返回 ``True`` 。
loop.last      如果为最后一个迭代元素，返回 ``True`` 。
loop.length    序列中的条目总数。
loop.cycle     序列列表间的循环辅助函数，见下方解释。
loop.depth     指示当前渲染的递归循环的深度。(从1开始)
loop.depth0    指示当前渲染的递归循环的深度。(从0开始)
============== ====

在 for 循环中，可以通过使用特殊的 *loop.cycle* 辅助函数，
实现在每次循环的字符串/变量之间循环：

.. code-block:: html+jinja

    {% for row in rows %}
        <li class="{{ loop.cycle('odd', 'even') }}">{{ row }}</li>
    {% endfor %}

从 Jinja 2.1 开始，提供了一个额外的循环(cycle)辅助函数，
允许循环(cycling)一个未绑定的循环(loop-unbound)。获取更多信息，请查看
`全局函数列表 <#builtin-globals>`_ (List of Global Functions)。

.. _loop-filtering:

不像在 Python 中那样，您不能在循环中执行 *break* 或 *continue* 。但是，
您可以在迭代期间过滤序列，过滤器允许您跳过特定的条目。下面的例子中跳过了所有被隐藏的用户：

.. code-block:: html+jinja

    {% for user in users if not user.hidden %}
        <li>{{ user.username|e }}</li>
    {% endfor %}

优点是特定的循环变量将被正确计数；没有被迭代的用户(users)不被计入。

如果因为序列为空或过滤器从序列中删除了所有条目而造成迭代没有执行，
您可以通过 *else* 来渲染一个默认块：

.. code-block:: html+jinja

    <ul>
    {% for user in users %}
        <li>{{ user.username|e }}</li>
    {% else %}
        <li><em>no users found</em></li>
    {% endfor %}
    </ul>

注意，在 Python 中，当相应的循环 **没有** *break* 时，将执行 *else* 语句块。
由于 Jinja 的循环根本就不支持 *break* ，所以选择了稍微不同的 *else* 关键词行为设计。

也可以递归地使用循环。如果您处理的是递归数据（如： Sitemaps 或 RDFa ），这将非常有用。
为了使用递归循环，您基本上必须将 *recursive* 修饰符添加到循环定义中，
并使用您想要递归的新迭代器调用 *loop* 变量。

下面的例子使用递归循环实现了一个站点地图(sitemap)：

.. code-block:: html+jinja

    <ul class="sitemap">
    {%- for item in sitemap recursive %}
        <li><a href="{{ item.href|e }}">{{ item.title }}</a>
        {%- if item.children -%}
            <ul class="submenu">{{ loop(item.children) }}</ul>
        {%- endif %}</li>
    {%- endfor %}
    </ul>

变量 *loop* 总是指向最近（最内部）的循环。如果我们又多级循环，
我们可以通过在我们想要递归使用的循环后写 *{% set outer_loop = loop %}* 来重新绑定
*loop* 变量。然后，我们通过 *{{ outer_loop(...) }}* 调用它。

请注意，循环中的赋值将在迭代结束时清除，不能作用于循环外。旧版本的 Jinja2 存在一个 bug ，
在某些情况下，循环内的赋值将在迭代结束后仍然有效。这是不支持的。
更多关于如何处理这种情况的说明，请查看 `赋值 <#assignments>`_ (Assignments)。


.. _if:

If
~~

Jinja 中的 *if* 语句与 Python 中的 *if* 语句相同。在最简单的形式中，
您可以使用它来测试一个变量是否被定义、非空以及非假(False)：

.. code-block:: html+jinja

    {% if users %}
    <ul>
    {% for user in users %}
        <li>{{ user.username|e }}</li>
    {% endfor %}
    </ul>
    {% endif %}

对于多分支的情况，可以像 Python 中那样使用 *elif* 和 *else* 。
您也可以使用更复杂的 `表达式 <#expressions-statements>`_ (expressions)：

.. code-block:: jinja

    {% if kenny.sick %}
        Kenny is sick.
    {% elif kenny.dead %}
        You killed Kenny!  You bastard!!!
    {% else %}
        Kenny looks okay --- so far
    {% endif %}

If 也可以被作为 `行内表达式 <#if-expression>`_ (inline expression)
和 for的 `循环过滤器 <#loop-filtering>`_ (loop filtering)使用。


.. _macros:

Macros
~~~~~~

宏(Macros)与常规编程语言中的函数相同。宏可用于将经常使用的代码放到一个可复用的函数中，
从而实现不重复造轮子("DRY")。

下面是一个宏的小例子，它渲染了一个表单元素：

.. code-block:: html+jinja

    {% macro input(name, value='', type='text', size=20) -%}
        <input type="{{ type }}" name="{{ name }}" value="{{
            value|e }}" size="{{ size }}">
    {%- endmacro %}

在其命名空间中，宏可以像一个函数那样被调用：

.. code-block:: html+jinja

    <p>{{ input('username') }}</p>
    <p>{{ input('password', type='password') }}</p>

如果宏被定义在不同的模板中，您需要首先 `import <#import>`_ 。

在宏内部，您可以访问三个特殊的变量：

`varargs`
    如果传递给宏多余其接受的位置参数数量，那么这些多余的参数将作为值列表存在于一个特殊的
    `varargs` 变量中。

`kwargs`
    像 `varargs` 一样，不过是对于关键字参数。所有未消费的关键字参数存储在这个特殊变量中。

`caller`
    如果一个宏从一个 `call <#call-block>`_ 标签中被调用，
    调用者(caller)作为可调用的宏被存储在这个变量中。

宏还暴露了一些其内部细节。以下属性可用于宏对象：

`name`
    宏名。 ``{{ input.name }}`` 将打印出 ``input`` 。

`arguments`
    宏接受的参数名称的元组。

`defaults`
    默认值的元组

`catch_kwargs`
    如果宏接受额外的关键字参数，则此值为 `true` (即：访问特别的 `kwargs` 变量)。

`catch_varargs`
    如果宏接受额外的位置参数，则此值为 `true` (即：访问特别的 `varargs` 变量)。

`caller`
    如果宏访问特别的 `caller` 变量，并且可以从 `call <#call-block>`_ 标签调用，
    则此值为 `true` 。

如果宏名以下划线开头，则为不可导出也不能被导入。


.. _call-block:

Call
~~~~

在某些情况下，将宏传递给另一个宏是很有用的。为此，您可以使用特殊的 `call` 语句块。
以下示例显示了利用 `call` 功能以及如何使用宏：

.. code-block:: html+jinja

    {% macro render_dialog(title, class='dialog') -%}
        <div class="{{ class }}">
            <h2>{{ title }}</h2>
            <div class="contents">
                {{ caller() }}
            </div>
        </div>
    {%- endmacro %}

    {% call render_dialog('Hello World') %}
        This is a simple dialog rendered by using a macro and
        a call block.
    {% endcall %}

它也可以将参数传递回 `call` 语句块。这使得它可以作为循环(loops)的替代。
一般来说， `call` 语句块完全像一个没有名称的宏。

下面是一个 `call` 语句块如何与参数一起使用的例子：

.. code-block:: html+jinja

    {% macro dump_users(users) -%}
        <ul>
        {%- for user in users %}
            <li><p>{{ user.username|e }}</p>{{ caller(user) }}</li>
        {%- endfor %}
        </ul>
    {%- endmacro %}

    {% call(user) dump_users(list_of_user) %}
        <dl>
            <dt>Realname</dt>
            <dd>{{ user.realname|e }}</dd>
            <dt>Description</dt>
            <dd>{{ user.description }}</dd>
        </dl>
    {% endcall %}


Filters
~~~~~~~

过滤器块(sections)允许您在模板数据块上应用常规的 Jinja2 过滤器。
只需要将代码封装在一个特殊的 `filter` 块(section)中:

.. code-block:: jinja

    {% filter upper %}
        This text becomes uppercase
    {% endfilter %}


.. _assignments:

Assignments
~~~~~~~~~~~

在代码块内部，您还可以将值赋给变量。在顶层（代码块、宏或循环之外）的赋值可以从模板中导出，
像顶层的宏，并且可被其他模板导入。

赋值使用 `set` 标签，并且可以有多个目标值：

.. code-block:: jinja

    {% set navigation = [('index.html', 'Index'), ('about.html', 'About')] %}
    {% set key, value = call_something() %}

.. admonition:: 作用域行为
    :class: note

    请记住，不可能在语句块外部使用语句块内部中设置(set)的变量。这也适用于循环(loops)。
    该规则的唯一例外是不会引入作用域的 ``if`` 语句。因此，以下模板不会像您期望的那样执行：

    .. code-block:: jinja

        {% set iterated = false %}
        {% for item in seq %}
            {{ item }}
            {% set iterated = true %}
        {% endfor %}
        {% if not iterated %} did not iterate {% endif %}

    使用 Jinja 语法不可能做到这一点。但是您可以使用替代的结构，如循环的 `else`
    语句块或者特殊的 `loop` 变量：

    .. code-block:: jinja

        {% for item in seq %}
            {{ item }}
        {% else %}
            did not iterate
        {% endfor %}


Block Assignments
~~~~~~~~~~~~~~~~~

`2.8版本中引入`

从 Jinja 2.8 开始，可以使用赋值块来将一个代码块的内容赋值到一个变量中。
这在某些情况下，可以作为宏的替代使用。在这种情况下，不是使用等号和值，而是仅仅使用变量名，
然后直到 ``{% endset %}`` 的内容将被赋值给该变量。

例子：

.. code-block:: html+jinja

    {% set navigation %}
        <li><a href="/">Index</a>
        <li><a href="/downloads">Downloads</a>
    {% endset %}

然后 `navigation` 变量将包含导航 HTML 的源码。


.. _extends:

Extends
~~~~~~~

`extends` 标签可以用于从另一个模板扩展一个模板。一个文件中可以有多个 `extends` 标签，
但是一次只能执行一个。

参见上面关于 `模板继承`_ (Template Inheritance)的部分。


.. _blocks:

Blocks
~~~~~~

块(Blocks)用于继承，并同时作为占位符(placeholders)和替换(replacements)。
在 `模板继承`_ (Template Inheritance)章节中有详细介绍。

.. _模板继承: #template-inheritance


Include
~~~~~~~

`include` 语句可用于包含模板，并将该文件的渲染内容返回到当前命名空间：

.. code-block:: jinja

    {% include 'header.html' %}
        Body
    {% include 'footer.html' %}

默认情况下， `include` 的模板可以访问现有上下文中的变量。
有关导入(imports)和包含(includes)的上下文行为的更多详细信息，
请参阅 `导入上下文行为`_ (Import Context Behavior)。

从 Jinja 2.2 起，您可以使用 ``ignore missing`` 来标记一个 include ；
在这种情况下，如果要 include 的模板不存在， Jinja 将忽略该语句。
当与 ``with`` 或 ``without context`` 相结合时，它必须放在上下文可见性语句之 *前* 。
下面是一些合法的用例：

.. code-block:: jinja

    {% include "sidebar.html" ignore missing %}
    {% include "sidebar.html" ignore missing with context %}
    {% include "sidebar.html" ignore missing without context %}

`2.2版本中引入`

您还可以提供在包含前检查其存在性的模板列表。第一个存在的模板将被 `include` 。
在列表中的模板均不存在的情况下，如果提供了 `ignore missing` 语句，将返回一个空渲染，
否则将抛出异常。

例子：

.. code-block:: jinja

    {% include ['page_detailed.html', 'page.html'] %}
    {% include ['special_sidebar.html', 'sidebar.html'] ignore missing %}

`2.4版本中变更` : 如果一个模板对象被传入到模板上下文中，您可以使用 `include` 包含这个对象。


.. _import-statements:

Import
~~~~~~

Jinja2 支持将常用代码放入宏中。这些宏可以放在不同的模板，并从那里被导入。
这类似于 Python 中的 import 语句。了解导入是被缓存的，并且默认情况下导入的模板只能访问全局变量，
不能访问当前模板中的变量。有关导入和包含的上下文行为的更多详细信息，请参阅 `导入上下文行为`_ 。

.. _导入上下文行为: #import-visibility

有两种导入模板的方式。您可以将完整的模板导入到变量中，或从中请求特定的宏/导出的变量。

想象一下，我们有一个渲染表单（称为 `forms.html` ）的辅助模块(module)：

.. code-block:: html+jinja

    {% macro input(name, value='', type='text') -%}
        <input type="{{ type }}" value="{{ value|e }}" name="{{ name }}">
    {%- endmacro %}

    {%- macro textarea(name, value='', rows=10, cols=40) -%}
        <textarea name="{{ name }}" rows="{{ rows }}" cols="{{ cols
            }}">{{ value|e }}</textarea>
    {%- endmacro %}

访问模板变量和宏的最简单和最灵活的方法是将整个模板模块导入到一个变量中。
这样，您就可以访问这些属性了：

.. code-block:: html+jinja

    {% import 'forms.html' as forms %}
    <dl>
        <dt>Username</dt>
        <dd>{{ forms.input('username') }}</dd>
        <dt>Password</dt>
        <dd>{{ forms.input('password', type='password') }}</dd>
    </dl>
    <p>{{ forms.textarea('comment') }}</p>

或者，您可以从模板中导入指定的名称到当前命名空间：

.. code-block:: html+jinja

    {% from 'forms.html' import input as input_field, textarea %}
    <dl>
        <dt>Username</dt>
        <dd>{{ input_field('username') }}</dd>
        <dt>Password</dt>
        <dd>{{ input_field('password', type='password') }}</dd>
    </dl>
    <p>{{ textarea('comment') }}</p>

以一个或多个下划线开头的宏和变量是私有的，无法导入。

`2.4版本中变更` : 如果一个模板对象被传入到模板上下文中，您可以使用 `import` 导入这个对象。


.. _import-visibility:

导入上下文行为 (Import Context Behavior)
----------------------------------------

默认情况下，包含(include)的模板被传递到当前上下文中，而导入(import)的模板不传递。
这样做的原因是，与 include 不同， import 是被缓存的；因为导入通常用作保存宏的模块。

此行为可以显式地更改：通过添加 `with context` 或 `without context` 到
import/include 指令，当前的上下文被传入到模板中，并且缓存被自动禁用。

这里有两个例子：

.. code-block:: jinja

    {% from 'forms.html' import input with context %}
    {% include 'header.html' without context %}

.. admonition:: 注意
    :class: note

    在 Jinja 2.0 中，传递给 include 模板的上下文不包含模板中定义的变量。事实上，
    这段代码无法实现我们的需求：

    .. code-block:: jinja

        {% for box in boxes %}
            {% include "render_box.html" %}
        {% endfor %}

    在 Jinja 2.0 中， include 的模板 ``render_box.html`` **无法** 访问到 `box` 。
    从 Jinja 2.1 开始， ``render_box.html`` 就可以访问到了。


.. _expressions-statements:

表达式 (Expressions)
--------------------

Jinja 允许基本表达式在任何地方使用。这非常类似于 Python ；即使您不使用 Python ，
您也应该感到很自然。


文字 (Literals)
~~~~~~~~~~~~~~~

文字是表达式的最简单形式。对于 Python 对象来说，文字(Literals)的表示为字符串和数字。
存在以下文字：

"Hello World":
    两个双引号或单引号间的所有内容称为一个字符串。这在模板中需要一个字符串时非常有用
    （例如：作为函数调用或过滤器的参数，或者只是用于扩展(extend)或包含(include)模板）。

42 / 42.23:
    整数和浮点数是通过写下数字创建的。如果存在一个小数点，那么该数字为浮点数，否则为整数。

['list', 'of', 'objects']:
    两个方括号间的所有内容称为一个列表。列表对于存储用来迭代的序列数据非常有用。例如：
    您可以很容易的使用列表(list)和元组(tuple)为一个 for 循环创建一组链接序列：

    .. code-block:: html+jinja

        <ul>
        {% for href, caption in [('index.html', 'Index'), ('about.html', 'About'),
                                 ('downloads.html', 'Downloads')] %}
            <li><a href="{{ href }}">{{ caption }}</a></li>
        {% endfor %}
        </ul>

('tuple', 'of', 'values'):
    元组就像不能修改的列表("immutable")。如果一个元组仅包含一个条目，后面必须跟一个逗号(
    ``('1-tuple',)`` )。元组通常用于表示两个或多个元素的条目。更多详细信息，
    请参阅上面列表的示例。

{'dict': 'of', 'key': 'and', 'value': 'pairs'}:
    Python 中的字典(dict)是一种结合键(key)和值(value)得结构。键必须是唯一的，
    并且始终只有一个值。字典很少在模板中使用；仅在某些罕见的情况下非常有用，比如
    `xmlattr() <#xmlattr>`_ 过滤器。

true / false:
    true 就是对， false 就是错。

.. admonition:: 注意
    :class: note

    特殊常量 `true` , `false` 和 `none` 都是小写的。
    因为这曾经造成了混乱，（ `True` 被用于扩展为一个被认为是 false
    的未定义变量(undefined variable)）。他们现在也可以被写成首字母大写的格式(
    `True`, `False` 和 `None` )。但是为了一致性，
    （所有的 Jinja 标识符都是小写的）您应该使用小写版本。


数学 (Math)
~~~~~~~~~~~

Jinja 允许您使用数值计算。这在模板中很少使用，仅为了完整性而存在。支持以下运算符：

\+
    俩对象求和。通常对象为数字，但如果两者都为字符串或列表，您可以使用这种方式来拼接他们。
    但这不是拼接字符串的首选方式！为实现字符串拼接，请查看 ``~`` 运算符。
    ``{{ 1 + 1 }}`` 结果为 ``2`` 。

\-
    从第一个数中减去第二个数。 ``{{ 3 - 2 }}`` 结果为 ``1`` 。

/
    两数相除。返回值将是浮点数。 ``{{ 1 / 2 }}`` 结果为 ``{{ 0.5 }}`` 。
    （就像 ``from __future__ import division`` 。）

//
    两书相除并且返回结果被截断的整数部分。 ``{{ 20 // 7 }}`` 结果为 ``2`` 。

%
    计算整除的余数。 ``{{ 11 % 7 }}`` 结果为 ``4`` 。

\*
    左操作数乘以右操作数。 ``{{ 2 * 2 }}`` 将返回 ``4`` 。也可以被用于多次重复字串。
    ``{{ '=' * 80 }}`` 将打印一个80个等号的条。

\**
    对左操作符求右操作符次幂。 ``{{ 2**3 }}`` 将返回 ``8`` 。


比较 (Comparisons)
~~~~~~~~~~~~~~~~~~

==
    比较两个对象相等。

!=
    比较两个对象不等。

>
    如果左边大于右边，返回 `true`

>=
    如果左边大于或等于右边，返回 `true`

<
    如果左边小于右边，返回 `true`

<=
    如果左边小于或等于右边，返回 `true`


逻辑 (Logic)
~~~~~~~~~~~~

对于 `if` 语句， `for` 过滤器，和 `if` 表达式，组合多个表达式是非常有用的：

and
    如果左右操作数皆为真，返回 true 。

or
    如果左或右操作数为真，返回 true 。

not
    否定语句（见下文）。

(expr)
    表达式组。

.. admonition:: 注意
    :class: note

    ``is`` 和 ``in`` 运算符支持中缀表示法的否定使用： ``foo is not bar`` 和
    ``foo not in bar`` 而不是 ``not foo is bar`` 和 ``not foo in bar`` 。
    所有其他表达式都需要前缀表示法： ``not (foo and bar)`` 。


其他运算符 (Other Operators)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

下述运算符非常有用，但是不归类于其他上述分类：

in
    执行序列/映射的包含测试。如果左操作数被包含于有操作数中，返回 true 。
    例如： ``{{ 1 in [1, 2, 3] }}`` 将返回 true 。

is
    执行一个 `测试 <#tests>`_ 。

\|
    应用一个 `过滤器 <#filters>`_ 。

~
    转换所有操作数为字符串，并拼接到一起。

    ``{{ "Hello" ~ name ~ "!" }}`` （假设 `name` 设置为 ``'John'`` ）将返回
    ``Hello John!`` 。

()
    调用一个 callable ： ``{{ post.render() }}`` 。像 Python
    那样，您可以在括号内使用位置参数和关键字参数：

    ``{{ post.render(user, full=true) }}`` 。

. / []
    获取一个对象的属性。(详细参阅 `变量 <#variables>`_ )。


.. _if-expression:

If表达式 (If Expression)
~~~~~~~~~~~~~~~~~~~~~~~~

也可以使用内联的 `if` 表达式。在某些情况下是很有用的。例如：如果定义了一个变量，
则可以从一个模板中使用此扩展，否则从默认布局模板中扩展：

.. code-block:: jinja

    {% extends layout_template if layout_template is defined else 'master.html' %}

通用语法是 ``<do something> if <something is true> else <do something else>`` 。

`else` 部分是可选的。如果不提供， else 块将隐式的设置为一个未定义对象(undefined object)：

.. code-block:: jinja

    {{ '[%s]' % page.title if page.title }}


.. _builtin-filters:

内建过滤器列表 (List of Builtin Filters)
----------------------------------------

abs(number)
    返回参数的绝对值。

.. _attr-func:

attr(obj, name)
    获取对象的属性。 ``foo|attr("bar")`` 与 ``foo.bar``
    相同，前者总是返回属性，并且不进行条目查找。

    详情参阅 `订阅注意 <#notes-on-subscriptions>`_ 。

batch(value, linecount, fill_with=None)
    批条目过滤器。

待完善


.. _builtin-tests:

内建测试列表 (List of Builtin Tests)
------------------------------------

待完善


.. _builtin-globals:

全局函数列表 (List of Global Functions)
---------------------------------------

待完善


扩展 (Extensions)
-----------------

接下来的章节介绍了 Jinja2 可被应用开启的内建扩展。
当然应用也可以提供本文档没有覆盖到的更多的扩展；在这种情况下，应该提供一个单独的文档，
来解释所用的 `扩展`_  (extensions)。

.. _扩展: http://jinja.pocoo.org/docs/2.9/extensions/#jinja-extensions

.. _i18n-in-templates:

i18n
~~~~

如果开启 i18n 扩展，可以将模板中的一部分标记为可翻译。要标记一个章节为可翻译，
您可以使用 `trans` ：

.. code-block:: html+jinja

    <p>{% trans %}Hello {{ user }}!{% endtrans %}</p>

要翻译模板表达式（例如：使用模板过滤器，或者只是访问对象的属性），
您需要将表达式绑定到名称以在翻译块中使用：

.. code-block:: html+jinja

    <p>{% trans user=user.username %}Hello {{ user }}!{% endtrans %}</p>

如果您需要在一个 `trans` 标签中绑定多个表达式，请使用逗号分隔( ``,`` )：

.. code-block:: html+jinja

    {% trans book_title=book.title, author=author.name %}
    This is {{ book_title }} by {{ author }}
    {% endtrans %}

在 trans 标签中除了变量标签外不允许使用任何语句。

对于复数表示，您可以在 `trans` 和 `endtrans` 之间使用 `pluralize`
标签指定单数和复数形式：

.. code-block:: html+jinja

    {% trans count=list|length %}
    There is {{ count }} {{ name }} object.
    {% pluralize %}
    There are {{ count }} {{ name }} objects.
    {% endtrans %}

默认情况下，语句块中的第一个变量用于确认正确的单复数形式。如果您希望指定用于判断的变量，
可以通过将用于判断的变量名作为参数添加到 `pluralize` 语句中，用以指定单复数形式判断依据：

.. code-block:: jinja

    {% trans ..., user_count=users|length %}...
    {% pluralize user_count %}...{% endtrans %}

在表达式中翻译一个字符串也是可行的。可通过以下三个函数实现：

- `gettext`: 翻译单数形式的字符串
- `ngettext`: 翻译复数形式的字符串
- `_`: `gettext` 的别名

例如：您可以像这样轻松的打印一个翻译后的字符串：

.. code-block:: jinja

    {{ _('Hello World!') }}

要使用占位符，请使用 `format` 过滤器：

.. code-block:: jinja

    {{ _('Hello %(user)s!')|format(user=user.username) }}

对于多个占位符，一定要使用 `format` 的关键字参数，因为其他语言可能不会使用相同的单词顺序。

`2.5版本中变更`

如果激活了新格式的 gettext 调用( `Newstyle Gettext`_ )，那么可以更容易的使用占位符：

.. code-block:: html+jinja

    {{ gettext('Hello World!') }}
    {{ gettext('Hello %(name)s!', name='World') }}
    {{ ngettext('%(num)d apple', '%(num)d apples', apples|count) }}

注意，除了常规参数外， `ngettext` 函数的格式化字符串还会自动接收 count 作为 `num` 参数。

.. _Newstyle Gettext: http://jinja.pocoo.org/docs/2.9/extensions/#newstyle-gettext
