安装
=====

.. _installation:

一、使用pip在线安装
------------

如果你正在 ``pip`` ，你可以使用如下命令，通过 ``pip`` 联网下载最新版本并进行安装:


.. code-block:: console

   $ pip install westat


二、使用pip离线安装
------------

如果你正在 ``pip`` ，你可以使用如下命令，通过 ``pip`` 联网下载最新版本，打包后，在离线环境内进行安装:

1、联网下载 westat 和相关依赖包

保存到当前目录下的westat文件夹:


.. code-block:: console

   $ pip download -d ./westat westat


2、离线安装 westat 和相关依赖包

将 westat 存放到指定的离线环境，在目录下执行如下命令


.. code-block:: console

   $ pip install --no-index --find-links=.westat/ westat


三、使用conda在线安装
------------

如果你正在 ``conda`` ,你可以使用如下命令，通过 conda 联网下载最新版本并进行安装:


.. code-block:: console

   $ conda install westat

