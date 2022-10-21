# vram 사전 할당 해제
import tensorflow as tf

gpu_devices = tf.config.experimental.list_physical_devices("GPU")
tf.config.experimental.set_memory_growth(gpu_devices[0], True)

# gui 연결
import gui.gui_main as guim

guim.createdGuiShow()
guim.pyqtAppExec()
