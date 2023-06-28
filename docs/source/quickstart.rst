快速入门
=====

.. _quickstart:

一、方法论
------------

westat的整体方法论和代码框架基于 ``SEMMA`` ，它是由SAS研究院开发的一款非常著名的数据挖掘与分析方法， ``SEMMA`` 分别是抽样(Sample)、探索(Explore)、修订(Modify)、建模(Model)和评估(Assess)的英文首字母缩写。


二、示例代码
----------------

在westat的源码仓库和安装后 ``examples`` 文件夹内，我们增加了一个名为 ``HereWeGo.ipynb`` 的代码示例文件，该文件是 ``jupyter-notebook`` 格式的Python脚本，你可以将该文件复制到jupyter的工作目录进行查看。


三、快速开始
----------------

.. code-block:: console

   $ import westat as we
   $ we.version