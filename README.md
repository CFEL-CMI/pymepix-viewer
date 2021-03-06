# PymePix Viewer

PymePix-viewer is a basic graphical user interface for data acquisition using the [PymePix
library](https://github.com/CFEL-CMI/pymepix). It is not meant as a full-fledged and stable DAQ-GUI,
but to demonstrate the capabilities of [PymePix](https://github.com/CFEL-CMI/pymepix), to provide an
initial operational system for easy entrance to Timepix operation, and as a reference implementation
for [PymePix](https://github.com/CFEL-CMI/pymepix) use.


## Prerequisites

Obviously, you need [PymePix](https://github.com/CFEL-CMI/pymepix) to be operational.

For the PymePix viewer PyQt5 is a requirement. This can be installed [(painfully)
manually](https://www.metachris.com/2016/03/how-to-install-qt56-pyqt5-virtualenv-python3) or using
package managers such as [Anaconda](https://www.anaconda.com) (`conda install pyqt=5`), MacPorts
(`sudo port install py38-pyqt5`), or similar.


## Installing

In the pymepixviewer project folder run the installation script through
```
pip install .
```
or
```
python setup.py install
```
Standard `setuptools` options such as `develop` or `--user` are available; see, e.g., the
[PymePix documentation](https://pymepix.readthedocs.io) for some details.


## Running

To run the GUI start it from a terminal as
```
pymepixviewer
```

If the prerequisites are satisfied and a Timepix3cam is connected then a window should open. See the
[PymePix documentation](https://pymepix.readthedocs.io) for further details.




<!-- Put Emacs local variables into HTML comment
Local Variables:
coding: utf-8
fill-column: 100
End:
-->
