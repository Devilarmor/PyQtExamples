from PyQt4 import QtCore, QtGui, uic
import sys, os

uiFile = os.path.realpath(__file__).replace(".py", ".ui")

class MyPushbuttonWin(QtGui.QMainWindow):
    """
    examples of QpushButtons signals, actions, ect...
    """
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent=parent)
        uic.loadUi(uiFile, self)
        self.connectSignals()
    
    def connectSignals(self):
        self.clear_pushButton.clicked.connect(self.clearResults)
        self.clicked_pushButton.clicked.connect(self.clickCmd)
        self.pushed_pushButton.pressed.connect(self.pressedCmd)
        self.released_pushButton.released.connect(self.releasedCmd)
        self.toggled_pushButton.toggled.connect(self.toggledCmd)
        
        self.rightClick_pushButton.clicked.connect(self.clickCmd2)
        self.rightClick_pushButton.rightClicked.connect(self.rightClicked)

    def clickCmd(self):
        self._updateResults("---> Button click signal")

    def pressedCmd(self):
        self._updateResults("---> Button pushed signal")

    def releasedCmd(self):
        self._updateResults("---> Button released signal")

    def toggledCmd(self, toggledState):
        self._updateResults("---> Button toggled signal -returns " + str(toggledState))

    def clickCmd2(self):
        self._updateResults("----- please right click instead of left ------")

    def rightClicked(self):
        self._updateResults("---> Button rightClick(custom) signal")
#-------------------------------------------
#   results methods
#-------------------------------------------
    def clearResults(self):
        self.result_textEdit.setText("")

    def _updateResults(self, inputTxt):
        currentTxt = str(self.result_textEdit.toPlainText())
        if currentTxt:
            currentTxt += "\n"
        currentTxt += inputTxt
        self.result_textEdit.setText(currentTxt)

#-------------------------------------------
#   customise own QPushButton
#-------------------------------------------
class myCustomBtn(QtGui.QPushButton):

    rightClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent=parent)

    def contextMenuEvent(self, event):
        self.rightClicked.emit()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = MyPushbuttonWin()
    w.show()
    sys.exit(app.exec_())