class Category:
    def __str__(self):
        output = ''
        for key, value in self.__dict__.items():
            output += f'| {key}: \t {value}' '\n'
        return output

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
        self.spine = Category()
        self.leg_points = []

    @staticmethod
    def from_seed(seed):
        from extra_maths import randint, perlin1d
        animal = Animal()
        spine = Category()
        spine.lenght = randint(seed * 1931, 7, 15)
        spine.gradation = randint(seed * 2124, 1, 100) / 10
        spine.straightness = randint(seed * 6114, 1, 100) / 10
        spine.distribution = randint(seed * 5667, 50, 100) / 5
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
            animal.leg_points.append(joints[i][0])
        return animal
    
    @staticmethod
    def from_params(length, gradation, straightness, 
                    distribution, seed):
        from extra_maths import randint, perlin1d
        animal = Animal()
        spine = Category()
        spine.lenght = length
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
            animal.leg_points.append(joints[i][0])
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
        for i in range(spine.lenght):
            x = abs(perlin1d(seedx, i / divx))
            y = perlin1d(seedy, i / divy) * pi
            vec = Vector2.pointed(x, y)
            vec.z = abs(perlin1d(seedz, i / divz))
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
            draw.line((coords.tuple(), newcoords.tuple()), fill=(0,
                                                                 0,
                                                                 255),
                                                           width=int(bone.z * scale))
            coords = newcoords
            if i in self.leg_points:
                draw.ellipse(((newcoords - Vector2(10, 10)).tuple(),
                              (newcoords + Vector2(10, 10)).tuple()),
                             fill=(0, 255, 0))
                draw.line((newcoords.tuple(), (newcoords.x, 2000)),
                          fill=(0, 255, 0),
                          width=5)
        draw.ellipse(((newcoords - Vector2(10, 10)).tuple(),
                      (newcoords + Vector2(10, 10)).tuple()),
                     fill=(255, 0, 0))