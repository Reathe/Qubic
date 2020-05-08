from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenuButton


class QubicButton(DropdownMenuButton):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class QubicButtonList(ButtonList):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.add_script(Scrollable())
