from ursina import *

from model.qubic import Qubic
from ui.qubic.vue_qubic import VueQubic
from ui.qamera.qamera_locked import QameraLocked

if __name__ == '__main__':
	app = Ursina()
	cam = QameraLocked()
	qbic = Qubic()
	VueQubic(qbic)

	app.run()
