from PyQt4 import QtCore, QtGui, uic
import sys, os, re

uiFile = os.path.realpath(__file__).replace(".py", ".ui")

class MyLineEditWin(QtGui.QMainWindow):
    """
    examples of QLineEdit signals, actions, ect...
    """
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent=parent)
        uic.loadUi(uiFile, self)
        self._validator = MyCustomValidator(self)
        self.connectTxtEditSignal()
        self.connectSignals()
    
    def connectSignals(self):
        self.cursorPosChanged_LineEdit.cursorPositionChanged.connect(self.posChangedCmd)
        self.editingFinished_LineEdit.editingFinished.connect(self.editingFCmd)
        self.returnPressed_LineEdit.returnPressed.connect(self.returnPressedCmd)
        self.selectionChanged_LineEdit.selectionChanged.connect(self.selChangedCmd)
        self.textChanged_LineEdit.textChanged.connect(self.txtChangedCmd)
        self.textEdited_LineEdit.textEdited.connect(self.txtEditedCmd)
        self.trigger_pushButton.clicked.connect(self.addStringCmd)

    def posChangedCmd(self, x, y):
        self._updateResults("---> cursor pos changed, pos {}:{}".format(x, y))

    def editingFCmd(self):
        self._updateResults("---> editingFinished")

    def returnPressedCmd(self):
        self._updateResults("---> return pressed")
        self.check_state()
        
    def selChangedCmd(self):
        self._updateResults("---> selection Changed")

    def txtChangedCmd(self, inputTxt):
        self._updateResults("---> text changed, inputText: " + inputTxt)

    def txtEditedCmd(self, inputTxt):
        self._updateResults("---> text Edited, inputText: " + inputTxt)

    def addStringCmd(self):
        self._updateResults("^^^ adding '-a-' programmatically to all lineEdits ^^^\n")
        lineEdits = [self.cursorPosChanged_LineEdit,
                     self.editingFinished_LineEdit,
                     self.returnPressed_LineEdit,
                     self.selectionChanged_LineEdit,
                     self.textChanged_LineEdit,
                     self.textEdited_LineEdit]
        for le in lineEdits:
            le.setText(le.text() + "-a-")
    
    def check_state(self):
        sender = self.sender()# what is sending the signal
        if isinstance(sender, QtGui.QLineEdit):
            if sender.objectName() == "returnPressed_LineEdit":
                self.returnPressed_LineEdit.setValidator(self._validator)
                validator = sender.validator()
                state = validator.validate(sender.text(), 0)[0]
                if state == QtGui.QValidator.Acceptable:
                    color = '#c4df9b' # green
                elif state == QtGui.QValidator.Intermediate:
                    color = '#c4df9b' # green
                    newText = validator.fixup(sender.text())
                    sender.setText(newText)
                else:
                    color = '#f6989d' # red
                sender.setStyleSheet('QLineEdit { background-color: %s }' % color) #adding color to lineEdit's input area
                self.returnPressed_LineEdit.setValidator(None)

#-------------------------------------------
#   results methods
#-------------------------------------------
    def connectTxtEditSignal(self):
        self.clear_pushButton.clicked.connect(self.clearResults)

    def clearResults(self):
        self.result_textEdit.setText("")

    def _updateResults(self, inputTxt):
        currentTxt = str(self.result_textEdit.toPlainText())
        if currentTxt:
            self.result_textEdit.setText(inputTxt + "\n" + currentTxt)
        else:
            self.result_textEdit.setText(inputTxt)


#-------------------------------------------
#   QValidator Example for editing finishing & return pressed signals
#-------------------------------------------
class MyCustomValidator(QtGui.QValidator):
    """
    reference links for notes
    https://stackoverflow.com/questions/23101267/pyqt-qvalidator-function-definition
    https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-using-qvalidator/

    input string must contain "--TEST--" and only 1 number
    QRegExpValidator is another option

    """
    def __init__(self, parent=None):
        QtGui.QValidator.__init__(self, parent)

    def validate(self, inputStr, pos):
        patterns = ['\D+(--TEST--)?\D+\d\D*', '\D+\D+\d\D*']
        for pattern in patterns:
            matchObj = re.search(pattern, inputStr)
            result = self._matchResult(matchObj, inputStr)
            if result in [QtGui.QValidator.Acceptable, QtGui.QValidator.Intermediate]:
                break
        return (result, pos)

    def fixup(self, inputStr):
        inputStr.push_front("--TEST-- ")
        return inputStr

    def _matchResult(self, matchObj, inputStr):
        if bool(matchObj):
            if matchObj.group(0) == inputStr:
                if len(matchObj.groups()) and matchObj.group(1) == "--TEST--":
                    return QtGui.QValidator.Acceptable
                return QtGui.QValidator.Intermediate
        return QtGui.QValidator.Invalid

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = MyLineEditWin()
    w.show()
    sys.exit(app.exec_())