from ctypes import cdll
import os

os.add_dll_directory(os.path.dirname(__file__))

dirpath = os.path.dirname(__file__) + "\DLL20220722.dll"
# pt = cdll.LoadLibrary(dirpath)
pt = cdll.LoadLibrary("./DLL20220722.dll")
pt.Test()
os.system("pause")

# 임시로 만들어진 프로그램
# 받아오는 패킷에서 nsl-kdd 특징 중 1~9번, 23번부터 41번까지 총 28개의 특징을 추출
# Ctrl + C로 프로그램 종료
# 생성되는 파일은 txt 형식
