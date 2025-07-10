import sys
from PyQt5 import QtWidgets, uic
app = QtWidgets.QApplication([])
win = uic.loadUi ("tugas1profile.ui")
win.show()
sys.exit(app.exec())