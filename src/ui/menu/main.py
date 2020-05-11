from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu

from controls import LocalController
from game_modes import OneVOne
from model.qubic import Qubic
from composite import Composite
from ui.general_ui import QubicButton
from ui.menu.online import OnlineMenu
from ui.qubic.vue_qubic import VueQubic


class MainMenu(Composite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		q = Qubic()
		comp = (
			self.__bouton_local(),
			self.__button_online_game(),
			VueQubic(q, LocalController(q)),
			self.__titre()
		)
		for c in comp:
			self.components.append(c)

	def __titre(self, **kwargs):
		return Text(text='Qubic',
		            position=(0 * window.aspect_ratio, 0.25),
		            origin=(-0.5, 0),
		            text_scale=10,
		            **kwargs)

	def __bouton_local(self, **kwargs):
		return DropdownMenu(text='Jeu en local',
		                    position=(0.5 * window.aspect_ratio * -0.8, 0.5),
		                    buttons=(self.__bouton_1v1(),
		                             QubicButton(text="1 vs IA")
		                             ),
		                    **kwargs)

	def __bouton_1v1(self, **kwargs):
		return QubicButton(text="1 vs 1",
		                   on_click=lambda: (destroy(self), OneVOne()),
		                   **kwargs)

	def __button_online_game(self, **kwargs):
		return QubicButton(text="Online game",
		                   position=(0.5 * window.aspect_ratio * -0.52, 0.5),
		                   on_click=lambda: (destroy(self), OnlineMenu()),
		                   **kwargs)
