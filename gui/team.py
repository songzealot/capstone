from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic
import os

# UI 파일 로드
ui_path = os.path.dirname(os.path.realpath(__file__)) + "/team.ui"
form_class = uic.loadUiType(ui_path)[0]

# 팀 로고 파일 로드
logo_path = os.path.dirname(os.path.realpath(__file__)) + "/team_logo.png"


####################################################################################################


class TeamGUI(QDialog, form_class):
    # 팀 소개 페이지
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 페이지 크기 고정
        self.setFixedSize(400, 430)

        # 팀 로고 표시
        self.team_logo.setPixmap(QtGui.QPixmap(logo_path))
