from extra_maths import Vector2, randint
from extra_maths import x as VARX
from extra_types import Category, DefaultValue

class Spine(Category):
    vfunc = VARX
    hfunc = VARX
    wfunc = VARX
    sfunc = VARX

    def __init__(self):
        self.default = 0
        
    def to_vectors(self):
        from extra_maths import perlin1d, Vector2, VectorChain
        from math import pi
        output = []
        seedx = self.seed_h
        seedy = self.seed_v
        seedz = self.seed_w
        seeds = self.seed_s
        divx = self.gradation
        divy = self.straightness
        divz = self.distribution
        divs = self.spreadvalue
        xfunc = self.hfunc
        yfunc = self.vfunc
        zfunc = self.wfunc
        sfunc = self.sfunc

        for i in range(self.length):
            x = xfunc(abs(perlin1d(seedx, i / divx)))
            y = yfunc(perlin1d(seedy, i / divy) * pi * 1.15)
            vec = Vector2.pointed(x, y)
            vec.z = zfunc(abs(perlin1d(seedz, (i + 1) / divz )))
            vec.a = sfunc(abs(perlin1d(seeds, (i + 1) / divs )))
            output.append(vec)
        return VectorChain(*output)

def head(seed, complexity=5) -> Spine:
    spine = Spine()
    spine.length = int(complexity)
    spine.gradation = 10
    spine.straightness = 30
    spine.distribution = 100
    spine.spreadvalue = 4
    spine.seed_v = seed * 92343
    spine.seed_h = seed * 42931
    spine.seed_w = seed * 41899
    spine.seed_s = seed * 58027
    return spine


class Animal:
    def __init__(self):
        self.spine = Spine()
        self.head = Spine()
        self.legs = {}

    def to_array(self):
        import numpy as np
        return np.array([self.spine.length,
                         self.spine.gradation,
                         self.spine.straightness,
                         self.spine.distribution,
                         self.spine.spreadvalue,
                         len(self.legs)
                         ])
    
    @classmethod
    def from_array(cls, seed, array):
        return cls.from_params(*[param for param in array], seed)

    @staticmethod
    def from_params(length, gradation, straightness, 
                    distribution, spreadvalue, leg_count, seed):
        from extra_maths import randint
        from math import pi
        
        leg_count = int(min(leg_count, length - 1))

        animal = Animal()
        spine = Spine()
        spine.length = int(length)
        spine.gradation = gradation
        spine.straightness = straightness
        spine.distribution = distribution
        spine.spreadvalue = spreadvalue
        animal.seed = seed
        spine.seed_v = seed * 10221
        spine.seed_h = seed * 26714
        spine.seed_w = seed * 51356
        spine.seed_s = seed * 51356
        animal.spine = spine
        
        joints = []
        vecs = spine.to_vectors()
        for i, bone in enumerate(vecs):
            if not i: continue
            v1, v2 = bone, vecs[i-1]
            try:
                comparator = 1 - (v1.dot_product(v2) / (v1.length() * v2.length()))
            except ZeroDivisionError:
                comparator = 0
            joints.append((i - 1, comparator, bone.length(), bone.z))
        le = len(vecs)
        joints.sort(key=lambda x: x[1], reverse=True)

        for i in range(leg_count):
            leg = Spine()
            leg.gradation = 100
            leg.straightness = straightness
            leg.distribution = distribution
            leg.spreadvalue = spreadvalue
            leg.length = 2
            leg.seed_v = seed * 42839 * (i + 1)
            leg.seed_h = seed * 35231 * (i + 1)
            leg.seed_w = seed * 51618 * (i + 1)
            leg.seed_s = seed * 25345 * (i + 1)
            leg.hfunc = joints[i][2] + VARX.abs() * 1.5  + 0.1
            #leg.hfunc = joints[i][2] + VARX * 0 + 0.2
            leg.vfunc = VARX - pi / 2
            leg.wfunc = joints[i][3] / 2 + VARX * 0.3
            animal.legs[joints[i][0]] = leg
        animal.head = head(seed * 931872123)

        return animal

class AnimalDraw:
    def __init__(self, animal=None):
        from extra_maths import Vector2
        self.animal = animal
        self.ground = DefaultValue
    
    def set_ground_level(self, level):
        self.ground = level
    
    def remove_ground(self):
        self.ground = DefaultValue
    
    def set_animal(self, animal):
        self.animal = animal
    
    def save_3d(self, path):
        import numpy as np
        from stl import mesh
        from math import pi

        def vec_to_vertex(vec, z):
            x, y = vec.tuple()
            return [x, z, y]
        
        def cross_vertecies(vec, w, z_offset=0, alpha=None, spread=0):
            if alpha is None: alpha = vec.angle
            return [vec_to_vertex(vec + Vector2.pointed(w, alpha + pi / 2), 0 + z_offset),
                    vec_to_vertex(vec, w + z_offset + spread),
                    vec_to_vertex(vec + Vector2.pointed(w, alpha - pi / 2), 0 + z_offset),
                    vec_to_vertex(vec, -w + z_offset - spread)]

        spine = self.animal.spine.to_vectors()
        coords = Vector2(0, 0)
        vertecies = []
        faces = []
        vb_offset = 0
        w = 0
        spr = 0
        local_leg_vb_size = 0
        for i, bone in enumerate(spine):
            newcoords = coords + bone

            a, b, c, d = cross_vertecies(coords, w / 2, alpha=bone.angle, spread=spr)
            e, f, g, h = cross_vertecies(newcoords, bone.z / 2, alpha=bone.angle, spread=bone.a)

            vertecies.extend([a, b, c, d, e, f, g, h])

            if i > 0:
                faces.append([vb_offset - 4 - local_leg_vb_size, vb_offset + 0, vb_offset - 1 - local_leg_vb_size])
                faces.append([vb_offset - 1 - local_leg_vb_size, vb_offset + 0, vb_offset + 3])

                faces.append([vb_offset - 4 - local_leg_vb_size, vb_offset + 0, vb_offset - 3 - local_leg_vb_size])
                faces.append([vb_offset - 3 - local_leg_vb_size, vb_offset + 1, vb_offset + 0])

                faces.append([vb_offset - 1 - local_leg_vb_size, vb_offset - 2 - local_leg_vb_size, vb_offset + 3])
                faces.append([vb_offset + 3, vb_offset + 2, vb_offset - 2 - local_leg_vb_size])

                faces.append([vb_offset - 3 - local_leg_vb_size, vb_offset + 1, vb_offset - 2 - local_leg_vb_size])
                faces.append([vb_offset + 1, vb_offset + 2, vb_offset - 2 - local_leg_vb_size])

            faces.append([vb_offset + 0, vb_offset + 4, vb_offset + 3])
            faces.append([vb_offset + 3, vb_offset + 4, vb_offset + 7])

            faces.append([vb_offset + 0, vb_offset + 4, vb_offset + 1])
            faces.append([vb_offset + 1, vb_offset + 5, vb_offset + 4])

            faces.append([vb_offset + 3, vb_offset + 2, vb_offset + 7])
            faces.append([vb_offset + 7, vb_offset + 6, vb_offset + 2])

            faces.append([vb_offset + 1, vb_offset + 5, vb_offset + 2])
            faces.append([vb_offset + 5, vb_offset + 6, vb_offset + 2])

            vb_offset += 8

            coords = newcoords
            w = bone.z
            spr = bone.a
            origin = w
            local_leg_vb_size = 0
            if i in self.animal.legs:
                for offset in -1, 1:
                    leg = self.animal.legs[i].to_vectors()
                    if self.ground is not DefaultValue:
                        leg = leg.cast_ik(Vector2(0, 0), Vector2(0, -coords.y - self.ground))
                    dcoords = coords
                    dw = w
                    dspread = origin
                    for j, bone in enumerate(leg):
                        bone.y *= -1
                        dnewcoords = dcoords + bone
                        bone._angle = bone.calc_angle()
                        a, b, c, d = cross_vertecies(dcoords, dw / 2, w * offset * j + offset * dspread , alpha=bone.angle)
                        e, f, g, h = cross_vertecies(dnewcoords, bone.z / 2, w * offset * (j + 1) + offset * bone.a, alpha=bone.angle)                            

                        vertecies.extend([a, b, c, d, e, f, g, h])
                        if not j:
                            faces.append([vb_offset + 0, vb_offset + 1, vb_offset + 2])
                            faces.append([vb_offset + 0, vb_offset + 2, vb_offset + 3])
                        else:
                            faces.append([vb_offset - 4, vb_offset + 0, vb_offset - 1])
                            faces.append([vb_offset - 1, vb_offset + 0, vb_offset + 3])

                            faces.append([vb_offset - 4, vb_offset + 0, vb_offset - 3])
                            faces.append([vb_offset - 3, vb_offset + 1, vb_offset + 0])

                            faces.append([vb_offset - 1, vb_offset - 2, vb_offset + 3])
                            faces.append([vb_offset + 3, vb_offset + 2, vb_offset - 2])

                            faces.append([vb_offset - 3, vb_offset + 1, vb_offset - 2])
                            faces.append([vb_offset + 1, vb_offset + 2, vb_offset - 2])

                        faces.append([vb_offset + 0, vb_offset + 4, vb_offset + 3])
                        faces.append([vb_offset + 3, vb_offset + 4, vb_offset + 7])

                        faces.append([vb_offset + 0, vb_offset + 4, vb_offset + 1])
                        faces.append([vb_offset + 1, vb_offset + 5, vb_offset + 4])

                        faces.append([vb_offset + 3, vb_offset + 2, vb_offset + 7])
                        faces.append([vb_offset + 7, vb_offset + 6, vb_offset + 2])

                        faces.append([vb_offset + 1, vb_offset + 5, vb_offset + 2])
                        faces.append([vb_offset + 5, vb_offset + 6, vb_offset + 2])

                        vb_offset += 8
                        local_leg_vb_size += 8

                        dcoords = dnewcoords
                        dw = bone.z
                        dspread = bone.a
        addw = w * 2
        head = self.animal.head.to_vectors()
        for i, bone in enumerate(head):
            newcoords = coords + bone

            a, b, c, d = cross_vertecies(coords, addw + w / 2, alpha=bone.angle, spread=spr)
            e, f, g, h = cross_vertecies(newcoords, addw + bone.z / 2, alpha=bone.angle, spread=bone.a)

            vertecies.extend([a, b, c, d, e, f, g, h])

            if i > 0:
                faces.append([vb_offset - 4 - local_leg_vb_size, vb_offset + 0, vb_offset - 1 - local_leg_vb_size])
                faces.append([vb_offset - 1 - local_leg_vb_size, vb_offset + 0, vb_offset + 3])

                faces.append([vb_offset - 4 - local_leg_vb_size, vb_offset + 0, vb_offset - 3 - local_leg_vb_size])
                faces.append([vb_offset - 3 - local_leg_vb_size, vb_offset + 1, vb_offset + 0])

                faces.append([vb_offset - 1 - local_leg_vb_size, vb_offset - 2 - local_leg_vb_size, vb_offset + 3])
                faces.append([vb_offset + 3, vb_offset + 2, vb_offset - 2 - local_leg_vb_size])

                faces.append([vb_offset - 3 - local_leg_vb_size, vb_offset + 1, vb_offset - 2 - local_leg_vb_size])
                faces.append([vb_offset + 1, vb_offset + 2, vb_offset - 2 - local_leg_vb_size])

            faces.append([vb_offset + 0, vb_offset + 4, vb_offset + 3])
            faces.append([vb_offset + 3, vb_offset + 4, vb_offset + 7])

            faces.append([vb_offset + 0, vb_offset + 4, vb_offset + 1])
            faces.append([vb_offset + 1, vb_offset + 5, vb_offset + 4])

            faces.append([vb_offset + 3, vb_offset + 2, vb_offset + 7])
            faces.append([vb_offset + 7, vb_offset + 6, vb_offset + 2])

            faces.append([vb_offset + 1, vb_offset + 5, vb_offset + 2])
            faces.append([vb_offset + 5, vb_offset + 6, vb_offset + 2])

            vb_offset += 8

            coords = newcoords
            w = bone.z
            spr = bone.a
            origin = w
            local_leg_vb_size = 0

        npvertecies = np.array(vertecies)
        npfaces = np.array(faces)
        animal_mesh = mesh.Mesh(np.zeros(npfaces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                animal_mesh.vectors[i][j] = npvertecies[f[j],:]
        animal_mesh.save(path)

    def draw_from_above(self, scale, draw=DefaultValue, position=Vector2(0, 0)):
        from extra_maths import Vector2
        maxwidth = 0
        spine = self.animal.spine.to_vectors()
        length = 0
        spine_dots = [(0,0)]
        legs_dots = [] 
        for i, bone in enumerate(spine):
            length += bone.x
            spine_dots.append((length, bone.z + bone.a))
            if i in self.animal.legs:
                legs_dots.append([(length, bone.z + bone.a, )])

        if draw is DefaultValue:
            position.x += maxwidth / 2
        for n, leg in enumerate(self.animal.legs.values()):
            leg = leg.to_vectors()
            leg_dots = legs_dots[n]
            originx = leg_dots[0][0]
            originz = leg_dots[0][1]
            
            for j, bone in enumerate(leg):
                dz = bone.z * j + bone.a
                leg_dots.append((originx, dz, bone.z))
                if dz + originz > maxwidth:
                    maxwidth = dz + originz

        returnim = False
        if draw is DefaultValue:
            from PIL import Image, ImageDraw
            output = Image.new('RGBA', (int(length * scale + 10), 
                                        int(maxwidth * 2 * scale)))
            draw = ImageDraw.Draw(output)
            returnim = True
        
        for i, dot in enumerate(spine_dots):
            if not i: continue
            draw.line(((int(spine_dots[i - 1][0] * scale + position.y), int(maxwidth * scale + position.x)), 
                       (int(spine_dots[i][0]  * scale + position.y), int(maxwidth * scale + position.x), )
                        ), fill=(165, 15 * i, 255),
                        width=int(spine_dots[i][1] * scale))
        for i, leg in enumerate(legs_dots):
            dx = maxwidth * scale + position.x
            for j, dot in enumerate(leg):
                if not j: continue
                draw.line(((int(dot[0]  * scale), int(dx + leg[j - 1][1] * scale)),
                           (int(dot[0]  * scale), int(dx + dot[1] * scale))), fill=(int(255 / (j + 1)), 45 * i, 165),
                            width=int(dot[2] * scale))
                draw.line(((int(dot[0]  * scale), int(dx - leg[j - 1][1] * scale)),
                           (int(dot[0]  * scale), int(dx - dot[1] * scale))), fill=(int(255 / (j + 1)), 45 * i, 165),
                            width=int(dot[2] * scale))
        if returnim:
            return output
    
    def draw(self, scale, draw=DefaultValue, position=Vector2(0, 0)):
        from extra_maths import Vector2
        ground = self.ground
        if ground is not DefaultValue: 
            ground *= scale
        left = 0
        right = 0
        down = 0
        up = 0
        spine = self.animal.spine.to_vectors()
        coords = Vector2(0, 0)
        spine_dots = [(Vector2(0, 0),)]
        legs_dots = [] 
        for i, bone in enumerate(spine):
            bone.y *= -1
            newcoords = coords + bone
            spine_dots.append((newcoords, bone.z))
            coords = newcoords
            right = max(right, newcoords.x + bone.z)
            left = min(left, newcoords.x - bone.z)
            down = max(down, newcoords.y + bone.z)
            up = min(up, newcoords.y - bone.z) 
            if i in self.animal.legs:
                legs_dots.append([(coords,)])

        if draw is DefaultValue:
            bposition = position
            position += Vector2(left, -up) * scale
        for n, leg in enumerate(self.animal.legs.values()):
            leg = leg.to_vectors()
            leg_dots = legs_dots[n]
            dcoords = leg_dots[0][0]
            if ground is not DefaultValue:
                leg = leg.cast_ik(Vector2(0, 0), Vector2(0, ((dcoords.y) * scale - ground)/scale))
            legs_dots.append([(coords,)])
            for j, bone in enumerate(leg):
                if ground is DefaultValue: bone.y *= -1
                dnewcoords = dcoords + bone
                leg_dots.append((dnewcoords, bone.z))
                dcoords = dnewcoords
                right = max(right, dnewcoords.x + bone.z)
                left = min(left, dnewcoords.x - bone.z)
                down = max(down, dnewcoords.y + bone.z)
                up = min(up, dnewcoords.y - bone.z)
        
        if draw is DefaultValue:
            position = bposition - Vector2(left, up) * scale

        returnim = False
        if draw is DefaultValue:
            from PIL import Image, ImageDraw
            output = Image.new('RGBA', (int(abs(right - left) * scale), 
                                        int(abs(down - up) * scale)))
            draw = ImageDraw.Draw(output)
            returnim = True
        
        if ground is not DefaultValue:
            draw.line(((0, ground - up * scale), (int(abs(right - left) * scale), ground - up * scale)), fill=(0, 255, 0))
        for i, dot in enumerate(spine_dots):
            if not i: continue
            draw.line((((spine_dots[i - 1][0]  * scale + position)).tuple(), 
                        ((dot[0]  * scale + position)).tuple()), fill=(165, 15 * i, 255),
                        width=int(dot[1] * scale))
        for i, leg in enumerate(legs_dots):
            for j, dot in enumerate(leg):
                if not j: continue
                draw.line((((leg[j - 1][0] * scale + position)).tuple(), 
                            ((dot[0] * scale + position)).tuple()), fill=(int(255 / (j + 1)), 45 * i, 165),
                            width=int(dot[1] * scale))
        draw.ellipse((((spine_dots[-1][0] - Vector2(0.04, 0.04)) * scale + position).tuple(),
                      ((spine_dots[-1][0] + Vector2(0.04, 0.04)) * scale + position).tuple()),
                     fill=(255, 0, 0))
        if returnim:
            return output
        

class Preset:
    def __init__(self, length=(9, 15), gradation=(0.2, 50.), 
                 straightness=(2, 20.0), distribution=(10.0, 50.0), leg_count=(1, 4),
                 spreadvalue=(10.0, 50.0)):
        self.length = length
        self.gradation = gradation
        self.straightness = straightness
        self.distribution = distribution
        self.spreadvalue = spreadvalue
        self.leg_count = leg_count
    
    def generate(self, seed, accuracy=100, paramseed=DefaultValue):
        if paramseed is DefaultValue:
            paramseed = seed
        salt = [52961]
        def param(source):
            if isinstance(source, tuple):
                salt[0] *= 1230
                return randint(paramseed * salt[0], source[0] * accuracy, 
                                                    source[1] * accuracy) / accuracy
            else:
                return source

        length = param(self.length)
        gradation = param(self.gradation)
        staightness = param(self.straightness)
        distribution = param(self.distribution)
        spreadvalue = param(self.spreadvalue)
        leg_count = param(self.leg_count)
        
        animal = Animal.from_params(length=int(length), gradation=gradation,
                                    straightness=staightness, distribution=distribution,
                                    leg_count=int(leg_count), spreadvalue=spreadvalue, seed=seed)

        return animal
    
    def __call__(self, seed, paramseed=DefaultValue):
        return self.generate(seed, paramseed=paramseed)