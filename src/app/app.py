from ursina import *

from ui.menu.main import MainMenu
from ui.qamera.qamera_locked import QameraLocked

if __name__ == '__main__':
	app = Ursina()
	cam = QameraLocked()
	MainMenu()
	app.run()
