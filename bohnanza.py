from random import randint

class Die(object):
	def __init__(self, faces):
		super(Die, self).__init__()
		self.faces = faces

	def roll(self):
		return self.faces[randint(0, len(self.faces) - 1)]

class WhiteDie(Die):
	def __init__(self):
		super(WhiteDie, self).__init__(['black', 'black', 'blue', 'orange', 'yellow', 'red'])

class BrownDie(Die):
	def __init__(self):
		super(BrownDie, self).__init__(['blue', 'blue', 'purple', 'purple', 'orange', 'green'])

class Task(object):
	def probability(self, dice, n=100000):
		return sum([self.check([die.roll() for die in dice]) for _ in range(n)]) / n

class CountTask(Task):
	def __init__(self, count):
		super(CountTask, self).__init__()
		self.count = count
	
	def check(self, faces):
		return all([sum([face == color for face in faces]) >= self.count[color] for color in self.count])

class AnyTask(Task):
	def __init__(self, tasks):
		super(AnyTask, self).__init__()
		self.tasks = tasks
		
	def check(self, faces):
		return any([task.check(faces) for task in self.tasks])

class ThreeBlueTask(Task):
	def check(self, faces):
		return sum([face == 'blue' for face in faces]) >= 3

class ThreeBlackOrTwoYellowTask(Task):
	def check(self, faces):
		return sum([face == 'black' for face in faces]) >= 3 or sum([face == 'yellow' for face in faces]) >= 2

class TwoPurpleAndOneBlackTask(Task):
	def check(self, faces):
		return sum([face == 'purple' for face in faces]) >= 2 and sum([face == 'black' for face in faces]) >= 1

if __name__ == '__main__':
	dice = [WhiteDie(), WhiteDie(), WhiteDie(), WhiteDie(), BrownDie(), BrownDie(), BrownDie()]
	print('3 blues', ThreeBlueTask().probability(dice))
	print('3 blues', CountTask({'blue': 3}).probability(dice))
	print('2 purples and 1 black', TwoPurpleAndOneBlackTask().probability(dice))
	print('2 purples and 1 black', CountTask({'black': 1, 'purple': 2}).probability(dice))
	print('3 blacks or 2 yellow', ThreeBlackOrTwoYellowTask().probability(dice))
	print('3 blacks or 2 yellow', AnyTask([CountTask({'black': 3}), CountTask({'yellow': 2})]).probability(dice))
