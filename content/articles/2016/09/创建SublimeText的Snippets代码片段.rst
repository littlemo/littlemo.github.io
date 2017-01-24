:title: 创建SublimeText的Snippets代码片段
:date: 2016-09-05
:modified: 2017-01-23 14:25:07
:category: Tools
:tags: SublimeText, Snippets
:slug: 创建SublimeText的Snippets代码片段
:author: moore
:summary: 设置SublimeText的Snippets代码段，从而便于快速的模板编写

设置Gitblog日志文件的代码片段
=============================

由于Gitblog是通过书写 ``Markdown`` 文件来生成日志页的，并提供相关的 ``分类`` ， ``归档`` ， ``标签`` 等功能，故需要在文档的header部分增加必要的描述信息。

为了提高效率，将其模板化设置为Snippets，内容如下：

.. code-block:: xml

    <snippet>
        <content><![CDATA[
    <!--
    author: ${1:moore}
    head: http://s.gravatar.com/avatar/cb7df89c872ae4af496b6b9e94520ffe?s=80
    date: ${2:YYYY-mm-dd}
    title: ${3:标题}
    tags: ${4:标签}
    category: ${5:分类}
    status: draft
    -->
    ]]></content>
        <!-- Optional: Set a tabTrigger to define how to trigger the snippet -->
        <tabTrigger>blog</tabTrigger>
        <!-- Optional: Set a scope to limit where the snippet will trigger -->
        <scope>text.html.markdown</scope>
    </snippet>

.. rubric:: 参考文章

#. `Sublime Text 2 中怎样查找scope的名称 <http://blog.csdn.net/pxzy/article/details/8490058>`_
#. `Sublime Text自定制代码片段(Code Snippets) <http://9iphp.com/web/html/sublime-text-code-snippets.html>`_
#. `Sublime Text非官方文档 <https://docs.sublimetext.info/en/latest/extensibility/snippets.html>`_
