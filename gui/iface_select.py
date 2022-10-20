from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import os

ui_path = os.path.dirname(os.path.realpath(__file__)) + "/iface_select.ui"

form_class = uic.loadUiType(ui_path)[0]


class IfaceSelectGUI(QDialog, form_class):
    def __init__(self, iflist):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(960, 360)

        self.iface_index = None
        for a in iflist:
            self.listWidget.addItem(a)

        self.listWidget.itemDoubleClicked.connect(self.setIndex)

    def setIndex(self):
        row = self.listWidget.currentRow()
        for i in range(row, -1, -1):
            item_split = list(filter(None, self.listWidget.item(i).text().split(" ")))

            if item_split[0] == "libpcap":
                self.iface_index = item_split[1]
                # print(self.iface_index)
                break
            else:
                if i == 0:
                    print("뭔가 잘못됨")
                    break
        QCoreApplication.instance().quit()

    def getIndex(self):
        return self.iface_index


# app = QApplication(sys.argv)
# myWindow = IfaceSelectGUI()
# myWindow.show()
# app.exec_()
