from ursina import *

from UI.Qamera.QameraLocked import QameraLocked
from UI.Qubic.VueQubic import VueQubic
from model.Qubic import Qubic

if __name__ == '__main__':
	app = Ursina()
	cam = QameraLocked()
	qbic = Qubic()
	VueQubic(qbic)

	app.run()
