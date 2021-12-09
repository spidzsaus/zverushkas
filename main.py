if __name__ == '__main__':
    from bio import Animal
    from random import randint
    from PIL import Image, ImageDraw
    seed = randint(1, 99999999)
    print(seed)
    test = Animal.from_seed(seed)
    print(test.spine)
    output = Image.new('RGBA', (2000, 2000))
    draw = ImageDraw.Draw(output)    
    test.draw(draw, 350)
    output.show()
    