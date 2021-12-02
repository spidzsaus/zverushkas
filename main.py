if __name__ == '__main__':
    from extra_maths import Vector2
    from math import pi
    from bio import Animal
    from random import randint
    seed = randint(1, 99999999)
    print(Vector2.pointed(1, pi / 4))
    print(seed)
    test = Animal.from_seed(seed)
    print(test.spine)
    test.draw().show()
    