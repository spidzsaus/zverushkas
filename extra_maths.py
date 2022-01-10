import math
from extra_types import DefaultValue

class Vector2:
    _angle = DefaultValue

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def angle(self):
        if self._angle is DefaultValue:
            from math import atan2
            self._angle = atan2(self.y, self.x)
        return self._angle

    def tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vector2(self.x // other, self.y // other)

    def __mod__(self, other):
        return Vector2(self.x % other, self.y % other)

    def __eq__(self, other):
        return self.tuple() == other.tuple()

    def round(self):
        return Vector2(round(self.x), round(self.y))

    def int(self):
        return Vector2(int(self.x), int(self.y))

    def __iter__(self):
        return self.tuple().__iter__()

    def map(self, f):
        return Vector2(f(self.x), f(self.y))

    def __hash__(self):
        return hash(self.tuple())

    def __iadd__(self, other):
        self = self + other
        return self

    def __isub__(self, other):
        self = self - other
        return self

    def __imul__(self, other):
        self = self * other
        return self

    def __itruediv__(self, other):
        self = self / other
        return self

    def __ifloordiv__(self, other):
        self = self // other
        return self

    def __str__(self):
        sx, sy = str(self.x), str(self.y)
        sx = sx[:sx.find('.') + 3]
        sy = sy[:sy.find('.') + 3]
        return f'({sx};{sy})'

    def __repr__(self):
        return f'Vector2({self.x}, {self.y})'

    def __getitem__(self, key):
        return self.tuple()[key]

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        from math import sqrt
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def unit(self):
        return self / self.length()
    
    def mimic(self, other):
        self.x = other.x
        self.y = other.y
        return self
    
    def copy(self):
        return Vector2(self.x, self.y)

    @classmethod
    def pointed(cls, length, degree):
        from math import sin, cos
        vec =  cls(length * cos(degree),
                   length * sin(degree))
        vec._angle = degree
        return vec

class VectorChain:
    def __init__(self, *vecs):
        self.vectors = vecs
    
    def __len__(self):
        return len(self.vectors)

    def cast_ik(self, start, dest):
        from math import acos, pi, degrees
        def pair_ik(a, b, start, dest):
            v = start - dest
            c = v.length()
            if a + b > c and a + c > b and b + c > a:
                beta = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
                angle = acos(beta) - pi * 1.5
                vec1 = Vector2.pointed(a, angle)
                return [vec1,
                        start - vec1 - dest]
            else:
                unit = v / c
                return [unit * a,
                        unit * b]
        
        if not self.count == 2:
            return NotImplemented
        chain = pair_ik(self.vectors[0].length(), 
                       self.vectors[1].length(),
                       start, dest)
        return [vec1.mimic(vec2) for vec1, vec2 in zip(self.vectors, chain)]

    @property
    def count(self):
        return len(self.vectors)
    
    def average_length(self):
        return self.length() / self.count
    
    def length(self):
        return sum(map(lambda x: x.length(), self.vectors))
    
    def __iter__(self):
        return iter(self.vectors)

    def __getitem__(self, key):
        return self.vectors.__getitem__(key)


def musrand(seed):
    a = int(seed)
    b = a + 1
    for _ in range(10):
        a = (a * 578194587349012378941734 + 174290425205728957) // 100000000
        b = (b * 578194587349012378941734 + 174290425205728957) // 100000000
    a = (a % 671049582825) / 671049582825
    b = (b % 671049582825) / 671049582825
    point = seed - int(seed)
    return a + ((b - a) * point ** 3 * (point * (point * 6 - 15) + 10))

def randint(seed, min, max):
    r = max - min
    return min + int(musrand(seed) * 10 ** len(str(r))) % r

def perlin1d(seed, x):
    a = int(x)
    b = a + 1
    dots = [(randint(seed ^ a, -100, 100) / 100) * (x - a),
            (randint(seed ^ b, -100, 100) / 100) * (x - b)]
    s = smoothstep(x - a)
    return lerp(*dots, s)

def lerp(a, b, t):
    return a + t * (b - a)

def smoothstep(t):
    return t * t * (3. - 2. * t)

def musnoise1d(seed, x):
    cP = int(x)
    d = x - cP
    fR = randint(seed ^ cP, -10, 10)
    cR = randint(seed ^ cP + 1, -10, 10)
    return lerp(fR, cR, d) / 10


class Expression:
    def __init__(self):
        self.operators = []

    def __add__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__add__', other))
        return ret

    def __radd__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__add__', other))
        return ret

    def __mul__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__mul__', other))
        return ret
    
    def __rmul__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__mul__', other))
        return ret
    
    def __truediv__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__truediv__', other))
        return ret  

    def __rtruediv__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__rtruediv__', other))
        return ret

    def __sub__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__sub__', other))
        return ret

    def __rsub__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__rsub__', other))
        return ret

    def __pow__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__pow__', other))
        return ret
    
    def __rpow__(self, other):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__rpow__', other))
        return ret

    def abs(self):
        ret = Expression()
        ret.operators = self.operators[:]
        ret.operators.append(('__abs__', None))
        return ret

    def __call__(self, x):
        result = x
        for operation, attrib in self.operators:
            if isinstance(attrib, Expression):
                attrib = attrib(x)
            if attrib is None:
                result = result.__getattribute__(operation)()
            else:
                result = result.__getattribute__(operation)(attrib)
        return result

x = Expression()