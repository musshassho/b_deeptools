
import nuke
import os
import json
from nukescripts import panels
import sys
import nuke

if nuke.NUKE_VERSION_MAJOR < 11: # < nuke11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
else: # > nuke11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets
