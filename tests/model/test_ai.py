import unittest

from model.ai import NegaMax
from model.pion import PionBlanc, PionNoir
from model.qubic import Qubic


class TestAI(unittest.TestCase):
	def test_nega_max(self):
		nm = NegaMax()
		test_ai(nm)


def test_ai(ai, qubic_args=(), *args, **kwars):
	q = Qubic(*qubic_args)
	nb_game = 1
	white_win = 0
	black_win = 0
	for game in range(1, nb_game + 1):
		print(f'Game {game}:')
		i = 0
		while not q.fini:
			q.poser(ai.play(q))
			i += 1
			print(f"{i} move(s) played ({100 * i / (len(q) ** 3):.2f}%)")
		if q.winner == PionBlanc:
			white_win += 1
		elif q.winner == PionNoir:
			black_win += 1
		else:
			raise Exception
		print(f"{white_win} white win(s) ({100 * white_win / game:.2f}%)")
		print(f"{black_win} black win(s) ({100 * black_win / game:.2f}%)")
		print(f"{game - white_win - black_win} draw(s) ({100 * (game - white_win - black_win) / game:.2f}%)")
		q.reset()


if __name__ == '__main__':
	unittest.main()
