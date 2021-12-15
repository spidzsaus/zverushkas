from extra_maths import Vector2
from extra_types import Category, DefaultValue

class Spine(Category):
    def to_vectors(self):
        from extra_maths import perlin1d, Vector2
        from math import pi
        output = []
        seedx = self.seed_h
        seedy = self.seed_v
        seedz = self.seed_w
        divx = self.gradation
        divy = self.straightness
        divz = self.distribution
        mulx = self.length_modifier
        muly = self.curve_modifier
        mulz = self.width_modifier
        addx = self.forced_length
        addy = self.forced_angle
        addz = self.forced_width
        for i in range(self.length):
            x = (addx + abs(perlin1d(seedx, i / divx))) * mulx
            y = (addy + perlin1d(seedy, i / divy) * pi) * muly
            vec = Vector2.pointed(x, y)
            vec.z = (addz + abs(perlin1d(seedz, i / divz))) * mulz
            output.append(vec)
        return output

class Animal:
    def __init__(self):
        self.spine = Spine()
        self.legs = {}

    @staticmethod
    def from_seed(seed):
        from extra_maths import randint, perlin1d
        from math import pi
        animal = Animal()
        spine = Spine()
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
            

class AnimalDraw:
    def __init__(self, animal: Animal):
        self.animal = animal
    
    def draw(self, scale, draw=DefaultValue, coords=Vector2(0, 0)):
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
            newcoords = coords + (bone * scale)
            spine_dots.append((newcoords, int(bone.z * scale)))
            coords = newcoords
            right = max(right, newcoords.x + bone.z * scale)
            left = min(left, newcoords.x - bone.z * scale)
            down = max(down, newcoords.y + bone.z * scale)
            up = min(up, newcoords.y - bone.z * scale)

            
            if i in self.animal.legs:
                leg = self.animal.legs[i].to_vectors()
                dcoords = coords
                legs_dots.append([(coords,)])
                for j, bone in enumerate(leg):
                    bone.y *= -1
                    dnewcoords = dcoords + (bone * scale)
                    legs_dots[-1].append((dnewcoords, int(bone.z * scale)))
                    dcoords = dnewcoords
                    right = max(right, dnewcoords.x + bone.z * scale)
                    left = min(left, dnewcoords.x - bone.z * scale)
                    down = max(down, dnewcoords.y + bone.z * scale)
                    up = min(up, dnewcoords.y - bone.z * scale)
        offset = Vector2(0, 0)
        returnim = False
        if draw is DefaultValue:
            from PIL import Image, ImageDraw
            output = Image.new('RGBA', (abs(int(right - left)), abs(int(down - up))))
            draw = ImageDraw.Draw(output)
            offset = Vector2(left, up)
            returnim = True
        
        for i, dot in enumerate(spine_dots):
            if not i: continue
            draw.line(((spine_dots[i - 1][0] - offset).tuple(), 
                        (dot[0] - offset).tuple()), fill=(165, 15 * i, 255),
                        width=dot[1])
        for i, leg in enumerate(legs_dots):
            for j, dot in enumerate(leg):
                if not j: continue
                draw.line(((leg[j - 1][0] - offset).tuple(), 
                            (dot[0] - offset).tuple()), fill=(165, 15 * i, 255),
                            width=dot[1])
        draw.ellipse(((spine_dots[-1][0] - Vector2(scale / 25, scale / 25) - offset).tuple(),
                      (spine_dots[-1][0] + Vector2(scale / 25, scale / 25) - offset).tuple()),
                     fill=(255, 0, 0))
        if returnim:
            return output
        

