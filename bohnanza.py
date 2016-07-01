from random import randint

class Die(object):
	def __init__(self, faces):
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
		self.count = count

	def check(self, faces):
		return all([sum([face == color for face in faces]) >= self.count[color] for color in self.count])

class AnyTask(Task):
	def __init__(self, tasks):
		self.tasks = tasks

	def check(self, faces):
		return any([task.check(faces) for task in self.tasks])

class AllTask(Task):
	def __init__(self, tasks):
		self.tasks = tasks

	def check(self, faces):
		return all([task.check(faces) for task in self.tasks])

if __name__ == '__main__':
	dice = [WhiteDie(), WhiteDie(), WhiteDie(), WhiteDie(), BrownDie(), BrownDie(), BrownDie()]
	print('3 blues', CountTask({'blue': 3}).probability(dice))
	print('2 purples and 1 black', CountTask({'black': 1, 'purple': 2}).probability(dice))
	print('3 blacks or 2 yellow', AnyTask([CountTask({'black': 3}), CountTask({'yellow': 2})]).probability(dice))
	print('2.5 blues and 2.5 orange', AnyTask([CountTask({'blue': 3, 'orange': 2}), CountTask({'blue': 2, 'orange': 3})]).probability(dice))
