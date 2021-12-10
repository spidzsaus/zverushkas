class Category:
    def __init__(self, default=0):
        self.default = 0
    
    def __getattr__(self, value):
        return self.default
    
    def __str__(self):
        output = ''
        for key, value in self.__dict__.items():
            output += f'| {key}: \t {value}' '\n'
        return output
    
    def copy(self):
        c = Category()
        for key, value in self.__dict__.items():
            c.__setattr__(key, value)
        return c

class Enum:
    def __init__(self, *modes):
        self.indexes = []
        for mode in modes:
            obj = object()
            self.__setattr__(mode, obj)
            self.indexes.append(obj)

    def __getitem__(self, value):
        return self.indexes[value]

class Animal:
    def __init__(self):
        self.spine = Category(0)
        self.legs = {}

    @staticmethod
    def from_seed(seed):
        from extra_maths import randint, perlin1d
        from math import pi
        animal = Animal()
        spine = Category(0)
        spine.length = randint(seed * 1931, 7, 15)
        spine.gradation = randint(seed * 2124, 1, 100) / 10
        spine.straightness = randint(seed * 6114, 1, 100) / 10
        spine.distribution = randint(seed * 5667, 50, 100) / 5
        spine.forced_length = 0.001
        spine.length_modifier  = 1
        spine.forced_angle = 0
        spine.curve_modifier = 1 #randint(seed * 3521, 25, 200) / 100
        spine.forced_width = 0.001
        spine.width_modifier = randint(seed * 3521, 25, 100) / 100
        spine.seed_v = seed * 10221
        spine.seed_h = seed * 26714
        spine.seed_w = seed * 51356
        animal.spine = spine

        joints = []
        yp = perlin1d(spine.seed_v, 0)
        for i in range(1, spine.length):
            y = perlin1d(spine.seed_v, i / spine.straightness)
            joints.append((i, y, abs(abs(y) - abs(yp))))
            yp = y
        joints.sort(key=lambda x: x[2], reverse=True)
        for i in range(2 + randint(seed * 14127, 0, 2)):
            leg = spine.copy()
            leg.forced_angle = joints[i][1] - pi / 2
            leg.width_modifier = 0.5
            leg.length = 5
            leg.forced_length = 0.001
            spine.seed_v = seed * 42839 * (i + 1)
            spine.seed_h = seed * 35231 * (i + 1)
            spine.seed_w = seed * 51618 * (i + 1)
            animal.legs[joints[i][0]] = leg
        return animal
    
    @staticmethod
    def from_params(length, gradation, straightness, 
                    distribution, seed):
        from extra_maths import randint, perlin1d
        
        return NotImplemented
        
        animal = Animal()
        spine = Category(0)
        spine.length = length
        spine.gradation = gradation
        spine.straightness = straightness
        spine.distribution = distribution
        spine.seed_v = seed * 10221
        spine.seed_h = seed * 26714
        spine.seed_w = seed * 51356
        animal.spine = spine
        
        joints = []
        yp = perlin1d(spine.seed_v, 0)
        for i in range(1, spine.lenght):
            y = perlin1d(spine.seed_v, i / spine.straightness)
            joints.append((i, abs(abs(y) - abs(yp))))
            yp = y
        joints.sort(key=lambda x: x[1], reverse=True)
        for i in range(2 + randint(seed * 14127, 0, 1)):
            animal.legs.append(joints[i][0] - 1)
        return animal


    @staticmethod
    def spine_to_vectors(spine: Category):
        from extra_maths import perlin1d, Vector2
        from math import pi
        output = []
        seedx = spine.seed_h
        seedy = spine.seed_v
        seedz = spine.seed_w
        divx = spine.gradation
        divy = spine.straightness
        divz = spine.distribution
        mulx = spine.length_modifier
        muly = spine.curve_modifier
        mulz = spine.width_modifier
        addx = spine.forced_length
        addy = spine.forced_angle
        addz = spine.forced_width
        for i in range(spine.length):
            x = (addx + abs(perlin1d(seedx, i / divx))) * mulx
            y = (addy + perlin1d(seedy, i / divy) * pi) * muly
            vec = Vector2.pointed(x, y)
            vec.z = (addz + abs(perlin1d(seedz, i / divz))) * mulz
            output.append(vec)
        return output
            
    def draw(self, draw, scale):
        from extra_maths import Vector2
        coords = Vector2(200, 1000)
        spine = Animal.spine_to_vectors(self.spine)
        i = 1
        for i, bone in enumerate(spine):
            bone.y *= -1
            newcoords = coords + (bone * scale)
            draw.line((coords.tuple(), newcoords.tuple()), fill=(165,
                                                                 15 * i,
                                                                 255),
                                                           width=int(bone.z * scale))
            coords = newcoords
            if i in self.legs:
                leg = Animal.spine_to_vectors(self.legs[i])
                dcoords = coords
                for j, bone in enumerate(leg):
                    bone.y *= -1
                    dnewcoords = dcoords + (bone * scale)
                    if j == len(leg) - 1:
                        dnewcoords.y = 1200
                    draw.line((dcoords.tuple(), dnewcoords.tuple()), fill=(25 * i,
                                                                           255,
                                                                           25 * i),
                                                                     width=int(bone.z * scale))
                    dcoords = dnewcoords                
        draw.ellipse(((newcoords - Vector2(10, 10)).tuple(),
                      (newcoords + Vector2(10, 10)).tuple()),
                     fill=(255, 0, 0))