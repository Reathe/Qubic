from ursina import *

sys.path.append("./src")

from ui.menu.main import MainMenu

if __name__ == '__main__':
	app = Ursina()
	menu_button = Button(texture='return_menu_button',
	                     scale=0.05,
	                     origin=(-0.5, 0.5),
	                     position=(-0.5 * window.aspect_ratio, 0.5),
	                     on_click=lambda: (scene.clear(), MainMenu()),
	                     eternal=True
	                     )
	MainMenu()
	app.run()
