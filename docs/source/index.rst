.. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**************************************
Welcome to pybpod-api's documentation!
**************************************

.. note::

   All examples and Bpod's state machine and communication logic were based on the original version made available by `Josh Sanders (Sanworks) <https://github.com/sanworks>`_.

.. image:: /_images/pybpodapi-logo.svg
   :scale: 100 %

What is pybpod-api?
===================
**pybpod-api** is a Python library that enables communication with the latest `Bpod device <https://sanworks.io/shop/viewproduct?productID=1011>`_ version. You can use it directly as a CLI (Command Line Interface) or use your favorite GUI to interact with it.

This library is maintained by a team of SW developers at the `Champalimaud Foundation <http://research.fchampalimaud.org>`_. Please find more information on section :ref:`Project Info <project-info-label>`.

What is Bpod?
-------------

**Bpod** is a system from `Sanworks <https://sanworks.io/index.php>`_ for precise measurement of small animal behavior.
It is a family of open source hardware devices which includes also software and firmware to control these devices. The software was originally developed in Matlab providing retro-compatibility with the `BControl <http://brodywiki.princeton.edu/bcontrol/index.php/Main_Page>`_ system.

.. seealso::

    Bpod device: https://sanworks.io/shop/viewproduct?productID=1011

    Bpod on Github: https://github.com/sanworks/Bpod

    Bpod Wiki: https://sites.google.com/site/bpoddocumentation/

    BControl project: http://brodywiki.princeton.edu/bcontrol/index.php/Main_Page/


Why a Python port?
------------------
Python is one of the most popular programming languages today `[1] <https://pypl.github.io/PYPL.html>`_. This is special true for the science research community because it is an open language, easy to learn, with a strong support community and with a lot of libraries available.

Questions?
==========
If you have any questions or want to report a problem with this library please fill in an issue `here <https://bitbucket.org/fchampalimaud/pybpod-api/issues>`_.

.. high level toc tree

.. toctree::
   :hidden:
   :maxdepth: 2
   :includehidden:
   :caption: Getting started

   Introduction <self>
   getting_started/installing
   getting_started/running
   getting_started/writing_protocols
   getting_started/manual_interaction
   getting_started/firmware_update
   getting_started/output_action_codes
   getting_started/event_codes

.. toctree::
   :hidden:
   :maxdepth: 4
   :includehidden:
   :caption: API reference

   api_reference/pybpodapi/index

.. toctree::
   :hidden:
   :maxdepth: 4
   :includehidden:
   :caption: About

   about/about

.. toctree::
   :hidden:
   :maxdepth: 2
   :includehidden:
   :caption: Contents

   contents

