Tutorial
========

.. toctree::
    :hidden:

    /tutorial/preparation
    /tutorial/basics/index


Dissect has an enormous amount of functionality which can be daunting to grasp at first. This tutorial is designed to help you
understand key concepts of Dissect and provides you with examples of what Dissect can do. It is important to realise that this
tutorial does not cover everything on Dissect so you are encouraged to check other parts of the documentation once you feel comfortable to do so.

Target audience
---------------

This tutorial is aimed at new users interested in learning what Dissect can do. Since Dissect provides tooling for forensic investigators and
incident responders, this tutorial deals with applications of Dissect in that field.

The prerequisites below are recommended in order to be able to follow the tutorial:

- Basic Python knowledge
- How to set up and use Python virtual environments (recommended)
- Linux command line knowledge (environment variables, grep, sort, ls, etc)
- Basic computer forensic knowledge to understand the use cases (recommended)


Tutorial goals
--------------

After completing this tutorial, you will have learned

- important terminology used by Dissect, such as targets and records
- the basic use of core tooling such as ``target-query``, ``target-info`` and ``rdump``
- how to easily obtain forensic artefacts from various sources, such as disks or Virtual machine images
- how to transfer the obtained artefacts to external tooling such as Splunk
- where to find additional information for you to explore (developing, plugins, etc).


.. FIXME. By giving you numerous examples which you can replicate on your own computer, ...

.. The setting of the tutorial is <investigation>

.. PLUGINS

Tutorial structure
------------------

The tutorial is structured as follows:

1. :doc:`preparation` Preparation; Installing Dissect, downloading example files and setting up a tutorial environment
2. :doc:`basics` Demonstration of key terminology such as targets and records
3. Basic use cases
4. Advanced use cases


.. note ::

    It is possible that you will also see warnings when executing these commands. These can be safely ignored.