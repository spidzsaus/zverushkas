class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    @classmethod
    def pointed(cls, length, degree):
        from math import sin, cos
        return cls(length * cos(degree),
                   length * sin(degree))

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