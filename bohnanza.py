from random import randint
from collections import Counter
import sys

class Die(object):
    def __init__(self, faces):
        self.faces = faces

    def __str__(self):
        return str(self.faces)

    def __repr__(self):
        return self.__str__()

    def roll(self):
        return self.faces[randint(0, len(self.faces) - 1)]

class MonoDie(Die):
    def __init__(self, face):
        self.face = face

    def __str__(self):
        return str(self.face)

    def __repr__(self):
        return self.__str__()

    def roll(self):
        return self.face

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
    def __init__(self, colors):
        self.colors = colors

    def __str__(self):
        return ', '.join(('%d %s%s' % (self.colors[color], color, 's' if self.colors[color] > 1 else '')
                            for color in self.colors))

    def check(self, faces):
        return all((sum((face == color for face in faces)) >= self.colors[color] for color in self.colors))

class AnyTask(Task):
    def __init__(self, tasks):
        self.tasks = tasks

    def __str__(self):
        return ' or '.join((str(task) for task in self.tasks))

    def check(self, faces):
        return any((task.check(faces) for task in self.tasks))

class AllTask(Task):
    def __init__(self, tasks):
        self.tasks = tasks

    def __str__(self):
        return ' and '.join((str(task) for task in self.tasks))

    def check(self, faces):
        return all((task.check(faces) for task in self.tasks))

class ExceptTask(Task):
    def __init__(self, colors, total=7):
        self.colors = colors
        self.total = total

    def __str__(self):
        return 'any %d dice except %s' % (self.total, ' or '.join(self.colors))

    def check(self, faces):
        return (len(faces) >= self.total
                and not any((face == color for face in faces for color in self.colors)))

class TuplesTask(Task):
    def __init__(self, size, tuples):
        self.size = size
        self.tuples = tuples

    def __str__(self):
        return '%d tuples of size %d' % (self.tuples, self.size)

    def check(self, faces):
        c = Counter(faces)
        return sum((c[color] >= self.size for color in c)) >= self.tuples

class CountTask(Task):
    def __init__(self, total, colors):
        self.total = total
        self.colors = colors

    def __str__(self):
        return 'any combination of %d %s' % (self.total, ' or '.join(self.colors))

    def check(self, faces):
        return sum((face in self.colors for face in faces)) >= self.total

class ColorCountTask(Task):
    def __init__(self, count):
        self.count = count

    def __str__(self):
        return '%d different colors' % self.count

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

    def __str__(self):
        if self.total == 5 and self.count1 == 3:
            return ('full house, one color %s, the other %s'
                        % (self.color1, 'free' if self.color2 is None else self.color2))
        else:
            return ('full house with %d dice, one tuple %d, the other %d, one color %s, the other %s'
                        % (self.total, self.count1, self.count2, self.color1,
                           'free' if self.color2 is None else self.color2))

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

    combinations = [
        {'blue': 3},
        {'black': 1, 'purple': 2},
        {'blue': 3, 'orange': 2}
    ]
    tasks = [CombinationTask(combination) for combination in combinations] + [
            AnyTask([CombinationTask({'black': 3}), CombinationTask({'yellow': 2})]),
            FullHouseTask('blue', 'orange'),
            FullHouseTask('orange'),
            ExceptTask(['yellow', 'purple']),
            TuplesTask(2, 3),
            TuplesTask(3, 2),
            TuplesTask(3, 1),
            TuplesTask(4, 1),
            CountTask(4, {'red', 'purple'}),
            ColorCountTask(6),
            ColorCountTask(7)
        ]
    extra_tasks = [
        CombinationTask({'blue': 2, 'black': 1}),
        CountTask(3, ['orange', 'green']),
        CombinationTask({'green': 1, 'black': 2})
    ]
    tasks += extra_tasks
    tasks += [AllTask(extra_tasks[:2]), AllTask(extra_tasks)]

    print(dice)
    for task in tasks:
        print('%s: %.1f%%' % (task, task.probability(dice, n=n) * 100))

    dice = dice[1:] + [MonoDie('black')]

    print(dice)
    for task in tasks:
        print('%s: %.1f%%' % (task, task.probability(dice, n=n) * 100))
