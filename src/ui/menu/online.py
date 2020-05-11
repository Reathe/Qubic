from ursina import *

from composite import Composite
from game_modes import Online
from networking.client import Client
from qubic_settings import Settings
from ui.general_ui import QubicButtonList


class OnlineUserSettings(Settings):
	def default(self):
		pass

	def __init__(self):
		super().__init__('OnlineUserSettings')
		self.user_id = None
		self.user_name = None


class OnlineMenu(Composite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.components.append(self.__titre())
		self.settings = OnlineUserSettings()
		try:
			# TODO: enelever ça
			raise IOError
			self.settings.load()
		except IOError:
			# TODO: ask user for his name
			self.settings.user_id = Client('Player').id
			self.settings.user_name = 'Player'
			self.settings.default()
			self.settings.save()

		self.client = Client(self.settings.user_name, self.settings.user_id)
		gm = self.__game_list()
		self.components.append(gm)
		self.__auto_refresh_list(gm).start()
		self.components.append(self.__create_game_button())

	def __titre(self, **kwargs):
		return Text(text='Qubic',
		            position=(-0.3 * window.aspect_ratio, 0.25),
		            origin=(0, 0),
		            scale=2,
		            **kwargs)

	def __game_button_dict(self):
		bd = {}

		def button_online_game(room):
			if self.client.join(room.id, False):
				destroy(self)
				Online(self.client)
			else:
				# TODO: show to user
				print("Room cannot be joined")

		bd['Name - Players - Specs - Other'] = lambda: 0
		for room in self.client.room_list():
			label = f'{room.name} -' \
			        f' {len(room.players)}/2 -' \
			        f' {len(room.spectators)}'
			while label in bd:
				label += ' '
			bd[label] = lambda: button_online_game(room)
		return bd

	def __game_list(self):
		return QubicButtonList(self.__game_button_dict())

	def __auto_refresh_list(self, button_list: QubicButtonList):
		def refresh(button_list):
			button_list.button_dict = self.__game_button_dict()

		return Sequence(1, Func(refresh, button_list), loop=True)

	def __create_game_button(self):
		def f():
			r = self.client.create('Room default name')

		# TODO: self.client.join(r, False)

		return Button(texture='create_game_button',
		              scale=0.1,
		              position=(0.3, 0.4),
		              on_click=f,
		              tooltip=Tooltip('Create a room')
		              )
