if __name__ == '__main__':
    from bio import Animal, AnimalDraw
    from random import randint
    from PIL import Image, ImageDraw
    seed = randint(1, 99999999)
    print(seed)
    test = Animal.from_seed(seed)
    output = AnimalDraw(test).draw(250)
    output.show()
    