


def TimeBonus(data):
	data.start = not data.start
	data.powerUpColor = "Green"
	if data.start:
		data.timer += 10
		data.currPowerUpName = "+10 seconds!"

def DoublePower(data):
	data.start = not data.start
	data.powerUpColor = "Green"
	if data.start:
		data.slider.multiplier = 50
		data.currPowerUpName = "2x Power!"
	else: data.slider.multiplier = 35
	

def EasyScoring(data):
	data.start = not data.start
	data.powerUpColor = "Green"
	if data.start:
		for hole in data.holes:
			hole.r = 40
		data.currPowerUpName = "Easy Scoring!"
	else: 
		for hole in data.holes:
			hole.r = 22
	

def TimeLost(data):
	data.start = not data.start
	data.powerUpColor = "Red"
	if data.start:
		data.timer -= 10
		data.currPowerUpName = "-10 seconds..."
	

def HalfPower(data):
	data.start = not data.start
	data.powerUpColor = "Red"
	if data.start:
		data.slider.multiplier = 15
		data.currPowerUpName = "Half Power..."
	else: data.slider.multiplier = 35
	

def HardScoring(data):
	data.start = not data.start
	data.powerUpColor = "Red"
	if data.start:
		for hole in data.holes:
			hole.r = 17
		data.currPowerUpName = "Hard Scoring..."
	else: 
		for hole in data.holes:
			hole.r = 22
	



