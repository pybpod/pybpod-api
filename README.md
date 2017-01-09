# PyControlGUI

**PyControlGUI** is a *Graphical User Interface (GUI)* for the [PyControl framework](https://bitbucket.org/takam/pycontrol/wiki/Home). It is written in Python3 and built on top of [PyForms](https://github.com/UmSenhorQualquer/pyforms) and [PyControlAPI](https://bitbucket.org/fchampalimaud/pycontrol-api) libraries.

![pyControlGUI frontpage](https://bytebucket.org/fchampalimaud/pycontrol-gui/wiki/media/PyControlGUI_layers.png?rev=bae0cf0ae21f0f7cffade1f2e76645e84530d5a6)

Please see [Wiki](https://bitbucket.org/fchampalimaud/pycontrol-gui/wiki/Home) for more information.

## Distribution

**PyControlGUI** is distributed as a standalone executable for Mac and Windows:

* [Windows installer](https://bitbucket.org/fchampalimaud/pycontrol-gui/downloads)
* [Mac installer](https://bitbucket.org/fchampalimaud/pycontrol-gui/downloads)


## Development
First, install [PyForms](https://github.com/UmSenhorQualquer/pyforms):

    pip install https://github.com/UmSenhorQualquer/pyforms/archive/master.zip

Then, install [PyControlAPI](https://bitbucket.org/fchampalimaud/pycontrol-api):

    pip install https://bitbucket.org/fchampalimaud/pycontrolapi/get/master.zip

Finally, run it:

	python3 -m pycontrolgui
	
## Setting environment

PyControlGUI relies on [PyForms](https://github.com/UmSenhorQualquer/pyforms) which relies on PyQt4. Please refer to the PyForms documentation on how to set the environment.