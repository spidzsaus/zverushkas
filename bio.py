from math import degrees
from extra_maths import Vector2, randint
from extra_maths import x as VARX
from extra_types import Category, DefaultValue

class Spine(Category):
    vfunc = VARX
    hfunc = VARX
    wfunc = VARX

    def __init__(self):
        self.default = 0
        
    def to_vectors(self):
        from extra_maths import perlin1d, Vector2, VectorChain
        from math import pi
        output = []
        seedx = self.seed_h
        seedy = self.seed_v
        seedz = self.seed_w
        divx = self.gradation
        divy = self.straightness
        divz = self.distribution
        xfunc = self.hfunc
        yfunc = self.vfunc
        zfunc = self.wfunc

        for i in range(self.length):
            x = xfunc(abs(perlin1d(seedx, i / divx)))
            y = yfunc(perlin1d(seedy, i / divy) * pi)
            vec = Vector2.pointed(x, y)
            vec.z = zfunc(abs(perlin1d(seedz, i / divz)))
            output.append(vec)
        return VectorChain(*output)

class Animal:
    def __init__(self):
        self.spine = Spine()
        self.legs = {}
    
    @staticmethod
    def from_params(length, gradation, straightness, 
                    distribution, leg_count, seed):
        from extra_maths import randint, perlin1d
        from math import pi
        
        animal = Animal()
        spine = Spine()
        spine.length = length
        spine.gradation = gradation
        spine.straightness = straightness
        spine.distribution = distribution
        spine.seed_v = seed * 10221
        spine.seed_h = seed * 26714
        spine.seed_w = seed * 51356
        animal.spine = spine
        
        joints = []
        vecs = spine.to_vectors()
        for i, bone in enumerate(vecs):
            if not i: continue
            a, b = bone.angle, vecs[i - 1].angle
            a, b = max(a, b), min(a, b)
            joints.append((i - 1, abs(a - b), bone.length()))
        joints.sort(key=lambda x: x[1], reverse=True)

        for i in range(leg_count):
            leg = Spine()
            leg.gradation = 100
            leg.straightness = straightness
            leg.distribution = distribution
            leg.length = 2
            leg.seed_v = seed * 42839 * (i + 1)
            leg.seed_h = seed * 35231 * (i + 1)
            leg.seed_w = seed * 51618 * (i + 1)
            leg.hfunc = joints[i][2] + VARX.abs() * 10
            leg.vfunc = VARX - pi / 2
            leg.wfunc = VARX * 0.6
            animal.legs[joints[i][0]] = leg

        return animal

class AnimalGenerator:
    @staticmethod
    def mamal(seed):
        length = randint(seed * 199, 5, 15)
        gradation = randint(seed * 235, 1, 1000) / 100
        straightness = randint(seed, 500, 1000) / 100
        distribution = randint(seed, 500, 1000) / 100
        leg_count = 2
        return Animal.from_params(length, gradation, straightness, distribution,
                                  leg_count, seed)


class AnimalDraw:
    def __init__(self, animal: Animal):
        self.animal = animal
    
    def draw(self, scale, draw=DefaultValue, coords=Vector2(0, 0), ground=DefaultValue):
        from extra_maths import Vector2
        left = coords.x
        right = coords.x
        down = coords.y
        up = coords.y
        spine = self.animal.spine.to_vectors()
        spine_dots = [(coords,)]
        legs_dots = [] 
        for i, bone in enumerate(spine):
            bone.y *= -1
            newcoords = coords + bone
            spine_dots.append((newcoords, int(bone.z)))
            coords = newcoords
            right = max(right, newcoords.x + bone.z)
            left = min(left, newcoords.x - bone.z)
            down = max(down, newcoords.y + bone.z)
            up = min(up, newcoords.y - bone.z)

            
            if i in self.animal.legs:
                leg = self.animal.legs[i].to_vectors()
                if ground is not DefaultValue:
                    leg = leg.cast_ik(Vector2(0, 0), Vector2(0, (coords.y - ground)))
                    print((ground - coords.y))
                dcoords = coords
                legs_dots.append([(coords,)])
                for j, bone in enumerate(leg):
                    bone.y *= -1
                    dnewcoords = dcoords + bone
                    legs_dots[-1].append((dnewcoords, int(bone.z)))
                    dcoords = dnewcoords
                    right = max(right, dnewcoords.x + bone.z)
                    left = min(left, dnewcoords.x - bone.z)
                    down = max(down, dnewcoords.y + bone.z)
                    up = min(up, dnewcoords.y - bone.z)

        offset = Vector2(0, 0)
        returnim = False
        if draw is DefaultValue:
            from PIL import Image, ImageDraw
            output = Image.new('RGBA', (abs(int(right - left) * scale), abs(int(down - up) * scale)))
            draw = ImageDraw.Draw(output)
            offset = Vector2(left, up)
            returnim = True
        
        if ground is not DefaultValue:
            draw.line(((0, ground * scale), (abs(int(right - left) * scale), ground * scale)), fill=(0, 255, 0))
        for i, dot in enumerate(spine_dots):
            if not i: continue
            draw.line((((spine_dots[i - 1][0] - offset) * scale).tuple(), 
                        ((dot[0] - offset) * scale).tuple()), fill=(165, 15 * i, 255),
                        width=dot[1] * scale)
        for i, leg in enumerate(legs_dots):
            for j, dot in enumerate(leg):
                if not j: continue
                draw.line((((leg[j - 1][0] - offset) * scale).tuple(), 
                            ((dot[0] - offset) * scale).tuple()), fill=(165, 15 * i, 255),
                            width=dot[1] * scale)
        draw.ellipse((((spine_dots[-1][0] - Vector2(0.04, 0.04) - offset) * scale).tuple(),
                      ((spine_dots[-1][0] + Vector2(0.04, 0.04) - offset) * scale).tuple()),
                     fill=(255, 0, 0))
        if returnim:
            return output
        

