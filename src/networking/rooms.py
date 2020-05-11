import string
from typing import List, Dict
from uuid import uuid4

from model.qubic import Qubic


class Player:
	def __init__(self, id, name):
		self.id = id
		self.name = name

	def __repr__(self):
		return f'Player[{self.name}, {self.id}]'


class Room:
	players: List[Player]

	def __init__(self, id, room_name, private=False, taille: int = 4, gravite: bool = True):
		self.id = id
		self.private = private
		self.players = []
		self.spectators = {}
		self.qubic = Qubic(taille, gravite)

		if room_name:
			self.name = room_name
		else:
			self.name = self.id

	def join(self, player, spectator=False):
		"""
        Add player to room
        """
		if player in self.players or player.id in self.spectators:
			raise AlreadyJoined
		if spectator:
			self.spectators[player.id] = player
		elif not self.is_full():
			self.players.append(player)
		else:
			raise RoomFull

	def leave(self, player):
		"""
        Remove player from room
        """
		if player in self.players:
			self.players.remove(player)
		elif player.id in self.spectators:
			self.spectators.pop(player.id)
		else:
			raise NotInRoom()

	def is_empty(self):
		"""
        Check if room has any players
        """
		return len(self.players) == 0

	def is_full(self):
		"""
        Check if room is full or not
        """
		return len(self.players) >= 2

	def is_in_room(self, player_id):
		"""
        Check if player is in room
        """
		for player in self.players:
			if player.id == player_id:
				return True
		return False

	def is_player_turn(self, player_id):
		"""
		Args:
			player_id: the player

		Returns:
			if its player_id's turn
		"""
		if len(self.players) != 2:
			return False

		if self.qubic.tour_blanc():
			return player_id == self.players[0].id
		elif self.qubic.tour_noir():
			return player_id == self.players[1].id
		else:
			return False

	def __str__(self):
		private = "private," if self.private else "public,"
		return (f" Room[name: '{self.name}',"
		        f" id: {self.id},"
		        f" {private}"
		        f" Players: {self.players},"
		        f" Specs: {list(self.spectators.values())}]")


class Rooms:
	_rooms = Dict[str, Room]
	players = Dict[str, Player]

	def __init__(self):
		self._rooms = {}
		self.players = {}

	@property
	def public_rooms_id(self):
		"""a list of all public room ids"""
		return [rid for rid in self.public_rooms]

	@property
	def public_rooms(self):
		"""a list of all public rooms"""
		return [room for room in self._rooms.values() if not room.private]

	@property
	def rooms(self):
		"""a list of all rooms"""
		return [room for room in self._rooms.values()]

	def __getitem__(self, room_id):
		"""
		Args:
			room_id: the rooms id

		Returns:
			the room
		"""
		return self._rooms[room_id]

	def register(self, player_name: string) -> Player:
		"""
		Registers a new player

		Args:
			player_name: the players name

		Returns: the created player
		"""
		player = Player(str(uuid4()), player_name)
		self.players[player.id] = player
		return player

	def create(self, room_name=None, private=False) -> str:
		"""
		Creates a new room

		Args:
			room_name: the __rooms name
			private: if set to true, the room will not be visible to other players, they would need the id to access it

		Returns: the room id
		"""
		identifier = str(uuid4())
		self._rooms[identifier] = Room(identifier, room_name, private=private)
		return identifier

	def join(self, player_id, room_id=None, spectator=False) -> str:
		"""
		Add player to room

		Args:
			player_id: the players id
			room_id: the __rooms id
			spectator: if the player joins as a spectator

		Returns:
			the joined __rooms id
		"""
		if player_id not in self.players:
			raise ClientNotRegistered()

		player = self.players[player_id]

		if room_id is None:
			for id, room in self._rooms:
				if not room.private:
					room_id = id

		if room_id in self._rooms:
			self._rooms[room_id].join(player, spectator)
			return room_id
		else:
			raise RoomNotFound()

	def leave(self, player_identifier, room_id):
		"""
        Removes a player (or spec) from a room

        Raises RoomNotFound
		Args:
			player_identifier: the player to be removed
			room_id: the room from wich he will be removed
		"""
		if player_identifier not in self.players:
			raise ClientNotRegistered()

		player = self.players[player_identifier]

		if room_id in self._rooms:
			self._rooms[room_id].leave(player)
			if self._rooms[room_id].is_empty():
				del self._rooms[room_id]
		else:
			raise RoomNotFound()

	def remove_empty(self):
		"""
        Delete empty __rooms
        """
		for room_id in self._rooms:
			if self._rooms[room_id].is_empty():
				del self._rooms[room_id]


class AlreadyJoined(Exception):
	pass


class RoomFull(Exception):
	pass


class RoomNotFound(Exception):
	pass


class NotInRoom(Exception):
	pass


class ClientNotRegistered(Exception):
	pass
