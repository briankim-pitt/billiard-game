#classes specific for multiplayer


class ScoreBar(object):
	def __init__(self):
		self.width = 50
		self.height = 200
		self.balls = []

class Player(object):
	def __init__(self, ballType):
		self.ballType = ballType
		self.turns = 0
		self.hasScoredAll = False


		



	