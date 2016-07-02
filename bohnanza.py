from random import randint
from collections import Counter
import sys

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
		return sum((self.check([die.roll() for die in dice]) for _ in range(n))) / n

class CombinationTask(Task):
	def __init__(self, count):
		self.count = count

	def check(self, faces):
		return all((sum((face == color for face in faces)) >= self.count[color] for color in self.count))

class AnyTask(Task):
	def __init__(self, tasks):
		self.tasks = tasks

	def check(self, faces):
		return any((task.check(faces) for task in self.tasks))

class AllTask(Task):
	def __init__(self, tasks):
		self.tasks = tasks

	def check(self, faces):
		return all((task.check(faces) for task in self.tasks))

class ExceptTask(Task):
	def __init__(self, colors, total=7):
		self.colors = colors
		self.total = total

	def check(self, faces):
		return len(faces) >= self.total and not any((face == color for face in faces for color in self.colors))

class TuplesTask(Task):
	def __init__(self, size, tuples):
		self.size = size
		self.tuples = tuples

	def check(self, faces):
		c = Counter(faces)
		return sum((c[color] >= self.size for color in c)) >= self.tuples

class CountTask(Task):
	def __init__(self, total, colors):
		self.total = total
		self.colors = colors

	def check(self, faces):
		return sum((face in self.colors for face in faces)) >= self.total

class ColorCountTask(Task):
	def __init__(self, count):
		self.count = count

	def check(self, faces):
		return len(Counter(faces)) >= self.count

class FullHouseTask(Task):
	def __init__(self, color1, color2=None, total=5, count1=3):
		self.color1 = color1
		self.color2 = color2
		self.total = total
		self.count1 = count1
		self.count2 = total - count1
		if self.count1 < self.count2:
			self.count1, self.count2 = self.count2, self.count1

	def check(self, faces):
		c = Counter(faces)
		c1 = c[self.color1]
		if c1 >= self.count1:
			c2 = self.count2
		elif c1 >= self.count2:
			c2 = self.count1
		else:
			return False
		if self.color2 is None:
			return any((c[color] >= c2 for color in c if color != self.color1))
		else:
			return c[self.color2] >= c2

if __name__ == '__main__':
	try:
		n = int(sys.argv[1])
	except:
		n = 2**16

	dice = [WhiteDie(), WhiteDie(), WhiteDie(), WhiteDie(), BrownDie(), BrownDie(), BrownDie()]
	print('3 blues', CombinationTask({'blue': 3}).probability(dice, n=n))
	print('2 purples and 1 black', CombinationTask({'black': 1, 'purple': 2}).probability(dice, n=n))
	print('3 blacks or 2 yellow', AnyTask([CombinationTask({'black': 3}), CombinationTask({'yellow': 2})]).probability(dice, n=n))
	print('2.5 blues and 2.5 orange', AnyTask([CombinationTask({'blue': 3, 'orange': 2}), CombinationTask({'blue': 2, 'orange': 3})]).probability(dice, n=n))
	print('2.5 blues and 2.5 orange (full house)', FullHouseTask('blue', 'orange').probability(dice, n=n))
	print('Anything except yellow or purple', ExceptTask(['yellow', 'purple']).probability(dice, n=n))
	print('3 pairs', TuplesTask(2, 3).probability(dice, n=n))
	print('2 triples', TuplesTask(3, 2).probability(dice, n=n))
	print('1 triple', TuplesTask(3, 1).probability(dice, n=n))
	print('Combination of 4 red / purple', CountTask(4, {'red', 'purple'}).probability(dice, n=n))
	print('6 different colors', ColorCountTask(6).probability(dice, n=n))
	print('7 different colors', ColorCountTask(7).probability(dice, n=n))
	print('Full house orange / other', FullHouseTask('orange').probability(dice, n=n))
