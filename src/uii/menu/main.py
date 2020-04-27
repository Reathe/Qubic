from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

from game_modes import OneVOne
from model.qubic import Qubic
from composite import Composite
from uii.qubic.vue_qubic import VueQubic


class BoutonJeu(DropdownMenuButton):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class MainMenu(Composite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		local = self.__bouton_local()
		self.components.append(local)
		self.components.append(VueQubic(Qubic()))
		self.components.append(self.__titre())

	def __titre(self, **kwargs):
		return Text(text='Qubic'
		            , position=(0 * window.aspect_ratio, 0.25)
		            , origin=(-0.5, 0)
		            , text_scale=10
		            , **kwargs)

	def __bouton_local(self, **kwargs):
		return DropdownMenu(text='Jeu en local'
		                    , position=(-0.5 * window.aspect_ratio * 0.8, 0.5)
		                    , buttons=(self.__bouton_1v1()
		                               , BoutonJeu(text="1 vs IA")
		                               )
		                    , **kwargs)

	def __bouton_1v1(self, **kwargs):
		return BoutonJeu(text="1 vs 1"
		                 , on_click=lambda: (destroy(self), OneVOne())
		                 , **kwargs)
# OneVOne(),
