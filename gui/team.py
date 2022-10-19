from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

ui_path = os.path.dirname(os.path.realpath(__file__)) + "/team.ui"

form_class = uic.loadUiType(ui_path)[0]


class TeamGUI(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.setWindowTitle("제작자 정보")
